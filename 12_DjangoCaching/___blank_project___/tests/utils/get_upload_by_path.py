from django.core.files.uploadedfile import SimpleUploadedFile


def get_upload_by_path(path: str, file_name: str, file_type: str) -> SimpleUploadedFile:
    return SimpleUploadedFile(
        name=file_name,
        content=open(path, 'rb').read(),
        content_type=file_type
    )
