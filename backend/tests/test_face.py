from datetime import datetime
import sys
sys.path.append('../src')

from base import KickerTest, KickerTestWithFixtures
from kickerapp.config import *
from kickerapp.models import FaceEncoding
import base64
import io
from PIL import Image
import numpy as np
from app import db


class TestFace(KickerTestWithFixtures):
    """
    Tests /add-faces and /recognize-faces endpoints.
    Also tests the Slack integration since it's used as a fixture.
    """
    def test_recognize_face(self):
        # Load example face
        with open("lena.png", 'rb') as f:
            b64_encoded_lena = base64.b64encode(f.read()).decode("utf-8")

        response = self.client.post("/kickerscore/api/v2/recognize-faces", data={"image": b64_encoded_lena})

        # Should return 200 status code
        assert response.status_code == 200

        # Should detect one face
        assert len(response.json["outputs"]) == 1

        # Should detect no known player (Lena doesn't play foosball)
        assert response.json["outputs"][0]["player"] is None

        # Embedding should be present and length should be 128 floats
        a = response
        assert len(a.json["outputs"][0]["embedding"]) == 128

        # Output image crop should be base64 decodable image
        with io.BytesIO() as f:
            f.write(base64.b64decode(response.json["outputs"][0]["image"]))
            Image.open(f)

    def test_add_face_empty_data(self):
        # Clear table
        FaceEncoding.query.delete()
        db.session.commit()

        # Test empty embeddings and usernames lists
        response = self.client.post("/kickerscore/api/v2/add-faces", json={
            "embeddings": [],
            "usernames": []
        })

        # Should return 400 status code
        assert response.status_code == 400
        assert FaceEncoding.query.count() == 0

    def test_add_face(self):
        # Clear table
        FaceEncoding.query.delete()
        db.session.commit()

        # Test single embedding and username
        username = "steven"
        random_embedding = np.random.rand(128).tolist()
        response = self.client.post("/kickerscore/api/v2/add-faces", json={
            "embeddings": [random_embedding],
            "usernames": [username]
        })

        # Should return 400 status code
        assert response.status_code == 200

        # Should be one element in database and match request data
        assert FaceEncoding.query.count() == 1
        assert np.allclose(np.array(FaceEncoding.query.first().encoding), np.array(random_embedding))
        assert FaceEncoding.query.first().player.slack_username == username

    def test_add_face_nonexisting_user(self):
        # Clear table
        FaceEncoding.query.delete()
        db.session.commit()

        username = "nonexistinguser"
        random_embedding = np.random.rand(128).tolist()
        response = self.client.post("/kickerscore/api/v2/add-faces", json={
            "embeddings": [random_embedding],
            "usernames": [username]
        })

        # Should return 400 status code
        assert response.status_code == 400

        # Should be nothing in database
        assert FaceEncoding.query.count() == 0
