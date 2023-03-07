"""Main module for working from cli"""
import argparse
from src.crypto_file_service import CryptoFileService as fs
from utils import utils


parser = argparse.ArgumentParser(description='App for working with files.')
subparser = parser.add_subparsers(dest="command", description="Choose a command")
create = subparser.add_parser('create', description='Creates a file with given filename',
                              help='Creates a file with given filename')
delete = subparser.add_parser('delete', description='Deletes file with given path.',
                              help='Deletes a file with given filename')
read = subparser.add_parser('read', description='Reads content of given file.',
                            help='Reads content of given file.')
metadata = subparser.add_parser('metadata', description="Returns file's metadata.",
                                help="Returns file's metadata.")

create.add_argument("--filename", '-f', required=True, type=str, help="Filename to be created")
create.add_argument("--sign", "-s", action='count', help="Create file signature hash file")
create.add_argument("--encrypt", "-e", action='count', help="Create encrypt version of file")

delete.add_argument("--filename", '-f', required=True, type=str, help="Filename to be deleted")

read.add_argument("--filename", '-f', required=True, type=str, help="Filename to be readed")
read.add_argument("--integrity", "-i", action='count', help="Verify file integrity")
read.add_argument("--decrypt", "-d", action='count', help="Create file signature hash file")

metadata.add_argument("--filename", '-f', required=True, type=str, help="Filename")

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == "create":
        fs.create_file(args.filename)
        if args.sign:
            fs.sign_file(fs(), args.filename)
        if args.encrypt:
            fs.encrypt_file(fs(), args.filename)
    elif args.command == "delete":
        fs.delete_file(args.filename)
    elif args.command == "read":
        if args.decrypt:
            fs.decrypt_file(fs(), args.filename)
        if args.integrity:
            if not fs.verify_signature(fs(), args.filename):
                utils.logger.error(f"File integrity broken")

        print(fs.read_file(args.filename))
    elif args.command == "metadata":
        utils.metadata_str(fs.get_metadata(args.metadata))
