from flask import Flask, jsonify

# Flask config
app = Flask(__name__)


# ==========================
#  Text generation tests
# ==========================
@app.route('/text_generation_success/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/text_generation_fail/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/text_generation_file_corrupted/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/text_generation_long_answer/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/text_generation_medium_answer/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/text_generation_short_answer/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


# ==========================
#  Image generation tests
# ==========================
@app.route('/image_generation_success/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/image_generation_fail/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


@app.route('/image_generation_file_corrupted/', methods=['POST'])
def text_long_answer():
    # TODO Implement
    return jsonify({'status': ''})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
