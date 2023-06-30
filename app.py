from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL 
import pymysql
 
PRODUCTOS = [
    {
        'id': '1',
        'nombre': 'Funda rosada',
        'descripcion': 'modelo Iphone X',
        'precio': '45.00'
    },
    {
        'id': '2',
        'nombre': 'Mica vidrio',
        'descripcion': 'modelo Samsung A20',
        'precio': '10.50'
    }
]
# configuration
DEBUG = True
 
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
     
mysql = MySQL()
    
app.config['MYSQL_DATABASE_USER'] = 'support'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ubuntu01'
app.config['MYSQL_DATABASE_DB'] = 'tienda_accesorios'
app.config['MYSQL_DATABASE_HOST'] = '34.226.143.67'
mysql.init_app(app)
 

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')
 
@app.route('/productos', methods=['GET'])
def all_productos():
    return jsonify({
        'status': 'success',
        'productos': PRODUCTOS
    })
 
@app.route('/')
def home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * from productos order by id")
        userslist = cursor.fetchall()
        return jsonify({
            'status': 'success',
            'productos': userslist
        })
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
 
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        Nombre = post_data.get('Nombre')
        Descripcion = post_data.get('Descripcion')
        Precio = post_data.get('Precio')
 
        print(Nombre)
        print(Descripcion)
        print(Precio)
 
        sql = "INSERT INTO productos(Nombre,Descripcion,Precio) VALUES(%s, %s, %s)"
        data = (Nombre, Descripcion, Precio)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
 
        response_object['message'] = "Successfully Added"
    return jsonify(response_object)
 
@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    print(id)
    cursor.execute("SELECT * FROM productos WHERE id = %s", [id])
    row = cursor.fetchone() 
 
    return jsonify({
        'status': 'success',
        'editproducto': row
    })
 
@app.route('/update', methods=['GET', 'POST'])
def update():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json(silent=True)
        edit_id = post_data.get('edit_id')
        edit_nombre = post_data.get('edit_nombre')
        edit_descripcion = post_data.get('edit_descripcion')
        edit_precio = post_data.get('edit_precio')
 
        print(edit_nombre)
        print(edit_descripcion)
        print(edit_precio)
 
        cursor.execute ("UPDATE productos SET Nombre=%s, Descripcion=%s, Precio=%s WHERE id=%s",(edit_nombre, edit_descripcion, edit_precio, edit_id))
        conn.commit()
        cursor.close()
 
        response_object['message'] = "Successfully Updated"
    return jsonify(response_object)
 
@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
   
    response_object = {'status': 'success'}
 
    cursor.execute("DELETE FROM productos WHERE id = %s", [id])
    conn.commit()
    cursor.close()
    response_object['message'] = "Successfully Deleted"
    return jsonify(response_object)
 
if __name__ == '__main__':
    app.run()