from TeamMatcher import mysql

class Project(object):
    """This is the proxy class to work with student relation"""

    def __init__(self):
        pass

    @staticmethod
    def get_info(project_id):
        """Retrieve the project with id `project_id`

        :param project_id Id from Projects relation
        :returns A dictionary with the description of a project with
            id = project_id
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
             FROM Project P
             WHERE P.Project_Id = %s
        """, (project_id,))

        tup = cur.fetchone()

        if not tup:
            return None

        return {'name': tup[0],
                'desc': tup[1],
                'max_cap': tup[2],
                'status': tup[3],
                'id': tup[4]}

    @staticmethod
    def get_all_Skills(id):
        """Retrieve all projects from the database

        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Skill_Id
            FROM Skill
            Where Skill_Id not in (Select Skill_Id from ProjectNeedsSkill where Project_id = %s)
        """, (id,))

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
            return
        res = []

        for tup in tups:
            res.append({'name': tup[0],
                        'id': tup[1]})

        return res

    @staticmethod
    def get_all_Proj_Skills():
        """Retrieve all projects from the database

        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT P.Name, S.Name
            FROM ProjectNeedsSkill T, Project P, Skill S
            Where P.Project_Id = T.Project_Id AND S.Skill_Id = T.Skill_Id
            Order By P.Name
        """)

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if not tups:
            return
        res = {}
        tres = []
        p = tups[0][0]
        for tup in tups:
            if(tup[0]==p):
                tres.append(tup[1])
            else:
                res.update({p: tres})
                tres = []
                p = tup[0]
                tres.append(tup[1])
        res.update({p: tres})
        return res

    @staticmethod
    def get_Skills(id):
        """Retrieve all projects from the database

        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Skill_Id
            FROM Skill
            Where Skill_Id in (Select Skill_Id from ProjectNeedsSkill where Project_id = %s)
        """, (id,))

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
            return
        res = []

        for tup in tups:
            res.append({'name': tup[0],
                        'id': tup[1]})

        return res


    @staticmethod
    def get_all():
        """Retrieve all projects from the database

        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
            FROM Project
        """)

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
            return
        res = []

        for tup in tups:
            res.append({'name': tup[0],
                        'desc': tup[1],
                        'max_cap': tup[2],
                        'status': tup[3],
                        'id':tup[4]})

        return res


    @staticmethod
    def get_for_student(username):
        """Retrieve projects `username` participates in

        :param username Student email whose projects will be retrieved
        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
             FROM Project
             WHERE Project_Id in (Select Project_Id FROM StudentPartOfProject WHERE Student_Id =
                 (SELECT Student_Id FROM Student WHERE Email=%s))
        """, (username,))

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()

        return [
            {'name': tup[0],
             'desc': tup[1],
             'max_cap': tup[2],
             'status': tup[3],
             'id': tup[4]}
            for tup in tups
        ]

    @staticmethod
    def get_created_by_student(username):
        """Retrieve all projects that `username` created

        :param username Student email to identify projects he/she created
        :returns A list of dictionaries containing projects descriptions
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
             FROM Project
             WHERE CreatedByStudentId =
                 (SELECT Student_Id FROM Student WHERE Email = %s)
        """, (username,))

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
            return

        return [
            {'name': tup[0],
             'desc': tup[1],
             'max_cap': tup[2],
             'status': tup[3],
             'id': tup[4]}
            for tup in tups
        ]


    def get_created_by_student_user(username, user):
        """Retrieve all projects that `username` created

        :param username Student email to identify projects he/she created
        :returns A list of dictionaries containing projects descriptions
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
             FROM Project
             WHERE CreatedByStudentId =
                 (SELECT Student_Id FROM Student WHERE Email = %s)
             AND Project_Id not in (Select Project_Id from StudentPartOfProject where Student_Id = (SELECT Student_Id FROM Student WHERE Email = %s))
        """, (username,user,))

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
            return

        return [
            {'name': tup[0],
             'desc': tup[1],
             'max_cap': tup[2],
             'status': tup[3],
             'id': tup[4]}
            for tup in tups
        ]


    @staticmethod
    def add(username, **kwargs): # we should add team later
        """This method adds new project in the the DB

        :param username email of the student that is creating the project
        :param kwargs A dictionary with a project description
        :returns Numeric id of the inserted project
        """

        print("Adding project for user %s" % username)
        print(kwargs)
        kw = kwargs
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO Project(
                Name,
                Description,
                Max_Capacity,
                Status,
                CreatedByStudentId
            )
            VALUES(%s, %s, %s, %s,
                (SELECT Student_Id FROM Student WHERE Email=%s))
        """, (kw.get('name', ''),
              kw.get('desc', ''),
              kw.get('max_cap', ''),
              kw.get('status', 'Created'),
              username))

        db.commit()
        project_id = cur.lastrowid

        cur.execute("""
            INSERT INTO StudentPartOfProject(
                Student_Id,
                Project_Id
            )
            VALUES ((SELECT Student_Id FROM Student WHERE Email=%s), %s)
        """, (username, project_id))

        db.commit()

        return project_id

    @staticmethod
    def createSkill(skill):

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO Skill(name)
            VALUES (%s)
        """, (skill,))
        db.commit()
        cur.execute("""SELECT MAX(Skill_Id) From Skill""")
        tup = cur.fetchone()
        return tup

    @staticmethod
    def update_info(**kwargs):
        """Updates the project info

        :param kwargs A dictionary with a project description and an id
        :except Throws RuntimeError if 'id' is not in kwargs
        :returns A dictionary with updated project description
        """

        if not 'id' in kwargs:
            raise RuntimeError('Id for the project is not set')

        kw = kwargs
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            UPDATE Project
            SET Name=%s,
                Description=%s,
                Max_Capacity=%s,
                Status=%s
            WHERE Project_Id=%s
        """, (kw.get('name', ''),
              kw.get('desc', ''),
              kw.get('max_cap', ''),
              kw.get('status', ''),
              kw.get('id')))

        db.commit()
        return kw

    @staticmethod
    def remove(project_id):
        """Removes the project from the database

        :param project_id Numeric id of the project to remove
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            DELETE FROM Project
            WHERE Project_Id = %s
        """, (project_id,))

        cur.execute("""
            DELETE FROM Project
            WHERE Project_Id = %s
        """, (project_id,))

        #TODO: make sure we remove all references to this project as well
        db.commit()

    @staticmethod
    def add_student(username, project_id):
        """Adds student with username to project `project_id`

        :param username: username of the student to add to a project
        :param project_id: project id to which to add a student
        :return:
        """
        #TODO: think about how to return failure

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO StudentPartOfProject(
                Student_Id,
                Project_Id
            )
            VALUES((SELECT Student_Id FROM Student WHERE Email = %s), %s)
        """, (username, project_id))

        db.commit()

    @staticmethod
    def addSkillToProject(project_id, skill_id):

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO ProjectNeedsSkill(Skill_Id, Project_Id)
            VALUES(%s, %s)
        """, (skill_id, project_id,))
        db.commit()

    @staticmethod
    def remove_student(username, project_id):
        """Removes student with username from the project project_id

        :param username: username of the student to remove from a project
        :param project_id: project id from which to remove a student
        :return:
        """

        #TODO: think about how to return failure

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            DELETE FROM StudentPartOfProject
            WHERE Student_Id = (SELECT Student_Id FROM Student WHERE Email = %s)
            AND Project_Id = %s
        """, (username, project_id))
        db.commit()


    @staticmethod
    def transfer_ownership(new_owner, project_id):
        """Transfers ownership of a project to a new student

        :param new_owner: username of a student to which to transfer the
            ownership
        :param project_id: the id of the project ownership of which to be
            transferred
        :return:
        """

        #TODO: think about how to return failure

        db = mysql.get_db()
        cur = db.cursor()

        # take away ownernship from previous owner
        cur.execute("""
            UPDATE Project
            SET CreatedByStudent=
                (SELECT Student_Id FROM Student WHERE Email=%s),
            WHERE Project_Id=%s
        """, (new_owner, project_id))


        db.commit()

    @staticmethod
    def removeSkillFromProject(project_id, skill_id):

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            DELETE FROM ProjectNeedsSkill
            WHERE Skill_Id = %s
            AND Project_Id = %s
        """, (skill_id, project_id,))
        db.commit()

    @staticmethod
    def get_participants(project_id):
        """Get all teammates of a specified project

        :param project_id: id of the project to get all the teammates
        :return: a list of dictionaries that describe participants
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Name, Email, School, Year, Major, GPA
            FROM StudentPartOfProject SP INNER JOIN Student S
            ON SP.Student_Id = S.Student_Id
            WHERE SP.Project_Id = %s
        """, (project_id,))

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
    def is_owner(username, project_id):
        """Checks if the student owns project `project_id`

        :param username:  student to check for the ownership
        :param project_id: project to check for the ownership
        :return: True if `username` owns `project_id`, False otherwise
        """

        db = mysql.get_db()
        cur = db.cursor()

        cur.execute("""
            SELECT Project_Id
            FROM Project
            WHERE Project_Id=%s AND CreatedByStudentId=(
                SELECT Student_Id FROM Student WHERE Email=%s
            )
        """, (project_id, username))

        return len(cur.fetchall())


