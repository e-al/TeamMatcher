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
    def update_info(**kwargs):
        """This method updates student info in the DB"""

        kw = kwargs
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            UPDATE Student
            SET Name=%s, GPA=%s, School=%s, Major=%s, Year=%s
        """, (kw['name'],
              kw['gpa'],
              kw['school'],
              kw['major'],
              kw['year']))

        db.commit()

    @staticmethod
    def retrieve_info(username):
        """This method retrieves the info about the student in the DB
        It returns the dictionary containing the fields of Student class
        """

        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT (Name, GPA, School, Major, Year) FROM Student
            WHERE Email=%s
        """, (username,))

        tup = cur.fetchone()
        res = dict()
        res['name'] = tup[0]
        res['gpa'] = tup[1]
        res['school'] = tup[2]
        res['major'] = tup[3]
        res['year'] = tup[4]

        return res

    @staticmethod
    def update_skill(username, skill, level):
        pass

    @staticmethod
    def remove_skill(username, skill):
        pass

    @staticmethod
    def add_skill(username, skill, level):
        pass



