from flask import session
from flask_socketio import join_room, leave_room, send, emit
from TeamMatcher import socketio
from TeamMatcher.message.message import Message
from TeamMatcher.message.room import Room


@socketio.on('connect')
def handle_connect():
    """
    On connect we will join all rooms in the server that this client belongs to
    :return:
    """

    if 'username' in session:
        username = session['username']
        rooms = Room.get_all_rooms(username)
        for room in rooms:
            join_room(str(room))


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

    data = {"user": username, "text": text}
    emit('chat_message', args=data, room=target_room, include_self=False)

