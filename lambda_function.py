
import os
from io import BytesIO
from urllib.parse import unquote_plus

import boto3
from PIL import Image, ImageOps

s3 = boto3.client("s3")
DESTINATION_BUCKET = os.environ["DESTINATION_BUCKET"]


def lambda_handler(event, context):
    for record in event.get("Records", []):
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = unquote_plus(record["s3"]["object"]["key"])

        if source_bucket == DESTINATION_BUCKET:
            raise ValueError("Source and destination buckets must differ")

        if not source_key.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"Skipping unsupported file: {source_key}")
            continue

        response = s3.get_object(
            Bucket=source_bucket,
            Key=source_key
        )

        with Image.open(response["Body"]) as original:
            image_format = original.format or "JPEG"
            image = ImageOps.exif_transpose(original)
            image.thumbnail((300, 300))

            output = BytesIO()

            if image_format.upper() == "PNG":
                if image.mode not in ("RGB", "RGBA", "L", "LA"):
                    image = image.convert("RGBA")
                image.save(output, format="PNG", optimize=True)
                extension = ".png"
                content_type = "image/png"
            else:
                if image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")
                image.save(output, format="JPEG", optimize=True)
                extension = ".jpg"
                content_type = "image/jpeg"

        filename = source_key.rsplit("/", 1)[-1]
        name, _ = os.path.splitext(filename)
        destination_key = f"thumbnails/{name}_thumb{extension}"

        s3.put_object(
            Bucket=DESTINATION_BUCKET,
            Key=destination_key,
            Body=output.getvalue(),
            ContentType=content_type
        )

        print(
            f"Created s3://{DESTINATION_BUCKET}/{destination_key}"
        )

    return {
        "statusCode": 200,
        "body": "Image processing completed"
    }