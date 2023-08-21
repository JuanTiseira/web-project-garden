from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Conexión a la base de datos
def connect_db():
    return psycopg2.connect(
        host="tu_host",
        database="tu_base_de_datos",
        user="tu_usuario",
        password="tu_contraseña"
    )

# Ruta para el registro de usuarios
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (Nombre) VALUES (%s) RETURNING ID", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Usuario registrado con éxito', 'user_id': user_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM Usuarios WHERE Nombre = %s", (username,))
        user_id = cursor.fetchone()
        
        if user_id:
            return jsonify({'message': 'Inicio de sesión exitoso', 'user_id': user_id[0]}), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear plantas
@app.route('/create_plant', methods=['POST'])
def create_plant():
    try:
        data = request.json
        plant_name = data['name']
        description = data['description']
        price = data['price']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Plantas (Nombre, Descripcion, Precio) VALUES (%s, %s, %s) RETURNING ID", (plant_name, description, price))
        plant_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Planta creada con éxito', 'plant_id': plant_id}), 201
    
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


if __name__ == '__main__':
    app.run(debug=True)
