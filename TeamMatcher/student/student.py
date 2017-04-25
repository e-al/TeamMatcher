from TeamMatcher import mysql
class Student(object):
    """This is the proxy class to work with student relation"""

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        # must be present, maybe add error checking
        self.username = kwargs.get('username')
        # we do not return the password as the information
        self.gpa = int(kwargs.get('gpa', 0))
        self.school = kwargs.get('school', '')
        self.major = kwargs.get('major', '')
        self.year = kwargs.get('year', '')

    @staticmethod
    def verify(username, password):
        """ This method verifies if the student is registered and
            the password matches """

        cur = mysql.get_db().cursor()
        cur.execute("""
            SELECT * FROM Student
            WHERE Email = %s AND Password = %s
        """, (username, password))
        if cur.fetchone():
            return True

        return False

    @staticmethod
    def exists(username):
        """This method verifies if the student exists in the database"""

        cur = mysql.get_db().cursor()
        cur.execute("""
            SELECT * FROM Student
            WHERE Email = %s
        """, (username,))
        if cur.fetchone():
            return True

        return False

    @staticmethod
    def add(username, password, name):
        """This method inserts the new user (student) in the the DB"""

        if Student.exists(username):
            # this should never happen, just making code bullet-proof
            raise RuntimeError('User with this email exists')
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO Student(Email, Password, Name)
            VALUES(%s, %s, %s)
        """, (username, password, name))

        db.commit()

    @staticmethod
    def update_info(username, **kwargs):
        """This method updates student info in the DB

            :param username Username of student whose profile we want to update
            :param kwargs A dictionary with new profile info
            :returns A dictionary with new profile info
        """

        kw = kwargs
        db = mysql.get_db()
        cur = db.cursor()
        #TODO: add major later
        cur.execute("""
            UPDATE Student
            SET Name=%s, GPA=%s, School=%s, Year=%s
            WHERE Email=%s
        """, (kw['name'],
              kw['gpa'],
              kw['school'],
              kw['year'],
              username))

        db.commit()
        kw['email'] = username
        return kw

    @staticmethod
    def retrieve_info(username):
        """This method retrieves the info about the student in the DB
        It returns the dictionary containing the fields of Student class
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT Name, GPA, School, Major, Year, Email FROM Student
            WHERE Email=%s
        """, (username,))

        tup = cur.fetchone()
        res = dict()
        res['name'] = tup[0]
        res['gpa'] = tup[1]
        res['school'] = tup[2]
        res['major'] = tup[3]
        res['year'] = tup[4]
        res['email'] = tup[5]

        return res
    @staticmethod
    def retrieve_all_info():
       """This method retrieves the info about the student in the DB
       It returns the dictionary containing the fields of Student class
       """
       db = mysql.get_db()
       cur = db.cursor()
       cur.execute("""
           SELECT Name, GPA, School, Major, Year, Email FROM Student
       """)
       tups = cur.fetchall()
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
    def update_skill(username, skill, level):
       db = mysql.get_db()
       cur = db.cursor()
       cur.execute("""
           UPDATE StudentHasSkill
           SET Skill_Level = %s
           WHERE Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s) AND Skill_Id = %s
       """, (level,username,skill))
       cur.execute("""
           SELECT Student_Id FROM Student WHERE Email=%s
       """, (username,))
       db.commit()
       return cur.fetchone()


    @staticmethod
    def remove_skill(username, skill):
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            DELETE FROM StudentHasSkill
            WHERE Skill_Id = %s
            AND Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s)
        """, (skill, username,))
        db.commit()

    @staticmethod
    def add_skill(username, skill, level):
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO StudentHasSkill(Student_Id, Skill_Id, Skill_Level)
            VALUES ((SELECT Student_Id FROM Student WHERE Email=%s), %s, %s)
        """, (username, skill,level,))
        db.commit()

    @staticmethod
    def get_all_People_Skills():
        """Retrieve all projects from the database

        :returns A list of dictionaries describing project properties
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT P.Name, S.Name
            FROM StudentHasSkill T, Student P, Skill S
            Where P.Student_Id = T.Student_Id AND S.Skill_Id = T.Skill_Id
            Order By P.Name
        """)

        #TODO: this is not good if we have a lot of projects, change to range
        tups = cur.fetchall()
        if tups is None:
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
    def getSkills(username):
       db = mysql.get_db()
       cur = db.cursor()
       cur.execute("""
           SELECT S.Name, P.Skill_Level, P.Skill_Id
           FROM Skill S, StudentHasSkill P
           WHERE S.Skill_Id in (SELECT Skill_Id From StudentHasSkill where Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s))
           AND P.Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s)
           AND P.Skill_Id = S.Skill_Id
       """, (username,username,))
       tups = cur.fetchall()
       return [
           {'name' : tup[0],
            'level' : tup[1],
            'id' : tup[2]}
            for tup in tups
        ]

    @staticmethod
    def getAllSkills(username):
       db = mysql.get_db()
       cur = db.cursor()
       cur.execute("""
           SELECT Name, Skill_Id
           FROM Skill
           WHERE Skill_Id NOT in (SELECT Skill_Id From StudentHasSkill where Student_Id = (SELECT Student_Id FROM Student WHERE Email=%s))
       """, (username,))

       #TODO: this is not good if we have a lot of projects, change to range
       tups = cur.fetchall()
       if tups is None:
          return
       res = []

       for tup in tups:
          res.append({'name': tup[0],
                      'id': tup[1]})

       return res
