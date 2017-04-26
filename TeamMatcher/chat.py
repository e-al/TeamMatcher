from flask import session
from flask_socketio import join_room, leave_room, send, emit
from TeamMatcher import socketio
from TeamMatcher.message.message import Message
from TeamMatcher.message.room import Room
import json


@socketio.on('connect')
def handle_connect():
    """
    On connect we will join all rooms in the server that this client belongs to
    :return:
    """

    if 'username' in session:
        username = session['username']
        rooms = Room.get_all_rooms(username)
        print("Trying to join rooms")
        print(rooms)
        for room in rooms:
            join_room(str(room['id']))


@socketio.on('disconnect')
def handle_disconnect():
    """
    On disconnect just leave all the rooms
    :return:
    """
    if 'username' in session:
        username = session['username']
        rooms = Room.get_all_rooms(username)
        for room in rooms:
            leave_room(str(room))


@socketio.on('chat_message')
def handle_chat_message_send(username, target_room, text):
    """
    Send a message to a room and store it in the database
    :param username:
    :param target_room:
    :param text:
    :return:
    """
    Message.send(username, int(target_room), text)

    data = {"user": username, "text": text, "room_id": target_room}
    print("sending to the room %s" % str(target_room))
    # emit('chat_message', args=data, room=str(target_room), include_self=True)
    print(json.dumps(data))
    send(json.dumps(data), room=str(target_room), include_self=False)

