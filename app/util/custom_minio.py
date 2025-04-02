from datetime import datetime, timedelta
from urllib.parse import urlunsplit

from minio import Minio, time
from minio.helpers import DictType, check_bucket_name, check_object_name, url_replace
from minio.signer import presign_v4


class CustomMinio(Minio):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self.public_endpoint = public_endpoint = kwargs.pop('public_endpoint', None)
        super().__init__(*args, **kwargs)

    def get_presigned_url(
        self,
        method: str,
        bucket_name: str,
        object_name: str,
        expires: timedelta = timedelta(days=7),
        response_headers: DictType | None = None,
        request_date: datetime | None = None,
        version_id: str | None = None,
        extra_query_params: DictType | None = None,
        public_enpoint: str | None = None,
    ) -> str:
        check_bucket_name(bucket_name, s3_check=self._base_url.is_aws_host)
        check_object_name(object_name)
        if expires.total_seconds() < 1 or expires.total_seconds() > 604800:
            raise ValueError('expires must be between 1 second to 7 days')

        region = self._get_region(bucket_name)
        query_params = extra_query_params or {}
        query_params.update({'versionId': version_id} if version_id else {})
        query_params.update(response_headers or {})
        creds = self._provider.retrieve() if self._provider else None
        if creds and creds.session_token:
            query_params['X-Amz-Security-Token'] = creds.session_token
        url = self._base_url.build(
            method,
            region,
            bucket_name=bucket_name,
            object_name=object_name,
            query_params=query_params,
        )

        # change compare to the original code
        if self.public_endpoint:
            url = url_replace(url, netloc=self.public_endpoint)

        if creds:
            url = presign_v4(
                method,
                url,
                region,
                creds,
                request_date or time.utcnow(),
                int(expires.total_seconds()),
            )
        url = urlunsplit(url)
        return url
