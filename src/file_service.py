"""Uses for operations with files"""
import os
import datetime
from pathlib import Path

from utils.utils import generate_data
from utils.logger import logger
from src.config_parser import config


def create_file(filename: str) -> bool:
    """Create file with provided filename and random data"""
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(generate_data())
            logger.info(f"Create {filename} with random data")
            return True
    except OSError:
        logger.error("Can not create a file")
        return False


def delete_file(filename: str) -> bool:
    """Delete specified filename"""
    try:
        os.remove(filename)
        logger.info(f"Remove {filename}")
        return True
    except FileNotFoundError:
        logger.error(f"File {filename} not exist")
        return False


def read_file(filename: str) -> str:
    """Read file and return it content"""
    try:
        with open(filename, encoding="utf-8") as file:
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


def get_metadata(filename: str) -> dict:
    """Gather and return metadata about file"""
    try:
        file_stats = os.stat(filename)
        file_name = Path(filename).name
        file_format = file_name.split('.')[-1]
        file_size = file_stats.st_size
        creation_date = datetime.datetime.fromtimestamp(file_stats.st_ctime)\
            .strftime(config()["date_format"])
        access_date = datetime.datetime.fromtimestamp(file_stats.st_atime)\
            .strftime(config()["date_format"])
        modification_date = datetime.datetime.fromtimestamp(file_stats.st_mtime)\
            .strftime(config()["date_format"])

        logger.info(f"Read metadata from {filename}")

        return {
            'name': file_name,
            'format': file_format,
            'size': f"{file_size} bytes",
            'fill_path': os.path.abspath(filename),
            'creation_date': creation_date,
            'last_access_date': access_date,
            'modification_date': modification_date
        }
    except FileNotFoundError:
        logger.error(f"File {filename} does not exist")
        return {}
