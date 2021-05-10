import unittest
import os
import json
from app import create_app, db


class PolicyDataTestCase(unittest.TestCase):
    """This class represents the policies test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.policy = {"id": "pol_000000C6XrazMarHjzKN1izjhrnN16"}

        with self.app.app_context():
            db.create_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
