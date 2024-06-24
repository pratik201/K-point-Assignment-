import unittest
from app import app, db
from app.models import User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.app.post('/users', json={
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

        with app.app_context():
            user = User.query.filter_by(email='john@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'John Doe')

if __name__ == '__main__':
    unittest.main()
