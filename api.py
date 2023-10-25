from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import bcrypt
from utils import verificar_token
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# Conexión a la base de datos
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="web",
        user="test",
        password="test12."
    )

# Ruta para el registro de usuariosimport bcrypt  # Asegúrate de importar bcrypt

@app.route('/register', methods=['POST'])
@verificar_token
def register():
    try:
        data = request.json
        username = data['username']
        estado = data['state']
        rol = data['rol']
        password = data['password']
        
        # Generar un hash de contraseña utilizando bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = connect_db()
        cursor = conn.cursor()
        tosave = hashed_password.decode('utf-8')
        cursor.execute("INSERT INTO Usuarios (nombre, estado, id_rol, password) \
                       VALUES (%s, %s, %s, %s) RETURNING ID", (username, estado, rol, tosave))
        user_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Usuario registrado con éxito', 'user_id': user_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta para el inicio de sesión
import jwt
import datetime

# ...

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, id_rol, password FROM Usuarios WHERE Nombre = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            nombre, id_rol, password_hash = user_data
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                # Genera un token JWT con una expiración de 30 minutos
                token_payload = {
                    'nombre': nombre,
                    'id_rol': id_rol,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                }
                secret_key = 'tu_clave_secreta'  # Cambia esto a tu clave secreta real
                token = jwt.encode(token_payload, secret_key, algorithm='HS256')
                
                return jsonify({'message': 'Inicio de sesión exitoso', 'nombre': nombre, 'id_rol': id_rol, 'token': token}), 200
            else:
                return jsonify({'error': 'Contraseña incorrecta'}), 401
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear plantas
@app.route('/create_plant', methods=['POST'])
def create_plant():
    try:
        data = request.json
        nombre = data['nombre']
        descripcion = data['descripcion']
        imagen = data['imagen']

        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Plantas (nombre, descripcion, imagen) VALUES (%s, %s, %s) RETURNING ID", (nombre, descripcion, imagen))
        plant_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Planta creada con éxito', 'plant_id': plant_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_plants', methods=['GET'])
def get_plants():
    print("hola")
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plantas")
        plants = cursor.fetchall()
        conn.close()

        # Convierte los resultados en una lista de diccionarios
        plant_list = []
        for plant in plants:
            plant_dict = {
                'id': plant[0],
                'nombre': plant[1],
                'descripcion': plant[2],
                'imagen': plant[3]
            }
            plant_list.append(plant_dict)

        return jsonify({'plants': plant_list})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_plant/<int:plant_id>', methods=['POST'])
def update_plant(plant_id):
    try:
        data = request.json
        print(data)
        nombre = data['nombre']
        descripcion = data['descripcion']
        imagen = data['imagen']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE plantas SET nombre = %s, descripcion = %s, imagen = %s WHERE id = %s", (nombre, descripcion, imagen, plant_id))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Planta con ID {plant_id} modificada con éxito'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_plant/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM plantas WHERE id = %s", (plant_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Planta con ID {plant_id} eliminada con éxito'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500   
# Ruta para crear publicaciones
@app.route('/create_publication', methods=['POST'])
def create_publication():
    try:
        data = request.json
        title = data['title']
        content = data['content']
        plant_id = data['plant_id']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Publicaciones (Titulo, Contenido, ID_Planta) VALUES (%s, %s, %s) RETURNING ID", (title, content, plant_id))
        publication_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Publicación creada con éxito', 'publication_id': publication_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para cambiar el estado del usuario a "Aprobado"
@app.route('/approve_user/<int:user_id>', methods=['PUT'])
def approve_user(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuarios SET Estado = %s WHERE ID = %s", ('Aprobado', user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Estado del usuario actualizado a Aprobado'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
##imagen

# Configura la carpeta donde se almacenarán las imágenes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Tamaño máximo de archivo (16 MB)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta para cargar una imagen
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se ha seleccionado ninguna imagen.'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No se ha seleccionado ninguna imagen.'}), 400

    if image:
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        return jsonify({'message': 'Imagen cargada con éxito'}), 200

# Ruta para acceder a una imagen cargada
@app.route('/uploads/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
    app.run(debug=True)
