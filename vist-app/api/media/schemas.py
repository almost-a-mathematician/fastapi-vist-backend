from fastapi import HTTPException, status, UploadFile
import filetype


def validate_file(file: UploadFile, max_size, types: list[str]):

	file_info = filetype.guess(file.file)

	if file_info is None:
		raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unable to determine file type", )

	detected_content_type = file_info.extension.lower()

	if detected_content_type not in types or detected_content_type not in types:
		raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type", )

	real_file_size = 0

	for chunk in file.file:
		real_file_size += len(chunk)
		if real_file_size > max_size:
			raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large")

	file.file.seek(0)
