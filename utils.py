import jwt
from functools import wraps
from flask import request, jsonify


def verificar_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token faltante'}), 401
        
        try:
            secret_key = 'tu_clave_secreta'  # Reemplaza con tu clave secreta real
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # Puedes acceder a los datos del token en data (por ejemplo, data['nombre'], data['id_rol'])
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return wrapper
