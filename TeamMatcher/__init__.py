from flask import Flask
from flaskext.mysql import MySQL
from flask_socketio import SocketIO
import TeamMatcher.default_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(TeamMatcher.default_config)
app.config.from_pyfile('teammatcher_config.py', silent=True)

# this thing is blatantly copied directly from the tutorial, such security
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

mysql = MySQL()
mysql.init_app(app)

socketio = SocketIO()
socketio.init_app(app)

def init_db():
    """TODO: Need to verify if this works"""
    db = mysql.get_db()
    with app.open_resource(app.config['MYSQL_SCHEMA_FILE'], mode='r') as f:
        db.cursor().execute(f.read())
        more = True
        while more:
            more = db.cursor().nextset()
            # Do we use fetchall() here?

@app.cli.command('initdb')
def initdb_command():
    """Init our database"""
    init_db()
    print("Database initialized")

import TeamMatcher.views
