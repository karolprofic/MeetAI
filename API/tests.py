from flask import Flask, jsonify
from utilities import load_file_and_encode, sanitize

# Flask config
app = Flask(__name__)


# ==========================
#  Text generation content
# ==========================
@app.route('/text_generation_success/', methods=['POST'])
def text_generation_success():
    return jsonify({
        'status': 'Text generated successfully',
        'text': sanitize("'The Grand Budapest Hotel': A whimsical tale of a hotel concierge's adventures, blending humor, intrigue, and visually stunning aesthetics. Perfect for an enchanting evening."),
        'len': 10.728,
        'file': load_file_and_encode('./content/wav/normal.wav')
    })


@app.route('/text_generation_fail/', methods=['POST'])
def text_generation_fail():
    return jsonify({'status': 'Unable to generate text'})


@app.route('/text_generation_long_answer/', methods=['POST'])
def text_generation_long_answer():
    return jsonify({
        'status': 'Text generated successfully',
        'text': sanitize("'Whispers of the Heart' is a heartwarming Japanese animated film that follows a young girl's journey of self-discovery. Shizuku, an aspiring writer, stumbles upon a mysterious cat figurine that leads her on an enchanting adventure. Through her encounters with art, love, and friendship, she learns profound lessons about life's beauty and challenges. The film beautifully explores the transformative power of creativity and following one's passions. With its stunning animation and a captivating story, 'Whispers of the Heart' is a perfect choice for an evening filled with warmth, inspiration, and reflection on the magical aspects of life."),
        'len': 38.856,
        'file': load_file_and_encode('./content/wav/long.wav')
    })


@app.route('/text_generation_medium_answer/', methods=['POST'])
def text_generation_medium_answer():
    return jsonify({
        'status': 'Text generated successfully',
        'text': sanitize("'Lost in Translation' is a captivating film about the unlikely connection between two lonely souls in Tokyo. Bill Murray and Scarlett Johansson deliver poignant performances in this atmospheric exploration of isolation, cultural differences, and the profound impact of human connection. A beautifully introspective choice for an evening viewing."),
        'len': 21.432,
        'file': load_file_and_encode('./content/wav/medium.wav')
    })


@app.route('/text_generation_short_answer/', methods=['POST'])
def text_generation_short_answer():
    return jsonify({
        'status': 'Text generated successfully',
        'text': sanitize("'Inception': Mind-bending heist within dreams, a visual masterpiece."),
        'len': 4.2,
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
