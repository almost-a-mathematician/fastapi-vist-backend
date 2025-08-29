import abc
import aiofiles
import uuid
import os
from pathlib import Path


class MediaService(abc.ABC):

    @abc.abstractmethod
    async def upload(self, img: bytes) -> str:
        # async def upload bytes: -> str(file_id) при первой загрузке картинки
        ...

    @abc.abstractmethod
    async def download(self, id: str) -> bytes | None:
        # async def download id: -> bytes
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


media_service = FileMediaService(os.getenv('STORAGE_PATH', './storage'))