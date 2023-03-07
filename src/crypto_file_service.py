"""Crypto module for files operations"""
import hashlib
from collections import OrderedDict

from utils.logger import logger
from utils.config_parser import config
from src.file_service import FileService


class CryptoFileService(FileService):
    """Class for cryptographic operations on file services"""
    __secret_key = config()["crypto"]["secret_key"]

    def sign_file(self, path: str) -> bool:
        """Create signature file of provided file"""
        try:
            data = self.get_data_for_sign(path)
            if data:
                with open(f"{path}.sha256", "wb") as signature:
                    signature.write(self.get_signature(data))
                    logger.info(f"Write signature of {path}, to {path}.sha256")
                return True
            return False
        except OSError:
            logger.error(f"Can not create sign for {path}")
            return False

    def get_data_for_sign(self, path: str) -> str:
        """Prepare file data for hashing"""
        try:
            with open(path, "rb") as file:
                content = file.read()

            data = OrderedDict(name=path, metadata=self.get_metadata(path), content=content)

            return str(data)
        except FileNotFoundError:
            logger.error(f"File {path} can`t be found")
            return ''

    def get_signature(self, data: str) -> bytes:
        """Create signature of provided data"""
        sha = hashlib.sha256()
        sha.update(data.encode("utf-8"))
        sha.update(self.__secret_key.encode("utf-8"))
        signature = sha.digest()

        return signature

    def verify_signature(self, path: str) -> bool:
        """Verify if file was compromise"""
        try:
            data = self.get_data_for_sign(path)

            with open(f"{path}.sha256", "rb") as file:
                file_signature = file.read()
                logger.info(f"Read {path} signature")

            if data:
                gen_signature = self.get_signature(data)
                logger.info(f"Get {path} signature")
                return gen_signature == file_signature

            return False
        except FileNotFoundError:
            logger.error(f"There are no sign for {path}")
            return False
