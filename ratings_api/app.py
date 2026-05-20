from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ratings = {
    'page1': {'likes': 0, 'dislikes': 0},
    'page2': {'likes': 0, 'dislikes': 0},
    'page3': {'likes': 0, 'dislikes': 0},
}

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'})

@app.route('/api/get-ratings', methods=['GET'])
def get_ratings():
    """Получение рейтинга"""
    page_name = request.args.get('page_name')
    
    if page_name not in ratings:
        return jsonify({'error': 'Page not found'}), 404
    
    return jsonify({
        'likes': ratings[page_name]['likes'],
        'dislikes': ratings[page_name]['dislikes']
    })

@app.route('/api/rate', methods=['POST', 'OPTIONS'])
def rate():
    """Обработка лайка/дизлайка"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        page_name = data.get('page_name')
        rating_type = data.get('type')
        
        if page_name not in ratings:
            return jsonify({'error': 'Page not found'}), 404
        
        if rating_type not in ['like', 'dislike']:
            return jsonify({'error': 'Invalid rating type'}), 400
        
        if rating_type == 'like':
            ratings[page_name]['likes'] += 1
        else:
            ratings[page_name]['dislikes'] += 1
        
        return jsonify({
            'success': True,
            'likes': ratings[page_name]['likes'],
            'dislikes': ratings[page_name]['dislikes']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reset-ratings', methods=['POST', 'OPTIONS'])
def reset_ratings():
    """Сброс рейтинга"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        page_name = data.get('page_name')
        
        if page_name not in ratings:
            return jsonify({'error': 'Page not found'}), 404
        
        ratings[page_name]['likes'] = 0
        ratings[page_name]['dislikes'] = 0
        
        return jsonify({
            'success': True,
            'likes': 0,
            'dislikes': 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)