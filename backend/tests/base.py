from flask_testing import TestCase
import sys
sys.path.append('../src')

# App imports
from app import app, db
from kickerapp.slack_sync import sync_new_and_left_channel_members


class KickerTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    @classmethod
    def fixtures(cls):
        pass

    @classmethod
    def setUpClass(cls):
        super(KickerTest, cls).setUpClass()
        db.drop_all()
        db.create_all()
        cls.fixtures()

    @classmethod
    def tearDownClass(cls):
        super(KickerTest, cls).tearDownClass()
        db.session.remove()


class KickerTestWithFixtures(KickerTest):
    @classmethod
    def fixtures(cls):
        # Run Slack Sync to populate database with players
        sync_new_and_left_channel_members()
