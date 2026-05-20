from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Простое хранилище пользователей (в памяти)
users = {}

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация пользователя"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if email in users:
            return jsonify({'success': False, 'error': 'User already exists'}), 400
        
        users[email] = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': email,
            'age': data.get('age')
        }
        
        return jsonify({'success': True, 'message': 'User registered'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Получение списка пользователей"""
    return jsonify(list(users.values()))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
