
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
 

# Configure MySQL connection
app.config['MYSQL_USER'] = 'Shama'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'loginPage' #pythonlogin
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/loginPage/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve the form data
        username = request.form['username']
        password = request.form['password']

        # Check if account exists 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return the result
        account = cursor.fetchone()

        # If account exists in accounts table in our database
        if account:
            # Create session data
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            return  'Incorrect username/password!'
if __name__ == '__main__':
    app.run(debug=True)
