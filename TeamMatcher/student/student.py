from TeamMatcher import mysql
class Student(object):
    """This is the proxy class to work with student relation"""

    def __init__(self):
        pass


    @staticmethod
    def verify(username, password):
        """ This method verifies if the student is registered and
            the password matches """

        cur = mysql.get_db().cursor()
        cur.execute("""SELECT * from Student WHERE email = %s
                       AND passwd = %s""", (username, password))
        if cur.fetchone():
            return True

        return False

    @staticmethod
    def exists(username):
        """This method verifies if the student exists in the database"""

        cur = mysql.get_db().cursor()
        cur.execute("""SELECT * from Student WHERE email = %s""", (username,))
        if cur.fetchone():
            return True

        return False

    @staticmethod
    def add(username, password):
        """This method inserts the new user (student) in the the DB"""

        if Student.exists(username):
            # this should never happen, just making code bullet-proof
            raise RuntimeError('User with this email exists')
        db = mysql.get_db()
        cur = db.cursor()
        cur.execute("""INSERT INTO Student(email, password) VALUES(%s, %s)""",
                    (username, password))

        db.commit()

