
from flask import Flask, request, session, redirect, url_for, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re 
app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = 'pass@1New'#password
#in my case password is null so i am keeping empty
app.config['MYSQL_DB'] = 'logindata'#database name

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True

            session['username'] = username
            session['password'] = password
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'mobilenumber' in request.form and'gender' in request.form and 'date' in request.form:
        u = request.form['username']
        p = request.form['password']
        e = request.form['email']
        m = request.form['mobilenumber']
        g = request.form['gender']
        d = request.form['date']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (e))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            
            
        
        else:
            
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts (username, email, password, mobilenumber, gender, date) VALUES (%s,%s,%s,%s,%s,%s)',(u, e, p, m, g, d))
            mysql.connection.commit()
           
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM accounts WHERE username = %s', [session['username']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login')) 
@app.route('/back')
def back(): 
    return render_template('index.html')
           
        

       
      
if __name__ == '__main__':
    app.run()
