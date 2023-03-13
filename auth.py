"""Authentication API service"""
from flask import Flask, request
import json

import auth.authModel as authModel
import auth.utils as utils

app = Flask(__name__)


@app.route("/user", methods=["POST", "DELETE"])
def user():
    if request.method == "POST":
        user_email = request.json.get("email")
        client_secret = request.json.get("password")

        hashed_secret = utils.hash_sha256_password(client_secret)
        create_response = authModel.create(user_email, hashed_secret)

        return {'success': create_response}

    elif request.method == "DELETE":
        authorization_header = request.headers.get('authorization')
        token = authorization_header.replace("Bearer ", "")
        verification = authModel.verify(token)

        if verification != {"success": False}:
            uuid = verification.get("uuid")

            create_response = authModel.delete(uuid)
            if create_response:
                authModel.blacklist(token)
            return {'success': create_response}
        else:
            return {'success': False, 'message': 'Access Denied'}
    else:
        return {'success': False}


@app.route("/auth", methods=["POST"])
def auth():
    user_email = request.json.get("email")
    client_secret = request.json.get("password")

    hashed_client_secret = utils.get_hashed_password(user_email, client_secret)

    authentication = authModel.authenticate(user_email, hashed_client_secret)

    if not authentication:
        return {'success': False}
    else:
        return json.dumps(authentication)


@app.route("/verify", methods=["POST"])
def verify():
    authorization_header = request.headers.get('authorization')
    token = authorization_header.replace("Bearer ", "")
    verification = authModel.verify(token)
    return verification


@app.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get('authorization')
    status = authModel.blacklist(token)
    return {'success': status}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
