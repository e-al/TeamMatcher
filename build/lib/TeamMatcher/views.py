from flask import request, render_template, session, redirect, url_for, jsonify
from TeamMatcher import app
from TeamMatcher.student.student import Student


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')

    return redirect(url_for('login'))

@app.route('/home')
def index1():
    if 'username' in session:
        return render_template('home.html')

    return redirect(url_for('login'))

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/searchteam')
def searchteam():
    return render_template('searchteam.html')

@app.route('/searchproject')
def searchproject():
    return render_template('searchproject.html')

@app.route('/addteam')
def addteam():
    return render_template('addteam.html')

@app.route('/addproject')
def addproject():
    return render_template('addproject.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    """Show sign up page or sign the student up"""
    if 'username' in session:
        return redirect(url_for('index'))

    response = dict()
    error = None
    # sign the user up and redirect to the main page
    if request.method == 'POST':
        if Student.exists(request.form['username']):
            error = 'User with this username already exists'
        else:
            # add the user into the database, store the session and redirect
            try:
                Student.add(request.form['username'],
                            request.form['password'],
                            request.form['name'])
                session['username'] = request.form['username']
                response['redirect'] = url_for('index')
                return jsonify(response)
            except RuntimeError as err:
                error = err

    response['form'] = render_template('signup.html', error=error)
    return jsonify(response)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Try to login the user"""
    if 'username' in session:
        return redirect(url_for('index'))

    response = dict()
    error = None
    if request.method == 'POST':
        if not Student.exists(request.form['username']):
            error = 'User with this username does not exist'
        elif Student.verify(request.form['username'],
                            request.form['password']):
            session['username'] = request.form['username']
            response['redirect'] = url_for('index')
            return jsonify(response)
        else:
            error = 'Invalid password'

    response['form'] = render_template('login.html', error=error)
    return jsonify(response)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/updateStudentInfo')
def update_student_info():
    """This is called when we need to update any student info"""

    pass

