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
from itertools import groupby
from operator import attrgetter


THRESHOLD = 0.6


def save_file(image):
    generated_uuid = uuid4().hex

    temp_dir = tempfile.gettempdir()

    filename = os.path.join(temp_dir, generated_uuid)

    with open(filename, 'wb') as f:
        f.write(image)

    return filename


class FaceRecognitionResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=str)

        args = parser.parse_args()

        if args['image'] is None:
            return "No image specified", 400

        decoded = base64.b64decode(args['image'])
        filename = save_file(decoded)

        recognized_faces = recognize_faces(filename)
        os.remove(filename)

        return {
            "outputs": recognized_faces,
        }


class AddFacesResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('embeddings', type=list, location='json', action='append')
        parser.add_argument('usernames', type=str, location='json', action='append')

        args = parser.parse_args()

        if args['embeddings'] is None or len(args['embeddings']) == 0:
            return "No embeddings specified", 400

        if args['usernames'] is None or len(args['usernames']) == 0:
            return "No users specified", 400

        if len(args['embeddings']) != len(args['usernames']):
            return "Embeddings and usernames should be of the same size, {} != {}".format(
                len(args['embeddings']),
                len(args['usernames'])), 200

        for user, embedding in zip(args['usernames'], args['embeddings']):
            user = Player.query.filter(func.lower(Player.slack_username) == func.lower(user)).first()

            if user is None:
                db.session.rollback()
                return "User {} does not exist".format(user), 400

            face_encoding = FaceEncoding(player_id=user.slack_id, encoding=embedding)
            db.session.add(face_encoding)

        db.session.commit()
        return "OK", 200


def recognize_faces(face_image_path):
    # Read image from disk
    image = api.load_image_file(face_image_path)

    # Get face locations in image
    face_locations = api.face_locations(image, model="hog")

    # Create encodings from image
    face_encodings = api.face_encodings(image, known_face_locations=face_locations)

    # Get encodings from DB
    existing_face_encoding_objects = [list(g) for _, g in groupby(FaceEncoding.query.order_by(FaceEncoding.player_id).all(), attrgetter('player_id'))]

    outputs = []

    for i, face_encoding in enumerate(face_encodings):
        distances = {}

        for face_encoding_group in existing_face_encoding_objects:
            # Calculate distance to every encoding for this group (person)
            existing_face_encodings = np.array([fe.encoding for fe in face_encoding_group])
            face_distances = api.face_distance(existing_face_encodings, face_encoding)

            distances[face_encoding_group[0].player] = sum(face_distances) / len(face_distances)

        recognized_player = None
        if len(distances) > 0:
            recognized_player = min(distances, key=distances.get)
            if distances[recognized_player] > THRESHOLD:
                recognized_player = None

        # Create a crop of the face
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
