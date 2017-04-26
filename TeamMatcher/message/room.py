from TeamMatcher import mysql
from TeamMatcher.project.project import Project

class Room(object):
    """This is the proxy class to work with rooms relations"""

    @staticmethod
    def add(name, members):
        """Creates a new room add optionally adds members to it"""

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO Room (
                Name
            )
            VALUES (%s)
        """, (name,))

        db.commit()
        room_id = cur.lastrowid

        Room.add_members(room_id, members)

        return room_id

    @staticmethod
    def add_members(room_id, members):
        if len(members):
            db = mysql.get_db()
            cur = db.cursor()

            for member in members:
                cur.execute("""
                    INSERT INTO RoomMember (
                        Room_Id,
                        Student_Id
                    )
                    VALUES (%s, (SELECT Student_Id FROM Student WHERE Email=%s))
                """, (room_id, member,))

            db.commit()


    @staticmethod
    def create_project_room(project_id):
        """
        Creates a room for project conversation. Will add all current project
        participants into this room TODO: potentially could use triggers for
        that
        :param project_id: id of the project for which to create the room
        :return: created room it or None if error TODO: switch to exceptions
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Name FROM Project WHERE Project_Id = %s
        """, (project_id,))

        tup = cur.fetchone()
        if not tup:
            return None

        members = [
            info['email'] for info in Project.get_participants(project_id)
        ]

        room_id = Room.add(tup[0], members)

        cur.execute("""
            INSERT INTO RoomToProject (
                Room_Id,
                Project_Id
            )
            VALUES (%s, %s)
        """, (room_id, project_id))

        db.commit()

        return room_id


    @staticmethod
    def create_private_room(username_1, username_2):
        """
        Creates a room for private conversations between two users and adds them
        both into it

        :param username_1:
        :param username_2:
        :return: room id
        """

        room_id = Room.add(username_1 + username_2, [username_1, username_2])
        key = ''.join(sorted([username_1, username_2]))

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO PrivateRoom (
                Combined_Users_Key,
                Room_Id
            )
            VALUES (%s, %s)
        """, (key, room_id))

        db.commit()

        return room_id

    @staticmethod
    def _get_project_room(project_id):
        """
        Returns id of the room that is assigned to a project or None if
        one doesn't exist

        :param project_id:
        :return: id of the room, None if not found
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Room_Id
            FROM RoomToProject
            WHERE Project_Id = %s
        """, (project_id,))

        tup = cur.fetchone()
        if tup:
            return tup[0]
        else:
            return None

    @staticmethod
    def get_project_room(project_id):
        """
        Returns id of the room that is assigned to a project
        Creates one if doesn't exist

        :param project_id:
        :return: id of the room, None if not found
        """

        room_id = Room._get_project_room(project_id)
        if not room_id:
            room_id = Room.create_project_room(project_id)

        return room_id


    @staticmethod
    def _get_private_room(username_1, username_2):
        """
        Returns private room for two users or None if one doesn't exist
        :param username_1:
        :param username_2:
        :return:
        """
        db = mysql.get_db()
        cur = db.cursor()

        key = ''.join(sorted([username_1, username_2]))
        cur.execute("""
            SELECT Room_Id
            FROM PrivateRoom
            WHERE Combined_Users_Key = %s
        """, (key,))

        tup = cur.fetchone()
        if tup:
            return tup[0]
        else:
            return None

    @staticmethod
    def get_private_room(username_1, username_2):
        """
        Returns private room for two users, creates one if doesn't exist
        :param username_1: first user
        :param username_2: second user
        :return:
        """

        room_id = Room._get_private_room(username_1, username_2)
        if not room_id:
            room_id = Room.create_private_room(username_1, username_2)

        return room_id

    @staticmethod
    def get_all_rooms(username):
        """
        Returns all room ids a person belongs to
        :param username:
        :return:
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Room.Room_Id, Room.Name
            FROM RoomMember, Room
            WHERE Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s)
            AND RoomMember.Room_Id = Room.Room_Id
        """, (username,))

        tups = cur.fetchall()

        return [
            {
                "id": tup[0],
                "name": tup[1]}
            for tup in tups
        ]





