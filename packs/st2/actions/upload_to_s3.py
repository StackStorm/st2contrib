from lib.action import St2BaseAction
import s3

__all__ = [
    'UploadToS3'
]


class UploadToS3(St2BaseAction):
    def run(self, file_name, remote_file, bucket):
        try:
            connection = s3.S3Connection(**self.config['s3'])
            storage = s3.Storage(connection)
            remote_name = s3.S3Name(remote_file, bucket=bucket)
            storage.write(file_name, remote_name)
            exists, metadata = storage.exists(remote_name)
            assert exists
            payload = {
                "status": "ok",
                "uploaded_file": remote_file,
            }

            return payload
        except StorageError, e:
            raise Exception('S3 upload failed: {}'.format(e))
