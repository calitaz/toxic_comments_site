from flask import Blueprint, render_template, url_for, request, jsonify
from flask import current_app as app
from application import mysqlconfg
from application import utils
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
import datetime 

home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates',
                    static_folder='../static')

## Form for define toxic comments in case they exist
class TypeForm(FlaskForm):
    toxic_types = SelectField('tipos', choices=[], validators=[DataRequired()])

## Route for main web index
@home_bp.route('/')
def home():

    sqlcomments = "SELECT c.id, c.comment, c.link, dc.title FROM comments c, data_comments dc WHERE c.link LIKE dc.link_news ORDER BY RAND() LIMIT 1"

    fetchdata = utils.select(sqlcomments, False)

    sqltypes = "SELECT id,type FROM toxic_type"

    fetchtoxictype = utils.select(sqltypes, True)

    
    form = TypeForm()
    form.toxic_types.choices = []

    for toxictypes in fetchtoxictype:
        idtype = toxictypes[0]
        nametype = toxictypes[1]

        form.toxic_types.choices += [(idtype, nametype)]

        

    return render_template('index.html', data=fetchdata, form = form)

## Route for toxic comments
@home_bp.route('/toxic_comment', methods=["POST"])
def toxic():
    conn = mysqlconfg.connection()
    cur = conn.cursor()
    retorno = []

    if(request.method == 'POST'):
        received = request.get_json()
        id_comment = int(received['id'])
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        try:
            cur.execute("INSERT INTO define_comments (idcomment, toxic, dateInsert) VALUES (%s,%s,%s)",(id_comment, 1, current_time))
            conn.commit()
            lastInsertedId = cur.lastrowid
            conn.close()
            retorno = {'status': "sucesso", 'msg': "Sua opinião foi computada com sucesso!", 'lastId': lastInsertedId }
            return jsonify(retorno)

        except Exception as e:
            return jsonify(str(e))

# Route for nontoxic comments
@home_bp.route('/nontoxic_comment', methods=["POST"])
def nontoxic():
    conn = mysqlconfg.connection()
    cur = conn.cursor()
    retorno = []

    if(request.method == 'POST'):
        received = request.get_json()
        id_comment = int(received['id'])
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        try:
            cur.execute("INSERT INTO define_comments (idcomment, toxic, dateInsert) VALUES (%s,%s,%s)",(id_comment, 0, current_time))
            conn.commit()
            lastInsertedId = cur.lastrowid
            conn.close()
            retorno = {'status': "sucesso", 'msg': "Sua opinião foi computada com sucesso!", 'lastId': lastInsertedId }
            return jsonify(retorno)

        except Exception as e:
            return jsonify(str(e))

# Route for defining the type o toxic comment
@home_bp.route('/define_toxic', methods=["POST"])
def definetoxic():
    conn = mysqlconfg.connection()
    cur = conn.cursor()
    retorno = []

    if(request.method == 'POST'):
        received = request.get_json()
        idcomment = int(received['idcomment'])
        idtype = int(received['idtype'])
    
        try:
            cur.execute("INSERT INTO define_type_toxic (idcomment, idtype) VALUES (%s,%s)",(idcomment, idtype))
            conn.commit()
            lastInsertedId = cur.lastrowid
            conn.close()
            retorno = {'status': "sucesso", 'msg': "Sua opinião foi computada com sucesso!", 'lastId': lastInsertedId }
            return jsonify(retorno)

        except Exception as e:
            return jsonify(str(e))
