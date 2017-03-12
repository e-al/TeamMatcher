from flask import request, render_template, session, redirect, url_for
from TeamMatcher import app
from TeamMatcher.student.student import Student


@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/signup',methods=['POST'])
def signUp():
    """Show sign up page or sign the student up"""
    error = None

    # sign the user up and redirect to the main page
    if request.method == 'POST':
        if Student.exists(request['username']):
            error = 'User with this username already exists'
        else:
            # add the user into the database, store the session and redirect

            return redirect(url_for('index'))
    return render_template('signup.html', error)

@app.route('/login', methods=['POST'])
def login():
    """Try to login the user"""
    error = None
    if request.method == 'POST':
        if not Student.exists(request['username']):
            error = 'User with this username does not exist'
        elif Student.verify(request['username'], request['password']):
            # add session
            return redirect(url_for('index'))
        else:
            error = 'Invalid password'

    return render_template('login.html', error=error)

