from flask import request, render_template, session, redirect, url_for, jsonify
import json
from TeamMatcher import app
from TeamMatcher.student.student import Student
from TeamMatcher.project.project import Project


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


@app.route('/projects', methods=['POST', 'GET'])
def projects():
    """Lists the projects the student is involved in

    WARNING: tentatively only lists the projects the student has created
    """

    error = None
    projects_list = None

    if 'username' in session:
        if request.method == 'POST' and 'remove_project' in request.values:
            Project.remove(request.values['remove_project'])
            # just return success code without redirecting
            # client-side js code can then remove the project row
            return json.dumps({'success:True'}), 200, \
                   {'ContentType': 'application/json'}

        projects_list = Project.get_for_student(session['username'])

    return render_template('projects.html', error=error,
                           projects=projects_list)


@app.route('/searchteam')
def searchteam():
    return render_template('searchteam.html')


@app.route('/searchproject')
def searchproject():
    return render_template('searchproject.html')


@app.route('/addteam')
def addteam():
    return render_template('addteam.html')


@app.route('/addproject', methods=['POST', 'GET'])
def addproject():

    error = None

    if 'username' in session:
        if request.method == 'POST':
            response = dict()
            project_id = Project.add(session['username'], **request.form)
            response['redirect'] = url_for('projects', _external=True)
            response['project_id'] = project_id
            return jsonify(response)
    else:
        return redirect(url_for('login'))

    return render_template('addproject.html', error=error)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'username' in session:
        username = session['username']
        if request.method == 'GET':
            info = Student.retrieve_info(username)
            return render_template('profile.html', error=None, info=info)
        if request.method == 'POST':
            Student.update_info(username, **request.form)
            return json.dumps({'success:True'}), 200, \
                   {'ContentType': 'application/json'}

    return redirect(url_for('login'))


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
                response['redirect'] = url_for('index', _external=True)
                return jsonify(response)
            except RuntimeError as err:
                error = err

    response_html = render_template('signup.html', error=error)
    # if we just access the link not through the button click
    if request.method == 'GET':
        return response_html

    response['form'] = response_html
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
            response['redirect'] = url_for('index', _external=True)
            return jsonify(response)
        else:
            error = 'Invalid password'

    response_html = render_template('login.html', error=error)
    # if we just access the link not through the button click
    if request.method == 'GET':
        return response_html

    response['form'] = response_html
    return jsonify(response)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

