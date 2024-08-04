import unittest
from pass_app import app

class PassAppTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Clean up actions if needed (not required for this simple example)
        pass

    def test_get_passwords(self):
        # Test the /password/ route
        response = self.app.get('/password/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'example.com', response.data)
        self.assertIn(b'github.com', response.data)
        self.assertIn(b'email.com', response.data)
        
    def test_get_password_valid_id(self):
        # Test the /password/1 route for a valid ID
        response = self.app.get('/password/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'example.com', response.data)
        self.assertIn(b'password123', response.data)
        
    def test_get_password_invalid_id(self):
        # Test the /password/999 route for an invalid ID
        response = self.app.get('/password/999/')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Password not found', response.data)
        
if __name__ == '__main__':
    unittest.main()