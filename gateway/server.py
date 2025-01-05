import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
import logging
from bson.objectid import ObjectId

server = Flask(__name__)

mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@server.route('/login', methods=["POST"])
def login():
    token, err = access.login(request)
    return token if not err else err
    
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file required.", 400
        
        for _, f in request.files.items():
            logger.info(f"Inside gateway:server.upload")
            err = util.upload(f, fs_videos, channel, access)

            if err:
                return err
            
        return "Success!", 200
    else:
        return "Not authorized.", 401

@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f'{fid_string}.mp3')
        except Exception as err:
            logger.info(err)
            return "Internal server error", 500

    return "Not authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)