from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
            # Account doesnt exist or username/password incorrect
    return render_template('index.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

    # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# Push the request to db
@app.route('/portal', methods=['GET', 'POST'])
def portal():
    msg = ''
    if request.method == "POST" and 'name' in request.form and 'email' in request.form and 'subject' in request.form and 'details' in request.form:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        details = request.form['details']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO portal VALUES (NULL,%s,%s,%s,%s,0)', (name, email, subject, details))
        mysql.connection.commit()
        msg = 'Request Sent'

    return render_template('portal.html', msg=msg)


# @app.route('/profile', methods=['GET', 'POST'])
# def approval():
#     msg = ''
#     if request.method == "POST" and 'id' in request.form:
#         status = request.form['id']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         if status == '1':
#             cursor.execute('UPDATE portal SET     approval = 1 WHERE id = 2')
#             msg = 'Approved'
#         elif status == '0':
#             cursor.execute('UPDATE portal SET     approval = 0 WHERE id = 2')
#             msg = 'Rejected'
#         mysql.connection.commit()

#     return render_template('layout.html', msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile', methods=['POST', 'GET'])
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = cursor.fetchall()
        # Show the profile page with account info
        select_stmt = (
            'SELECT *  FROM portal where approval = 0 ORDER by id DESC ')
        cursor.execute(select_stmt)
        portal = cursor.fetchall()
        approval_statement = (
            'SELECT *  FROM portal where approval = 1 ORDER by id DESC ')
        cursor.execute(approval_statement)
        account = cursor.fetchall()
        # msg = 'Data'
    # if request.method == "POST" and 'name' in request.form and 'id' in request.form:
    #     name = request.form['name']
    #     if name == 'Approve':
    #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #         cursor.execute('UPDATE portal SET approval = 1 WHERE id = 1')
    #         # elif name == 'Reject':
    #         #     cursor.execute('UPDATE portal SET approval = 0 WHERE id = 1')
    #         #     msg = 'Rejected'
    #     mysql.connection.commit()
    return render_template('profile.html', account=account, portal=portal)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/approving', methods=['POST', 'GET'])
def approving():
    if request.method == "GET":
        aname = request.args.get('aname')
        aid=request.args.get('aid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE portal SET approval = 1 WHERE name = %s and id = %s',[aname,aid])
        # elif name == 'Reject':
        #     cursor.execute('UPDATE portal SET approval = 0 WHERE id = 1')
        #     msg = 'Rejected'
        mysql.connection.commit()
        # msg = 'Approved'
    return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(debug=True)
