import unittest
from datetime import datetime
from app import app, db
from app.models import User, Room, Meeting, Participant

class MeetingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

            # Create a user and room for testing
            self.user = User(name='John Doe', email='john@example.com', password='password123')
            db.session.add(self.user)
            self.room = Room(room_name='Conference Room A', capacity=10)
            db.session.add(self.room)
            db.session.commit()
            
            # Reload the user and room instances to ensure they are bound to the session
            self.user = User.query.filter_by(email='john@example.com').first()
            self.room = Room.query.filter_by(room_name='Conference Room A').first()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_meeting(self):
        response = self.app.post('/meetings', json={
            'title': 'Team Meeting',
            'description': 'Discuss project updates',
            'start_time': '2023-06-15 10:00:00',
            'end_time': '2023-06-15 11:00:00',
            'room_id': self.room.room_id,
            'created_by': self.user.user_id,
            'participants': [self.user.user_id]
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Meeting created successfully', response.data)

        with app.app_context():
            meeting = Meeting.query.filter_by(title='Team Meeting').first()
            self.assertIsNotNone(meeting)
            self.assertEqual(meeting.description, 'Discuss project updates')

            participant = Participant.query.filter_by(meeting_id=meeting.meeting_id, user_id=self.user.user_id).first()
            self.assertIsNotNone(participant)

if __name__ == '__main__':
    unittest.main()
