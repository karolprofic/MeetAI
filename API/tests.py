from flask import Flask, jsonify, send_file

# Flask config
app = Flask(__name__)


# ==========================
#  Text generation content
# ==========================
@app.route('/text_generation_fail/', methods=['POST'])
def text_generation_fail():
    return jsonify({'status': 'Unable to generate text'})


@app.route('/text_generation_long_answer/', methods=['POST'])
def text_generation_long_answer():
    return jsonify({
        'status': 'Text generated successfully',
        'text': "Lost in Translation is a captivating film about the unlikely connection between two lonely souls in Tokyo. Bill Murray and Scarlett Johansson deliver poignant performances in this atmospheric exploration of isolation, cultural differences, and the profound impact of human connection. A beautifully introspective choice for an evening viewing.",
        'len': 21.432,
        'filename': 'long.wav'
    })


@app.route('/text_generation_medium_answer/', methods=['POST'])
def text_generation_medium_answer():
    return jsonify({
        'status': 'Text generated successfully',
        'text': 'The Grand Budapest Hotel: A whimsical tale of a hotel concierge\'s adventures, blending humor, intrigue, and visually stunning aesthetics. Perfect for an enchanting evening.',
        'len': 10.728,
        'filename': 'medium.wav'
    })


@app.route('/text_generation_short_answer/', methods=['POST'])
def text_generation_short_answer():
    return jsonify({
        'status': 'Text generated successfully',
        'text': 'Inception Mind-bending heist within dreams, a visual masterpiece.',
        'len': 4.2,
        'filename': 'short.wav'
    })


# ==========================
#  Image generation content
# ==========================
@app.route('/image_generation_fail/', methods=['POST'])
def image_generation_fail():
    return jsonify({'status': 'Unable to generated image'})


@app.route('/image_generation_large_file/', methods=['POST'])
def image_generation_large_file():
    return jsonify({
        'status': 'Image generated successfully',
        'filename': 'large.png'
    })


@app.route('/image_generation_small_file/', methods=['POST'])
def image_generation_small_file():
    return jsonify({
        'status': 'Image generated successfully',
        'filename': 'blank.png'
    })


# ==========================
#  Other
# ==========================
@app.route('/download_file/<filename>/', methods=['GET'])
def download_file(filename):
    filepath = './content/' + ('img' if 'png' in filename else 'wav') + '/' + filename
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
