from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class CloudflareR2Storage(S3Boto3Storage):
    """
    Custom storage backend for Cloudflare R2
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint_url = settings.CLOUDFLARE_R2_ENDPOINT_URL
        
    def url(self, name):
        """
        返回文件的公开访问URL
        """
        if hasattr(settings, 'CLOUDFLARE_R2_PUBLIC_URL'):
            return f"{settings.CLOUDFLARE_R2_PUBLIC_URL}/{name}"
        return super().url(name)
