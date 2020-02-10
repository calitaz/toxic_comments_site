from flask import Blueprint, render_template, request, jsonify
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug import generate_password_hash, check_password_hash
import datetime 
from application import mysqlconfg
import MySQLdb

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder='templates',
                     static_folder='../static',
                     url_prefix='/admin')

class FormTag(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@admin_bp.route('/login')
def login_page():

    return render_template('login.html')    

@admin_bp.route('/register')
def register_page():
    form = FormTag()
    return render_template('register.html', form = form)  

@admin_bp.route('/register/create', methods=["POST"])
def register():
    retorno = []
    if (request.method == 'POST'):
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if (password != confirmpassword):
            retorno = {'status': "false", 'msg': "Senhas não batem!"}
            return jsonify(retorno)
        else:
            _hashed_password = generate_password_hash(password)
            try:
                conn = mysqlconfg.connection()
                cur = conn.cursor()

                cur.execute("SELECT username,email FROM users")
                fetchdata = cur.fetchall()

                for search in fetchdata:
                    if(search[0] == username):
                        retorno = {'status': "false", 'msg': "Nome de usuário ja cadastrado no sistema"}
                        return jsonify(retorno)
                    if(search[1] == email):
                        retorno = {'status': "false", 'msg': "Email ja cadastrado no sistema"}
                        return jsonify(retorno)
                    
                

                sql = "INSERT INTO users (username, password, email, dateInsert) VALUES (%s, %s, %s, %s)"
                data = (username, _hashed_password, email, current_time)
                cur.execute(sql, data)
                conn.commit()
                lastInsertedId = cur.lastrowid


                sql = "INSERT INTO person (iduser, name, dateInsert) VALUES (%s, %s, %s)"
                data = (lastInsertedId, name, current_time)
                cur.execute(sql, data)
                conn.commit()

                retorno = {'status': "true", 'msg': "Cadastro realizado com sucesso!"}
                return jsonify(retorno)

            except Exception as e:
                retorno = {'status': "false", 'msg': str(e)}
                return jsonify(retorno)
    else: 
        retorno = {'status': "false", 'msg': "Algo aconteceu..."}
        return jsonify(retorno)


        