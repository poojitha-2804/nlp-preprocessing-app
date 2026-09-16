import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from utils.nlp_processor import nlp_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nlp_preprocess_secret_key_2026'

# ----------------------------------------------------
# PAGE ROUTES
# ----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/techniques')
def techniques():
    return render_template('techniques.html')

@app.route('/tokenization')
def tokenization():
    return render_template('tokenization.html')

@app.route('/stemming')
def stemming():
    return render_template('stemming.html')

@app.route('/lemmatization')
def lemmatization():
    return render_template('lemmatization.html')

@app.route('/stopwords')
def stopwords():
    return render_template('stopwords.html')

@app.route('/cleaning')
def cleaning():
    return render_template('cleaning.html')

@app.route('/pos-tagging')
@app.route('/pos')
def pos_tagging():
    return render_template('pos_tagging.html')

@app.route('/workbench')
def workbench():
    return render_template('playground.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/about')
def about():
    return render_template('about.html')


# ----------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "NLP Data Preprocessing API",
        "version": "1.0.0"
    })

@app.route('/api/tokenize', methods=['POST'])
def api_tokenize():
    data = request.get_json() or {}
    text = data.get('text', '')
    token_type = data.get('type', 'word')
    pattern = data.get('pattern', r'\b\w+\b')
    n_gram = data.get('n', 2)

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    result = nlp_engine.tokenize(text, token_type=token_type, pattern=pattern, n=n_gram)
    return jsonify(result)

@app.route('/api/stem', methods=['POST'])
def api_stem():
    data = request.get_json() or {}
    text = data.get('text', '')
    algorithm = data.get('type', 'porter')

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    result = nlp_engine.stem(text, algorithm=algorithm)
    return jsonify(result)

@app.route('/api/lemmatize', methods=['POST'])
def api_lemmatize():
    data = request.get_json() or {}
    text = data.get('text', '')
    method = data.get('type', 'wordnet')

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    result = nlp_engine.lemmatize(text, method=method)
    return jsonify(result)

@app.route('/api/remove-stopwords', methods=['POST'])
def api_stopwords():
    data = request.get_json() or {}
    text = data.get('text', '')
    method = data.get('type', 'standard')
    custom_words = data.get('custom_words', '')
    lang = data.get('lang', 'english')
    domain = data.get('domain', 'tech')

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    result = nlp_engine.remove_stopwords(text, method=method, custom_words=custom_words, lang=lang, domain=domain)
    return jsonify(result)

@app.route('/api/clean', methods=['POST'])
def api_clean():
    data = request.get_json() or {}
    text = data.get('text', '')
    operations = data.get('operations', ['lowercasing', 'punctuation_removal', 'extra_whitespace_removal'])

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    result = nlp_engine.clean_text(text, operations=operations)
    return jsonify(result)

@app.route('/api/pos-tag', methods=['POST'])
def api_pos_tag():
    data = request.get_json() or {}
    text = data.get('text', '')
    tagset = data.get('tagset', 'penn')
    algorithm = data.get('algorithm', 'nltk')
    ground_truth = data.get('ground_truth', None)

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    if ground_truth:
        result = nlp_engine.evaluate_pos_tagging(text, ground_truth=ground_truth, algorithm=algorithm, tagset=tagset)
    else:
        result = nlp_engine.pos_tag_text(text, tagset=tagset, algorithm=algorithm)
    return jsonify(result)

@app.route('/api/process', methods=['POST'])
def api_process():
    data = request.get_json() or {}
    text = data.get('text', '')
    technique = data.get('technique', 'tokenization')
    sub_type = data.get('type', 'word')
    custom_options = data.get('options', {})

    if not text.strip():
        return jsonify({"success": False, "error": "Please enter some text before processing."}), 400

    result = nlp_engine.process_playground(text, technique, sub_type=sub_type, custom_options=custom_options)
    return jsonify(result)


# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error occurred."}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
