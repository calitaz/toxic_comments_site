from flask_mysqldb import MySQL
from flask import current_app as app

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'comments_database'

mysql = MySQL(app)

def connection():
    cur = mysql.connect
    return cur