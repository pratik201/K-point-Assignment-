from app.models import Meeting

def is_collision(new_start_time, new_end_time, room_id):
    meetings = Meeting.query.filter_by(room_id=room_id).all()
    for meeting in meetings:
        if not (new_end_time <= meeting.start_time or new_start_time >= meeting.end_time):
            return True
    return False
