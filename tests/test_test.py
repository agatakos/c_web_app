import unittest
import os
import json
from app import create_app, db

class POlicyDataTestCase(unittest.TestCase):
    """This class represents the policies test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.policy = {'id': 'pol_000000C6XrazMarHjzKN1izjhrnN16'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_api_can_get_all_policy_data(self):
        """Test API can get a bucketlist (GET request)."""
        res = self.client().post('/policies/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/policies/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('pol_000000C6XrazMarHjzKN1izjhrnN16', str(res.data))

    def test_api_can_get_policy_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        rv = self.client().post('/policies/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/policies/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Borabora', str(result.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()