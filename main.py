"""Main module for working from cli"""
import argparse
from src.crypto_file_service import CryptoFileService
from utils import utils


parser = argparse.ArgumentParser(description='App for working with files.')
subparser = parser.add_subparsers(dest="command", description="Choose a command")
create = subparser.add_parser('create', help='Creates a file with given filename')
delete = subparser.add_parser('delete', help='Deletes file with given path.')
read = subparser.add_parser('read', help='Reads content of given file.')
metadata = subparser.add_parser('metadata', help="Returns file's metadata.")

create.add_argument("--filename", '-f', required=True, type=str, help="Filename to be created")
create.add_argument("--sign", "-s", action='count', help="Create file signature hash file")

delete.add_argument("--filename", '-f', required=True, type=str, help="Filename to be deleted")

read.add_argument("--filename", '-f', required=True, type=str, help="Filename to be readed")
read.add_argument("--integrity", "-i", action='count', help="Verify file integrity")

metadata.add_argument("--filename", '-f', required=True, type=str, help="Filename")

args = parser.parse_args()

if __name__ == "__main__":
    fs = CryptoFileService()
    if args.command == "create":
        if args.sign:
            fs.create_file(args.filename)
            fs.sign_file(args.filename)
        else:
            fs.create_file(args.filename)
    elif args.command == "delete":
        fs.delete_file(args.filename)
    elif args.command == "read":
        if args.integrity:
            if fs.verify_signature(args.filename):
                print(fs.read_file(args.filename))
            else:
                utils.logger.error(f"File integrity broken")
    elif args.command == "metadata":
        utils.metadata_str(fs.get_metadata(args.metadata))
