import face_recognition.api as api
from .db import db
from .models import FaceEncoding, Player

from flask_restful import Resource, reqparse
from sqlalchemy import func
import werkzeug
from uuid import uuid4
import os
import tempfile
import numpy as np
from PIL import Image
import base64
import io


def save_file(image):
    generated_uuid = uuid4().hex

    temp_dir = tempfile.gettempdir()

    filename = os.path.join(temp_dir, generated_uuid)
    image.save(filename)

    return filename


class FaceRecognitionResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=werkzeug.FileStorage, location='files')

        args = parser.parse_args()

        if args['image'] is None:
            return "No image specified", 400

        filename = save_file(args['image'])

        recognized_faces = recognize_faces(filename)
        os.remove(filename)

        return {
            "outputs": recognized_faces,
        }


class AddFacesResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=werkzeug.FileStorage, location='files')
        parser.add_argument('usernames', type=str)

        args = parser.parse_args()

        if args['image'] is None:
            return "No image specified", 400

        if args['username'] is None or args['username'] == "":
            return "No user specified", 400

        user = Player.query.filter(func.lower(Player.slack_username) == func.lower(args['username'])).first()

        if user is None:
            return "User {} does not exist".format(args['username']), 200

        filename = save_file(args['image'])
        insert_new_face(filename, user.slack_id)

        return "OK", 200


def recognize_faces(face_image_path):
    # Read image from disk
    image = api.load_image_file(face_image_path)

    # Get face locations in image
    face_locations = api.face_locations(image)

    # Create encodings from image
    face_encodings = api.face_encodings(image, known_face_locations=face_locations)

    # Get encodings from DB
    existing_face_encoding_objects = FaceEncoding.query.all()
    existing_face_encodings = np.array([fe.encoding for fe in existing_face_encoding_objects])

    outputs = []

    # Loop through detected faces
    for i, face_encoding in enumerate(face_encodings):
        face_matches = api.compare_faces(existing_face_encodings, face_encoding)
        recognized_player = None

        if any(face_matches):
            # Face matched to existing face
            ix = face_matches.index(True)
            recognized_player = existing_face_encoding_objects[ix].player

        # Face found, but could not be matched
        top, right, bottom, left = face_locations[i]

        image_crop = image[top:bottom, left:right]

        im = Image.fromarray(image_crop)
        with io.BytesIO() as output:
            im.save(output, format="JPEG")
            contents = output.getvalue()

        outputs.append(
            {
                "image": base64.b64encode(contents).decode("utf-8"),
                "embedding": face_encoding.tolist(),
                "player": recognized_player.serialize() if recognized_player else None
            })

    return outputs


def insert_new_face(face_image_path, user_id):
    image_encoding = api.face_encodings(api.load_image_file(face_image_path))
    face_encoding = FaceEncoding(player_id=user_id, encoding=image_encoding[0])

    db.session.add(face_encoding)
    db.session.commit()
