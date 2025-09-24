import abc
import io
import aiofiles
import uuid
import os
from pathlib import Path
from miniopy_async import Minio


class MediaService(abc.ABC):

	@abc.abstractmethod
	async def upload(self, img: bytes) -> str:
		...

	@abc.abstractmethod
	async def download(self, id: str) -> bytes | None:
		...

	@abc.abstractmethod
	async def streaming_download(self, id: str):
		...

	@abc.abstractmethod
	async def delete(self, id: str) -> True | False:
		...


class FileMediaService(MediaService):

	def __init__(self, storage_relative_path: str):
		self.storage_relative_path = storage_relative_path

	def get_path(self, id: str):
		project_root = os.getcwd()

		storage_path = os.path.join(project_root, self.storage_relative_path.lstrip('./'))
		file_path = os.path.join(storage_path, str(id))

		os.makedirs(storage_path, exist_ok=True)

		return file_path

	async def upload(self, img):
		img_id = str(uuid.uuid4())

		file_path = self.get_path(img_id)

		async with aiofiles.open(file_path, mode='wb') as f:
			await f.write(img)

		return img_id

	async def download(self, id):
		file_path = self.get_path(id)
		try:
			async with aiofiles.open(file_path, mode='rb') as f:
				img = await f.read()
		except FileNotFoundError:
			return None

		return img

	async def streaming_download(self, id):
		file_path = self.get_path(id)
		try:
			async with aiofiles.open(file_path, mode='rb'):
				pass

			async def generator():
				async with aiofiles.open(file_path, mode='rb') as f:
					while chunk := await f.read(1024 * 1024):
						yield chunk

			return generator()
		except FileNotFoundError:
			return None

	async def delete(self, id):
		file_path = self.get_path(id)

		try:
			os.remove(file_path)
		except FileNotFoundError:
			return False
		return True


class S3MediaService(MediaService):

	def __init__(self, minio_endpoint, minio_access_key, minio_secret_key, minio_secure, minio_bucket_name):
		self.client = Minio(
			endpoint=minio_endpoint,
			access_key=minio_access_key,
			secret_key=minio_secret_key,
			secure=minio_secure
		)
		self.minio_bucket_name = minio_bucket_name

	async def upload(self, img):
		img_id = str(uuid.uuid4())

		await self.client.put_object(self.minio_bucket_name, img_id, io.BytesIO(img), img.__len__())

		return img_id

	async def download(self, id):
		raise Exception('Not implemented')

	async def streaming_download(self, id):
		try:
			result = await self.client.get_object(self.minio_bucket_name, id)

			if not result.ok:
				return None

			async def generator():
				async for chunk in result.content.iter_chunked(1024 * 1024):
					yield chunk

			return generator()
		except:
			return None

	async def delete(self, id):
		await self.client.remove_object(self.minio_bucket_name, id)

		return True


# media_service = FileMediaService(os.getenv('STORAGE_PATH', './storage'))

media_service = S3MediaService(
	minio_endpoint=os.getenv('MINIO_ENDPOINT'),
	minio_access_key=os.getenv('MINIO_ACCESS_KEY'),
	minio_secret_key=os.getenv('MINIO_SECRET_KEY'),
	minio_secure=int(os.getenv('MINIO_SECURE')),
	minio_bucket_name=os.getenv('MINIO_BUCKET_NAME')
)
