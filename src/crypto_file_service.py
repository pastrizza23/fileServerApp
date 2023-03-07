"""Crypto module for files operations"""
import hashlib
import os
from collections import OrderedDict
from Crypto.Cipher import AES

from utils.logger import logger
from utils.config_parser import config
from src.file_service import FileService


class CryptoFileService(FileService):
    """Class for cryptographic operations on file services"""
    __secret_key = config()["crypto"]["secret_key"]
    __aes_key = config()["crypto"]["AES_key"].encode()

    def sign_file(self, path: str) -> bool:
        """Create signature file of provided file"""
        try:
            data = self.get_data_for_sign(path)
            path = os.path.join(FileService.FILE_PATH, path)
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
            path = os.path.join(FileService.FILE_PATH, path)
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
            path = os.path.join(FileService.FILE_PATH, path)

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

    def encrypt_file(self, path: str) -> bool:
        """Encrypt provided file"""
        try:
            path = os.path.join(self.FILE_PATH, path)

            with open(path, "rb") as file:
                content = file.read()

            cipher = AES.new(self.__aes_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(content)

            with open(f"{path}.encrypt", "wb") as file:
                [file.write(x) for x in (cipher.nonce, tag, ciphertext)]  # pylint: disable=expression-not-assigned

            logger.info(f"File {path} was encrypted")
            return True
        except FileNotFoundError:
            logger.error(f"File {path} doesn't exist")
            return False

    def decrypt_file(self, path: str) -> bool:
        """Encrypt provided file"""
        try:
            path = os.path.join(self.FILE_PATH, path)

            with open(f"{path}.encrypt", "rb") as file:
                nonce, tag, ciphertext = [file.read(x) for x in (16, 16, -1) ]

            cipher = AES.new(self.__aes_key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
            logger.info(f"Decrypting {path} ...")

            with open(f"{path}.decrypt", 'wb') as file:
                file.write(data)

            return True
        except FileNotFoundError:
            logger.error(f"File {path} doesn't exist")
            return False
