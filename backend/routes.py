from . import app
import os
import json
from flask import jsonify, request

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """Return the length of data."""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Fetch and return all pictures."""
    if data:
        return jsonify(data), 200
    return {"message": "No pictures found"}, 404

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Retrieve a picture by ID."""
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture."""
    new_picture = request.get_json()
    
    if not new_picture or "id" not in new_picture:
        return {"message": "Bad request. 'id' is required."}, 400

    # Check for duplicate
    if any(picture["id"] == new_picture["id"] for picture in data):
        return {"message": "Picture with this ID already exists"}, 409

    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update a picture by ID."""
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    updated_data = request.get_json()
    if not updated_data:
        return {"message": "Bad request. Data is required"}, 400

    picture.update(updated_data)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Remove a picture by ID."""
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    data.remove(picture)
    return {"message": "Picture deleted successfully"}, 200

######################################################################
# CLEAR ALL PICTURES
######################################################################
@app.route("/picture/clear", methods=["DELETE"])
def clear_pictures():
    """Clear all pictures."""
    global data
    data.clear()
    return {"message": "All pictures cleared"}, 200