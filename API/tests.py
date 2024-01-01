from flask import Flask, jsonify
from utilities import load_file_and_encode

# Flask config
app = Flask(__name__)

# TODO img: blank.png
# TODO wav: normal.wav / long.wav / medium.wav / short.wav


# ==========================
#  Text generation content
# ==========================
@app.route('/text_generation_success/', methods=['POST'])
def text_generation_success():
    # TODO Implement
    return jsonify({
        'status': 'Text generated successfully',
        'text': '',
        'len': '',
        'file': load_file_and_encode('./content/wav/normal.wav')
    })


@app.route('/text_generation_fail/', methods=['POST'])
def text_generation_fail():
    return jsonify({'status': 'Unable to generate text'})


@app.route('/text_generation_long_answer/', methods=['POST'])
def text_generation_long_answer():
    # TODO Implement
    return jsonify({
        'status': 'Text generated successfully',
        'text': '',
        'len': '',
        'file': load_file_and_encode('./content/wav/long.wav')
    })


@app.route('/text_generation_medium_answer/', methods=['POST'])
def text_generation_medium_answer():
    # TODO Implement
    return jsonify({
        'status': 'Text generated successfully',
        'text': '',
        'len': '',
        'file': load_file_and_encode('./content/wav/medium.wav')
    })


@app.route('/text_generation_short_answer/', methods=['POST'])
def text_generation_short_answer():
    # TODO Implement
    return jsonify({
        'status': 'Text generated successfully',
        'text': '',
        'len': '',
        'file': load_file_and_encode('./content/wav/short.wav')
    })


# ==========================
#  Image generation content
# ==========================
@app.route('/image_generation_success/', methods=['POST'])
def image_generation_success():
    return jsonify({
        'status': 'Image generated successfully',
        'file': load_file_and_encode('./content/img/blank.png')
    })


@app.route('/image_generation_fail/', methods=['POST'])
def image_generation_fail():
    return jsonify({'status': 'An error occurred'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
