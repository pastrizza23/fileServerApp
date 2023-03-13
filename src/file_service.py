"""Uses for operations with files"""
import os
import datetime
from pathlib import Path

from utils.utils import generate_data
from utils.logger import logger
from utils.config_parser import config


class FileService:
    """Class for basic file operations"""

    @staticmethod
    def create_file(filename: str) -> bool:
        """Create file with provided filename and random data"""
        try:
            file_path = config()["app"]["file_folder"]
            path = os.path.join(file_path, filename)
            with open(os.path.abspath(path), 'w', encoding="utf-8") as file:
                file.write(generate_data())
                logger.info(f"Create {filename} with random data")
                return True
        except OSError:
            logger.error("Can not create a file")
            return False

    @staticmethod
    def delete_file(filename: str) -> bool:
        """Delete specified filename"""
        try:
            file_path = config()["app"]["file_folder"]
            path = os.path.join(file_path, filename)
            os.remove(os.path.abspath(path))
            logger.info(f"Remove {filename}")
            return True
        except FileNotFoundError:
            logger.error(f"File {filename} not exist")
            return False

    @staticmethod
    def read_file(filename: str) -> str:
        """Read file and return it content"""
        try:
            file_path = config()["app"]["file_folder"]
            path = os.path.join(file_path, filename)
            with open(os.path.abspath(path), encoding="utf-8") as file:
                content = file.read()
                logger.info(f"Read from {filename}")
                logger.debug(f"Content : {content}")
                return content
        except FileNotFoundError:
            logger.error(f"File {filename} not exist")
            return ''
        except OSError:
            logger.error(f"Can not read {filename}")
            return ''

    @staticmethod
    def get_metadata(filename: str) -> dict:
        """Gather and return metadata about file"""
        try:
            file_stats = os.stat(os.path.abspath(filename))
            file_name = Path(os.path.abspath(filename)).name
            file_format = file_name.split('.')[-1]
            file_size = file_stats.st_size
            creation_date = datetime.datetime.fromtimestamp(file_stats.st_ctime)\
                .strftime(config()["base"]["date_format"])
            modification_date = datetime.datetime.fromtimestamp(file_stats.st_mtime)\
                .strftime(config()["base"]["date_format"])

            logger.info(f"Read metadata from {filename}")

            return {
                'name': file_name,
                'format': file_format,
                'size': f"{file_size} bytes",
                'full_path': os.path.abspath(filename),
                'creation_date': creation_date,
                'modification_date': modification_date
            }
        except FileNotFoundError:
            logger.error(f"File {filename} does not exist")
            return {}
