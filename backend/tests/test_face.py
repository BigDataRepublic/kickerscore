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

    def test_add_face(self):
        # Test empty embeddings and usernames lists
        response = self.client.post("/kickerscore/api/v2/add-faces", data={
            "embeddings": [],
            "usernames": []
        })

        # Should return 400 status code
        assert response.status_code == 400

        # Test single embedding and username
        response = self.client.post("/kickerscore/api/v2/add-faces", data={
            "embeddings": [np.random.rand(128).tolist()],
            "usernames": ["steven"]
        })

        # Should return 400 status code
        assert response.status_code == 200

        # Should be one element in database
        assert FaceEmbedding.query.count() == 1
