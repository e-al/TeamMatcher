from flask import request, render_template, session, redirect, url_for
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


@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    """Show sign up page or sign the student up"""
    if 'username' in session:
        redirect(url_for('index'))

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
                return redirect(url_for('index'))
            except RuntimeError as err:
                error = err

    return render_template('signup.html', error = error)

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Try to login the user"""
    if 'username' in session:
        return redirect(url_for('index'))

    error = None
    if request.method == 'POST':
        if not Student.exists(request.form['username']):
            error = 'User with this username does not exist'
        elif Student.verify(request.form['username'],
                            request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid password'

    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/updateStudentInfo')
def update_student_info():
    """This is called when we need to update any student info"""

    pass

