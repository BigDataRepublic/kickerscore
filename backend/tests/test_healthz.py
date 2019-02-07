from base import KickerTest


class TestHealthz(KickerTest):
    def test_healthz_endpoint(self):
        response = self.client.get("/healthz")

        assert response.status_code == 200
