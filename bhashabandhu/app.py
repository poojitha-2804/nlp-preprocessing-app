import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bhashabandhu_secret_key_2026'

@app.route('/')
@app.route('/bhashabandhu')
def index():
    return render_template('bhashabandhu.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    name = data.get('name', 'Learner')
    email = data.get('email', '')
    lang = data.get('lang', '')
    message = data.get('message', '')

    return jsonify({
        "success": True,
        "message": f"Thank you, {name}! Your message has been received.",
        "recipient": "poojithapooji2804@gmail.com"
    })

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('bhashabandhu.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error occurred."}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
