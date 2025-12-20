import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria o bucket S3 se não existir"

    def handle(self, *args, **options):
        s3 = boto3.client(
            "s3",
            region_name="django-base",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        )

        try:
            s3.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            self.stdout.write("Bucket já existe.")
        except ClientError:
            s3.create_bucket(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                CreateBucketConfiguration={"LocationConstraint": "django-base"},
            )
            self.stdout.write("Bucket criado com sucesso.")
