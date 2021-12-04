from flask_sqlalchemy import SQLAlchemy

import base64
import boto3
import datetime
from io import BytesIO
from mimetypes import guess_extension, guess_type
import os
from PIL import Image
import random
import re
import string

db = SQLAlchemy()

EXTENSIONS = ["png", "gif", "jpg", "jpeg", "webp"]
BASE_DIR = os.getcwd()
S3_BUCKET = "hackchallengeimages"
S3_BASE_URL = f"http://{S3_BUCKET}.s3.us-east-2.amazonaws.com"
# your classes here
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    outifts = db.relationship("Outfits", cascade='delete')

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "outifts": [o.serialize() for o in self.outifts]
        }

class Outfits(db.Model):
    __tablename__ = 'outifts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    top_id = db.Column(db.Integer, nullable=False)
    bottom_id = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.top_id = kwargs.get("top_id")
        self.bottom_id = kwargs.get("bottom_id")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "top_id": self.top_id,
            "bottom_id": self.bottom_id
        }

class Clothes(db.Model):
    __tablename__ = 'clothes'
    id = db.Column(db.Integer, primary_key=True)
    base_url = db.Column(db.String, nullable=True)
    salt = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)

    top = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.create(kwargs.get("image_data"))
        self.top = kwargs.get("top")

    def serialize(self):
        return {
            "id": self.id,
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "top": self.top
        }
    
    def create(self, image_data):
        try:
            ext = guess_extension(guess_type(image_data)[0])[1:]
            if ext not in EXTENSIONS:
                raise Exception(f"Extension {ext} not supported")

            salt = "".join(
                random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits
                )
            for _ in range(16)
            )

            img_str = re.sub("^data:image/.+;base64,", "", image_data)
            img_data = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_data))

            self.base_url = S3_BASE_URL
            self.salt = salt
            self.extension = ext

            img_filename = f"{salt}.{ext}"
            self.upload(img, img_filename)
        except Exception as e:
            print(f"Unable to create image due to {e}")

    def upload(self, img, img_filename):
        try:
            img_temploc = f"{BASE_DIR}/{img_filename}"
            img.save(img_temploc)

            s3client = boto3.client("s3")
            s3client.upload_file(img_temploc, S3_BUCKET, img_filename)

            s3_resource = boto3.resource("s3")
            object_acl = s3_resource.ObjectAcl(S3_BUCKET, img_filename)
            object_acl.put(ACL="public-read")
            os.remove(img_temploc)

        except Exception as e:
            print("Unable to open image due to {e}")

# class Bottoms(db.Model):
#     __tablename__ = 'bottoms'
#     id = db.Column(db.Integer, primary_key=True)
#     img = db.Column(db.Integer, nullable=False)

#     def __init__(self, **kwargs):
#         self.img = kwargs.get("img")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "img": self.img
#         }
