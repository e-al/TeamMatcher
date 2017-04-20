from TeamMatcher import mysql

class Project(object):
    """This is the proxy class to work with student relation"""

    def __init__(self):
        pass

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
        """Retrieve projects created by student

        :param username Student email whose projects will be retrieved
        :returns A list of dictionaries describing project properties
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
        res = []

        for tup in tups:
            res.append({'name': tup[0],
                        'desc': tup[1],
                        'max_cap': tup[2],
                        'status': tup[3],
                        'id': tup[4]})

        return res

    @staticmethod
    def get_id(id):
        """Retrieve projects created by student

        :param username Student email whose projects will be retrieved
        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
             FROM Project
             WHERE Project_Id = %s
        """, (id,))

        #TODO: this is not good if we have a lot of projects, change to range
        tup = cur.fetchone()
        if tup is None:
            return
        res = dict()
        res['name'] = tup[0]
        res['desc'] = tup[1]
        res['max_cap'] = tup[2]
        res['status'] = tup[3]
        res['id'] = tup[4]

        return res
    @staticmethod
    def get_participant_id(id):
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, GPA, School, Major, Year, Email
             FROM Student
             WHERE Student_Id in (SELECT Student_Id FROM StudentPartOfProject WHERE Project_Id = %s)
        """, (id,))

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
            return
        return [
           {'name' : tup[0],
            'gpa' : tup[1],
            'school' : tup[2],
            'major' : tup[3],
            'year' : tup[4],
            'email' : tup[5]}
            for tup in tups
        ]

    @staticmethod
    def get_for_student_no_team(username):
        """

        :param username: Student email whose projects will be retrieved
        :return: A List of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, Description, Max_Capacity, Status, Project_Id
             FROM Project
             WHERE CreatedByStudentId =
                 (SELECT Student_Id FROM Student WHERE Email = %s)
             AND Team_Id = NULL
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

    @staticmethod
    def add(username, **kwargs): # we should add team later
        """This method adds new project in the the DB

        :param username email of the student that is creating the project
        :param kwargs A dictionary with a project description
        :returns Numeric id of the inserted project
        """

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
        cur.execute("""SELECT MAX(Project_Id) From Project""")
        tup = cur.fetchone()
        cur.execute("""
            INSERT INTO StudentPartOfProject(Student_Id, Project_Id, Student_Owns)
            VALUES((SELECT Student_Id FROM Student WHERE Email=%s), %s, TRUE)
        """, (username, tup))


        db.commit()

        return cur.lastrowid

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

        #TODO: make sure we remove all references to this project as well
        db.commit()

    @staticmethod
    def addPersonToProject(project_id, person_id):

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO StudentPartOfProject(Student_Id, Project_Id, Student_Owns)
            VALUES(%s, %s, FALSE)
        """, (person_id, project_id,))
        db.commit()
