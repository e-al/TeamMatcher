from TeamMatcher import mysql

class Team(object):
    """Proxy class to work with Team relation"""
    def __init__(self):
        pass


    @staticmethod
    def get_all():
        """Retrieve all teams from the database

        :returns A list of dictionaries containing teams descriptions
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Team_Id, Name
            FROM Team
        """)

        #TODO: this is not good if we have a lot of teams, change to range
        tups = cur.fetchall()
        res = []

        for tup in tups:
            res.append({'id': tup[0],
                        'name': tup[1]})

        return res

    @staticmethod
    def get_for_student(username):
        """Retrieve all teams where `username` is participating or created

        :param username Student email to identify teams he/she is a part of
        :returns A list of dictionaries containing teams descriptions
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Team_Id, Name, Student_Owns
            FROM Team T INNER JOIN StudentPartOfTeam SP
            ON T.Team_Id = SP.Team_Id
            WHERE SP.Student_Id =
                (SELECT Student_Id FROM Student WHERE Email = %s)
        """, (username,))

        #TODO: this is not good if we have a lot of teams, change to range
        tups = cur.fetchall()
        res = []

        for tup in tups:
            res.append({'id': tup[0],
                        'name': tup[1],
                        'owner': tup[2]})

        return res

    @staticmethod
    def get_owned_by_student(username):
        """Retrieve all teams that `username` owns

        :param username Student email to identify teams he/she owns
        :returns A list of dictionaries containing teams descriptions
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Team_Id, Name
            FROM Team T INNER JOIN StudentPartOfTeam SP
            ON T.Team_Id = SP.Team_Id
            WHERE SP.Student_Id =
                (SELECT Student_Id FROM Student WHERE Email = %s)
            AND SP.Student_Owns = TRUE
        """, (username,))

        #TODO: this is not good if we have a lot of teams, change to range
        tups = cur.fetchall()
        res = []

        for tup in tups:
            res.append({'id': tup[0],
                        'name': tup[1])

        return res

    @staticmethod
    def add(username, **kwargs): # we should add team later
        """This method adds new team in the the DB

        :param username email of the student that is creating/owning the team
        :param kwargs A dictionary with a team description
        :returns Numeric id of the created team
        """

        kw = kwargs
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO Team(
                Name,
                Student_Owns
            )
            VALUES(%s, %s, (SELECT Student_Id FROM Student WHERE Email=%s))
        """, (kw.get('name', ''),
              'TRUE',
              username))

        db.commit()

        return cur.lastrowid

    @staticmethod
    def update_info(**kwargs):
        """Updates the team info. To add/remove students and transfer owndership
        use add_student, remove_student and transfer_ownership

        :param kwargs A dictionary with a team description and an id
        :except Throws RuntimeError if 'id' is not in kwargs
        :returns A dictionary with updated team description
        """

        if not 'id' in kwargs:
            raise RuntimeError('Id for the team is not set')

        kw = kwargs
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            UPDATE Team
            SET Name=%s,
            WHERE Team_Id=%s
        """, (kw.get('name', ''),
              kw.get('id')))

        db.commit()
        return kw

    @staticmethod
    def remove(team_id):
        """Removes the team from the database

        :param team_id Numeric id of the team to remove
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            DELETE FROM Team
            WHERE Team_Id = %s
        """, (team_id,))

        #TODO: make sure we remove all references to this team as well
        db.commit()

    @staticmethod
    def add_student(username, team_id):
        """Adds student with username to team team_id

        :param username: username of the student to add to a team
        :param team_id: team id to which to add a student
        :return:
        """
        #TODO: think about how to return failure

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO StudentPartOfTeam(
                Student_Id,
                Team_Id
            )
            VALUES((SELECT Student_Id FROM Student WHERE Email = %s), %s)
        """, (username, team_id))

        db.commit()


    @staticmethod
    def remove_student(username, team_id):
        """Removes student with username from the team team_id

        :param username: username of the student to remove from a team
        :param team_id: team id from which to remove a student
        :return:
        """

        #TODO: think about how to return failure

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            DELETE FROM StudentPartOfTeam(
                Student_Id,
                Team_Id
            )
            WHERE Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s)
            AND Team_Id = %s
        """, (username, team_id))


    @staticmethod
    def transfer_ownership(new_owner, team_id):
        """Transfers ownership of a team to a new student

        :param new_owner: username of a student to which to transfer the
            ownership
        :param team_id: the id of the team ownership of which to be transfered
        :return:
        """

        #TODO: think about how to return failure

        db = mysql.get_db()
        cur = db.cursor()

        # take away ownernship from previous owner
        cur.execute("""
            UPDATE StudentPartOfTeam
            SET Student_Owns=FALSE,
            WHERE Team_Id=%s
            AND Student_Id=(SELECT Student_Id
                            FROM StudentPartOfTeam
                            WHERE Team_Id=%s AND Student_Owns=TRUE)
        """, (team_id, team_id))

        cur.execute("""
            UPDATE StudentPartOfTeam
            SET Student_Owns=TRUE,
            WHERE Team_Id=%s
            AND Student_Id=(SELECT Student_Id FROM Student WHERE Email=%s)
        """, (team_id, new_owner))

        db.commit()

    @staticmethod
    def get_participants(team_id):
        """Get all teammates of a specified team

        :param team_id: id of the team to get all the teammates
        :return: a list of dictionaries that describe participants
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Student_Id, Name, Email, School, Year, Major, GPA
            FROM StudentPartOfTeam SP INNER JOIN Student S
            ON SP.Student_Id = S.Student_Id
            WHERE SP.Team_Id = %s
        """, (team_id,))

        tups = cur.fetchall()

        return [
            {'name': tup[0],
             'email': tup[1],
             'school': tup[2],
             'year': tup[3],
             'major': tup[4],
             'gpa': tup[5]}
            for tup in tups
        ]


    @staticmethod
    def assign_project(team_id, project_id):
        """Assigns a project that this team manages

        Same team can manage several projects, but no project can be managed by
        several teams.

        However, this method won't check if the project is already managed by
        a team, and therefore this should be checked somewhere else

        :param team_id: id of the team to manage the project
        :param project_id: id of the project to be managed

        """
        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            UPDATE
            FROM StudentPartOfTeam SP INNER JOIN Student S
            ON SP.Student_Id = S.Student_Id
            WHERE SP.Team_Id = %s
        """, (team_id,))

        tups = cur.fetchall()

        return [
            {'name': tup[0],
             'email': tup[1],
             'school': tup[2],
             'year': tup[3],
             'major': tup[4],
             'gpa': tup[5]}
            for tup in tups
        ]








