from flask import Blueprint, render_template, request, jsonify, flash, redirect, session, url_for
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from werkzeug import generate_password_hash, check_password_hash
import datetime 
from application import mysqlconfg
import MySQLdb

admin = Blueprint('admin', __name__,
                     template_folder='templates',
                     static_folder='../static',
                     url_prefix='/admin')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

## Login - Registration ##
@admin.route('/')
def index():
    return login_page()

@admin.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        token = form.csrf_token.data

        conn = mysqlconfg.connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, password FROM users WHERE email LIKE %s", [email])

        fetchdata = cur.fetchone()
        conn.close()

        if fetchdata:
           confirmedpass = check_password_hash(fetchdata[2],password)
           if confirmedpass:
               session['loggedin'] = True
               session['id'] = fetchdata[0]
               session['token'] = token

               return redirect(url_for('admin.dashboard'))
           else:
               flash("E-mail e/ou senha estão incorretos. Por favor, tente novamente")

        
    return render_template('login.html', form=form)    

@admin.route('/register')
def register_page():
    form = FlaskForm()
    return render_template('register.html', form = form)  

@admin.route('/register/create', methods=["POST"])
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
                        conn.close()
                        return jsonify(retorno)
                    if(search[1] == email):
                        retorno = {'status': "false", 'msg': "Email ja cadastrado no sistema"}
                        conn.close()
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
                conn.close()
                retorno = {'status': "true", 'msg': "Cadastro realizado com sucesso!"}
                return jsonify(retorno)

            except Exception as e:
                retorno = {'status': "false", 'msg': str(e)}
                return jsonify(retorno)
    else: 
        retorno = {'status': "false", 'msg': "Algo aconteceu..."}
        return jsonify(retorno)

## End Login - Registration ##

@admin.route('/dashboard')
def dashboard():
    if 'loggedin' in session and 'token' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@admin.route('/logout')
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('login_page'))



        