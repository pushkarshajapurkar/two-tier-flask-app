import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

# Function to create the messages table by executing the SQL script
def create_messages_table():
    print(f"MySQL Host: {app.config['MYSQL_HOST']}")
    print(f"MySQL User: {app.config['MYSQL_USER']}")
    print(f"MySQL Password: {app.config['MYSQL_PASSWORD']}")
    print(f"MySQL DB: {app.config['MYSQL_DB']}")

    if mysql.connection is None:
        print("MySQL connection is None")
        return

    script_path = 'message.sql'  # Path to the SQL script
    with open(script_path, 'r') as sql_file:
        cur = mysql.connection.cursor()
        cur.execute(sql_file.read())
        mysql.connection.commit()
        cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('hello'))

if __name__ == '__main__':
    create_messages_table()  # Create the messages table
    app.run(host='0.0.0.0', port=5000, debug=True)
