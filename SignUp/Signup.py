from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)


# Configure MySQL connection
app.config['MYSQL_USER'] = 'Shama'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'LoginPage'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/loginPage/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            msg = 'Username already exists!'
        else:
            # Account doesnt exist, insert new account
            cursor.execute('INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
if __name__ == '__main__':
    app.run(debug=True)   