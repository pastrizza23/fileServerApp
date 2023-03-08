"""This module used for handle web request"""
import os
from flask import Flask, jsonify, abort, request

from src.crypto_file_service import CryptoFileService as fs
from utils.logger import logger
from utils.config_parser import update_config

app = Flask(__name__)


@app.route('/files/list', methods=['GET'])
def ls_files():  # pylint: disable=inconsistent-return-statements
    """List files in work directory"""
    try:
        logger.info("Request for list files")
        files = os.listdir(fs.FILE_PATH)
        files_metadata = [fs.get_metadata(os.path.join(fs.FILE_PATH, file)) for file in files]

        response = jsonify(files_metadata)

        if not response.get_json():
            abort(404, "Files not found")

        return response, 200
    except OSError:
        err_mess = 'Can`t list a directory'
        logger.error(err_mess)
        abort(500, err_mess)


@app.route('/files', methods=['GET'])
def get_file():  # pylint: disable=inconsistent-return-statements
    """Return info and content of file
    Take file name as paramether ?file=<filename>"""
    try:
        file = request.args.get('file', default='', type=str)

        if file:
            logger.info(f"Request to get {file}")
            file = os.path.join(fs.FILE_PATH, file)

            if os.path.isfile(file):
                file_metadata = fs.get_metadata(file)
                file_data = fs.read_file(file)

                response = jsonify(file_metadata, file_data)

                if not response.get_json():
                    abort(404, "File not found")

                return response, 200

            abort(404, "File not found")

        abort(400, "Specify /files?file=<filename>")
    except OSError:
        err_mess = 'Can`t get a file'
        logger.error(err_mess)
        abort(500, err_mess)


@app.route('/files', methods=["POST"])
def create_file():  # pylint: disable=inconsistent-return-statements
    """Crete files with provoded filename
    Takes {"filename":"{filename}"}"""
    try:
        logger.info("Received request for file creation.")
        if request.content_type != 'application/json':
            err_massage = "Content-Type must be 'application/json'."
            logger.error(err_massage)
            abort(400, err_massage)

        data = request.get_json()
        if 'filename' not in data:
            err_massage = "Key 'content' is missing."
            logger.error(err_massage)
            abort(400, err_massage)

        content = data['filename']
        filename = fs.create_file(content)
        if filename:
            response = jsonify({'filename': content})
            return response, 201

        abort(400, "Can not create such file")
    except OSError:
        err_mess = 'Can not create such file'
        logger.error(err_mess)
        abort(500, err_mess)


@app.route('/files/<file>', methods=["DELETE"])
def delete_file(file):  # pylint: disable=inconsistent-return-statements
    """Delete a file
    Takes /files/<filename>"""
    try:
        if file:
            logger.info(f"Received request for {file} deletion.")
            path = os.path.join(fs.FILE_PATH, file)

            if os.path.isfile(path):
                deleted = fs.delete_file(file)

                if deleted:
                    response = jsonify(deleted)
                    logger.info(f"Delete {file}")
                    return response, 200
        abort(404, "File not found")
    except OSError:
        err_mess = 'Can not delete such file'
        logger.error(err_mess)
        abort(500, err_mess)


@app.route('/change_file_dir', methods=['POST'])
def change_file_dir():  # pylint: disable=inconsistent-return-statements
    """Change working directory"""
    try:
        logger.info("Received request for directory change.")
        if request.content_type != 'application/json':
            err_massage = "Content-Type must be 'application/json'."
            logger.error(err_massage)
            abort(400, err_massage)

        data = request.get_json()
        if 'path' not in data:
            err_massage = "Key 'path' is missing."
            logger.error(err_massage)
            abort(400, err_massage)

        content = data['path']

        if not os.path.exists(content):
            os.mkdir(content)

        update_config('app', 'file_folder', content)

        response = jsonify({'path': content})
        return response, 200
    except OSError:
        err_mess = 'Can not change working directory'
        logger.error(err_mess)
        abort(500, err_mess)
