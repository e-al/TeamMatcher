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
            SELECT Name, Description, Max_Capacity, Status
             FROM Project
        """)

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        res = []

        for tup in tups:
            res.append({'name': tup[0],
                        'desc': tup[1],
                        'max_cap': tup[2],
                        'status': tup[3]})

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
        res = []

        for tup in tups:
            res.append({'name': tup[0],
                        'desc': tup[1],
                        'max_cap': tup[2],
                        'status': tup[3],
                        'id': tup[4]})

        return res

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
