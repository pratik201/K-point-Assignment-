from flask import request, jsonify
from app import app, db
from app.models import User, Room, Meeting, Participant
from datetime import datetime

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(user_list), 200

@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    new_room = Room(room_name=data['room_name'], capacity=data['capacity'])
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room created successfully'}), 201

@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    room_list = [{'id': room.room_id, 'room_name': room.room_name, 'capacity': room.capacity} for room in rooms]
    return jsonify(room_list), 200


@app.route('/meetings', methods=['POST'])
def create_meeting():
    data = request.json
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')

    # Check for room availability
    room_conflict = Meeting.query.filter(
        Meeting.room_id == data['room_id'],
        Meeting.start_time < end_time,
        Meeting.end_time > start_time
    ).first()
    if room_conflict:
        return jsonify({'message': 'Room is not available at the requested time'}), 409

    # Check for participant availability
    for user_id in data['participants']:
        participant_conflict = Meeting.query.join(Participant).filter(
            Participant.user_id == user_id,
            Meeting.start_time < end_time,
            Meeting.end_time > start_time
        ).first()
        if participant_conflict:
            return jsonify({'message': f'User {user_id} is not available at the requested time'}), 409

    new_meeting = Meeting(
        title=data['title'],
        description=data.get('description'),
        start_time=start_time,
        end_time=end_time,
        room_id=data['room_id'],
        created_by=data['created_by']
    )
    db.session.add(new_meeting)
    db.session.commit()

    for user_id in data['participants']:
        participant = Participant(meeting_id=new_meeting.meeting_id, user_id=user_id)
        db.session.add(participant)

    db.session.commit()
    return jsonify({'message': 'Meeting created successfully'}), 201

@app.route('/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    all_meetings = []
    for meeting in meetings:
        participants = Participant.query.filter_by(meeting_id=meeting.meeting_id).all()
        participant_list = [{'participant_id': participant.participant_id, 'user_id': participant.user_id} for participant in participants]
        meeting_data = {
            'meeting_id': meeting.meeting_id,
            'title': meeting.title,
            'description': meeting.description,
            'start_time': meeting.start_time,
            'end_time': meeting.end_time,
            'room_id': meeting.room_id,
            'created_by': meeting.created_by,
            'participants': participant_list
        }
        all_meetings.append(meeting_data)
    return jsonify(all_meetings)

