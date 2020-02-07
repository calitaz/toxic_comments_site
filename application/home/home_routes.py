from flask import Blueprint, render_template, url_for, request, jsonify
from flask import current_app as app
from application import mysqlconfg
import datetime 

home_bp = Blueprint('home_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

## Route for main web index
@home_bp.route('/')
def home():
    conn = mysqlconfg.connection()
    cur = conn.cursor()
    cur.execute("SELECT id,comments FROM comments ORDER BY RAND() LIMIT 1")
    fetchdata = cur.fetchone()
    conn.close()

    return render_template('index.html', data=fetchdata)

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