"""File for helpers features"""
import random
from utils.config_parser import config
from utils.logger import logger


def generate_data() -> str:
    """Generates random data for files"""
    symbols = config()["base"]["ascii_and_digits"]
    data = ''.join(random.choice(symbols) for _ in range(config()["base"]["data_length"]))
    logger.debug(f"Generate such data: {data}")
    return data


def metadata_str(metadata) -> None:
    """Printing provided metadata"""
    for field, data in metadata.items():
        print(field, ": ", data)
