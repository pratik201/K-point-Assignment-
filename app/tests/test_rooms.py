import unittest
from app import app, db
from app.models import Room

class RoomTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_room(self):
        response = self.app.post('/rooms', json={
            'room_name': 'Conference Room A',
            'capacity': 10
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Room created successfully', response.data)

        with app.app_context():
            room = Room.query.filter_by(room_name='Conference Room A').first()
            self.assertIsNotNone(room)
            self.assertEqual(room.capacity, 10)

if __name__ == '__main__':
    unittest.main()
