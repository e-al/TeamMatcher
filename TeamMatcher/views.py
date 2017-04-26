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
            return json.dumps({'success': True}), 200, \
                   {'ContentType': 'application/json'}

        projects_list = Project.get_created_by_student(session['username'])

    return render_template('projects.html', error=error,
                           projects=projects_list)


@app.route('/searchproject')
def searchproject():
    info = Project.get_all()
    projSkills = Project.get_all_Proj_Skills()
    return render_template('searchproject.html', info=info, projSkills=projSkills)


@app.route('/addToProject')
def addToProject():
    username = request.args.get('user')
    id = request.args.get('proj')
    Project.add_student(username, id)
    url = "/viewprofile?user="+ username
    return redirect(url)

@app.route('/addSkillProj')
def addSkillProj():
    skill = request.args.get('skill')
    id = request.args.get('proj')
    Project.addSkillToProject(id,skill)
    url = "/editproject?proj="+ id
    return redirect(url)

@app.route('/addSkillPerson')
def addSkillPerson():
    skill = request.args.get('skill')
    user = request.args.get('user')
    Student.add_skill(user,skill,0)
    url = "/profile"
    return redirect(url)

@app.route('/removeprojpart')
def removeprojpart():
    username = request.args.get('user')
    id = request.args.get('proj')
    Project.remove_student(username, id)
    url = "/editproject?proj="+ id
    return redirect(url)

@app.route('/removeprojskill')
def removeprojskill():
    skill = request.args.get('skill')
    id = request.args.get('proj')
    Project.removeSkillFromProject(id,skill)
    url = "/editproject?proj="+ id
    return redirect(url)

@app.route('/removeUserSkill')
def removeUserSkill():
    skill = request.args.get('skill')
    user = request.args.get('user')
    Student.remove_skill(user,skill)
    url = "/profile"
    return redirect(url)

@app.route('/createSkill')
def createSkill():
    skill = request.args.get('skill')
    id = request.args.get('proj')
    skill_id = Project.createSkill(skill)
    Project.addSkillToProject(id,skill_id)
    url = "/editproject?proj="+ id
    return redirect(url)

@app.route('/createSkillUser')
def createSkillUser():
    skill = request.args.get('skill')
    skill_id = Project.createSkill(skill)
    Student.add_skill(session['username'],skill_id,0)
    url = "/profile"
    return redirect(url)

@app.route('/setSkill')
def setSkill():
    skill = request.args.get('skill')
    user = request.args.get('user')
    level = request.args.get('level')
    Student.update_skill(user,skill,level)
    url = "/profile"
    return redirect(url)


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

@app.route('/editproject', methods=['POST', 'GET'])
def editproject():

    error = None

    if 'username' in session:
        if request.method == 'POST':
            response = dict()
            project_id = Project.update_info(**request.form)
            response['redirect'] = url_for('projects', _external=True)
            response['project_id'] = project_id
            return jsonify(response)
        if request.method == 'GET':
            id = request.args.get('proj')
            project = Project.get_info(id)
            people = Project.get_participants(id)
            skills = Project.get_all_Skills(id)
            projSkills = Project.get_Skills(id)
            return render_template("editproject.html", project = project, people = people, skills = skills , projSkills = projSkills)
    else:
        return redirect(url_for('login'))

    return render_template('editproject.html', error=error)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'username' in session:
        username = session['username']
        if request.method == 'GET':
            info = Student.retrieve_info(username)
            skills = Student.getAllSkills(username)
            profSkills = Student.getSkills(username)
            return render_template('profile.html', error=None, info=info, skills = skills , profSkills = profSkills)
        if request.method == 'POST':
            Student.update_info(username, **request.form)
            return json.dumps({'success': True}), 200, \
                   {'ContentType': 'application/json'}

    return redirect(url_for('login'))

@app.route('/viewprofile', methods=['POST', 'GET'])
def viewprofile():
    if 'username' in session:
        username = request.args.get('user')
        if request.method == 'GET':
            info = Student.retrieve_info(username)
            projects = Project.get_for_student(username)
            projects_list = Project.get_created_by_student_user(session['username'],username)
            skills = Student.getSkills(username)
            return render_template('viewprofile.html', error=None, info=info, projects=projects_list, projects_u = projects, profSkills = skills)

    return redirect(url_for('login'))

@app.route('/viewproject', methods=['POST', 'GET'])
def viewproject():
    if 'username' in session:
        id = request.args.get('proj')
        if request.method == 'GET':
            info = Project.get_info(id)
            people = Project.get_participants(id)
            projSkills = Project.get_Skills(id)
            return render_template('viewproject.html', error=None,
                                   project=info, people=people, projSkills = projSkills)

    return redirect(url_for('login'))



@app.route('/searchprofiles', methods=['POST', 'GET'])
def searchprofiles():
    if 'username' in session:
        if request.method == 'GET':
            info = Student.retrieve_all_info()
            peopleSkills = Student.get_all_People_Skills()
            return render_template('searchperson.html', error=None, info=info, peopleSkills=peopleSkills)

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

@app.route('/recommended')
def recommended():
    proj = Student.getRecommended(session['username'])
    projSkills = Project.get_all_Proj_Skills()
    if proj:
        return render_template('searchproject.html', info=proj, projSkills=projSkills)
    else:
        return render_template('home.html')

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

@app.route('/message')
def message():
    if 'username' in session:
        return render_template('message.html')
    return redirect(url_for('index'))

