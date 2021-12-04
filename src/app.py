from db import db
from flask import Flask
from flask import request
import json

from db import Users
from db import Clothes 
from db import Outfits 

import os

app = Flask(__name__)
db_filename = "outFit.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here
#USERS
@app.route("/api/users/")
def get_users():
    return json.dumps({"users": [u.serialize() for u in Users.query.all()]}), 200

@app.route("/api/users/", methods=['POST'])
def post_users():
    body = json.loads(request.data)
    username = body.get("username", False)
    if not username:
        return json.dumps({"error": "Invalid fields"}), 400
    else:
        new_user = Users(username=username)
        db.session.add(new_user)
        db.session.commit()
        return json.dumps(new_user.serialize()), 201

@app.route("/api/users/<int:id>/")
def get_user_id(id):
    user = Users.query.filter_by(id=id).first()
    if user is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps(user.serialize()), 200

@app.route("/api/users/<int:id>/", methods=['DELETE'])
def del_user_id(id):
    user = Users.query.filter_by(id=id).first()
    if user is None:
        return json.dumps({"error": "Invalid fields"}), 400
    db.session.delete(user)
    db.session.commit()
    return json.dumps(user.serialize()), 200

#OUTFITS
@app.route("/api/outfits/")
def get_outfits():
    return json.dumps({"outfits": [o.serialize() for o in Outfits.query.all()]}), 200

@app.route("/api/outfits/", methods=['POST'])
def post_outfit():
    body = json.loads(request.data)
    user_id = body.get("user_id", False)
    top_id = body.get("top_id", False)
    bottom_id = body.get("bottom_id", False)
    if not user_id or not top_id or not bottom_id:
        return json.dumps({"error": "Invalid fields"}), 400
    else:
        new_outfit = Outfits(user_id=user_id, top_id=top_id, bottom_id=bottom_id)
        db.session.add(new_outfit)
        db.session.commit()
        return json.dumps(new_outfit.serialize()), 201

@app.route("/api/outfits/<int:id>/")
def get_outfit_id(id):
    outfit = Outfits.query.filter_by(id=id).first()
    if outfit is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps(outfit.serialize()), 200

@app.route("/api/outfits/user/<int:id>/")
def get_outfit_by_user_id(id):
    outfits = Outfits.query.filter_by(user_id=id)
    if outfits is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps({"outfits": [o.serialize() for o in outfits]}), 200

@app.route("/api/outfits/<int:id>/", methods=['DELETE'])
def del_outfit_id(id):
    outfit = Outfits.query.filter_by(id=id).first()
    if outfit is None:
        return json.dumps({"error": "Invalid fields"}), 400
    db.session.delete(outfit)
    db.session.commit()
    return json.dumps(outfit.serialize()), 200


#TOPS
@app.route("/api/tops/")
def get_tops():
    return json.dumps({"tops": [t.serialize() for t in Clothes.query.filter_by(top=True)]}), 200

@app.route("/api/tops/", methods=['POST'])
def post_tops():
    body = json.loads(request.data)
    image_data = body.get("image_data", False)
    if not image_data:
        return json.dumps({"error": "Invalid fields"}), 400
    else:
        new_top = Clothes(image_data=image_data, top=True)
        db.session.add(new_top)
        db.session.commit()
        return json.dumps(new_top.serialize()), 201

@app.route("/api/tops/<int:id>/")
def get_top_id(id):
    top = Clothes.query.filter_by(id=id).first()
    if top is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps(top.serialize()), 200

@app.route("/api/tops/<int:id>/", methods=['DELETE'])
def del_top_id(id):
    top = Clothes.query.filter_by(id=id).first()
    if top is None:
        return json.dumps({"error": "Invalid fields"}), 400
    db.session.delete(top)
    db.session.commit()
    return json.dumps(top.serialize()), 200

#BOTTOMS
@app.route("/api/bottoms/")
def get_bottoms():
    return json.dumps({"bottoms": [b.serialize() for b in Clothes.query.filter_by(top=False)]}), 200

@app.route("/api/bottoms/", methods=['POST'])
def post_bottoms():
    body = json.loads(request.data)
    image_data = body.get("image_data", False)
    if not image_data:
        return json.dumps({"error": "Invalid fields"}), 400
    else:
        new_bottom = Clothes(image_data=image_data, top=False)
        db.session.add(new_bottom)
        db.session.commit()
        return json.dumps(new_bottom.serialize()), 201

@app.route("/api/bottoms/<int:id>/")
def get_bottom_id(id):
    bottom = Clothes.query.filter_by(id=id).first()
    if bottom is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps(bottom.serialize()), 200

@app.route("/api/bottoms/<int:id>/", methods=['DELETE'])
def del_bottoms_id(id):
    bottom = Clothes.query.filter_by(id=id).first()
    if bottom is None:
        return json.dumps({"error": "Invalid fields"}), 400
    db.session.delete(bottom)
    db.session.commit()
    return json.dumps(bottom.serialize()), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
