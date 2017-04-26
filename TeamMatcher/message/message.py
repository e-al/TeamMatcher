from TeamMatcher import mysql
import datetime

class Message(object):
    """This is the proxy class to work with message relations"""

    @staticmethod
    def send(sender_username, recv_room_id, text):
        """ This function 'sends' the message to the room by permanently
        storing it in the DB.

        Additionally, it updates the last read message from the corresponding
        room
        """

        db = mysql.get_db()
        cur = db.cursor()

        now = datetime.datetime.now()
        cur.execute("""
            INSERT INTO Message (
                Sender_Id,
                Recv_Room_Id,
                Text,
                Ts
            )
            VALUES ((SELECT Student_Id FROM Student WHERE Email=%s), %s, %s, %s)
        """, (sender_username, recv_room_id, text, now))


        last_msg_id = cur.lastrowid

        cur.execute("""
            INSERT INTO LastReadMessage (
                Student_Id,
                Room_Id,
                Last_Msg_Id,
                Last_Read_Msg_Id
            )
            VALUES ((SELECT Student_Id FROM Student WHERE Email=%s), %s, %s, %s)
            ON DUPLICATE KEY UPDATE Last_Msg_Id = %s, Last_Read_Msg_Id = %s
        """, (sender_username, recv_room_id, last_msg_id, last_msg_id,
              last_msg_id, last_msg_id))

        cur.execute("""Select Student_Id FROM RoomMember WHERE Room_Id = %s""", (recv_room_id,))

        members = cur.fetchall()

        for member in members:
            cur.execute("""
                INSERT INTO LastReadMessage (
                    Student_Id,
                    Room_Id,
                    Last_Msg_Id,
                    Last_Read_Msg_Id
                )
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE Last_Msg_Id = %s
            """, (member, recv_room_id, last_msg_id,
                  last_msg_id, last_msg_id))

        db.commit()

    @staticmethod
    def mark_message_read(msg_id, room_id, username):
        """
        Marks `msg_id` as last read message by `username` in the room `room_id`

        :param msg_id: the message id to mark as read
        :param room_id: the room id to which this message belongs
        :param username: the username that read the message
        :return:
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            UPDATE LastReadMessage
            SET Last_Read_Msg_Id = %s, Last_Msg_Id = %s
            WHERE Student_Id=(SELECT Student_Id FROM Student WHERE Email=%s)
            AND Room_Id = %s
        """, (msg_id, msg_id, username, room_id,))

        db.commit()



    @staticmethod
    def get_history_for_room(room_id, limit):
        """
        This function returns history messages from a specified room

        :param room_id: room from which to retrieve the history
        :param limit: truncate the history to this value
        :return: a list of dictionaries containing message text, sender email
            and ts
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT S.Email, Text, Ts, M.Id
             FROM Message M INNER JOIN Student S
             ON M.Sender_Id = S.Student_Id
             WHERE M.Recv_Room_Id = %s
             ORDER BY Ts
             LIMIT %s
        """, (room_id, limit))

        tups = cur.fetchall()

        return [
            {'user': tup[0],
             'text': tup[1],
             'ts': tup[2],
             'id': tup[3]}
            for tup in tups
        ]


    @staticmethod
    def get_all_unread(username):
        """
        Returns a list of dictionaries that contain rooms with unread
            messages
        :param username: email of the student
        :return: True if there are any unread messages in the rooms `username`
            is in, False otherwise
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Room_Id, Last_Msg_Id
             FROM LastReadMessage
             WHERE Last_Msg_Id <> Last_Read_Msg_Id
             AND Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s)
        """, (username,))

        tups = cur.fetchall()

        return [
            {'room_id': tup[0],
             'msg_id': tup[1]}
            for tup in tups
        ]



