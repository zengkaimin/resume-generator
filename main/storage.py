from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import boto3
from botocore.config import Config

class CloudflareR2Storage(S3Boto3Storage):
    """
    Custom storage class for Cloudflare R2
    """
    def __init__(self, *args, **kwargs):
        self.endpoint_url = settings.CLOUDFLARE_R2_ENDPOINT_URL
        self.access_key = settings.CLOUDFLARE_R2_ACCESS_KEY_ID
        self.secret_key = settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY
        self.bucket_name = settings.CLOUDFLARE_R2_BUCKET_NAME
        self.region_name = 'auto'
        
        kwargs['access_key'] = self.access_key
        kwargs['secret_key'] = self.secret_key
        kwargs['bucket_name'] = self.bucket_name
        kwargs['endpoint_url'] = self.endpoint_url
        kwargs['region_name'] = self.region_name
        
        super().__init__(*args, **kwargs)
        
        # 创建一个boto3客户端用于列出文件
        self.client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4'),
        )

    def url(self, name):
        """
        返回文件的URL
        """
        if hasattr(settings, 'CLOUDFLARE_R2_PUBLIC_URL'):
            return f"{settings.CLOUDFLARE_R2_PUBLIC_URL}/{name}"
        return super().url(name)

    def list_files(self, prefix=''):
        """列出指定前缀下的所有文件"""
        try:
            print(f"Listing files with prefix: {prefix}")
            print(f"Using bucket: {self.bucket_name}")
            
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            print(f"R2 response: {response}")
            
            if 'Contents' in response:
                files = [obj['Key'] for obj in sorted(
                    response['Contents'],
                    key=lambda x: x['LastModified'],
                    reverse=True
                )]
                print(f"Found files: {files}")
                return files
            print("No contents found in response")
            return []
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
