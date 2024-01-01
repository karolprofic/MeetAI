from converter.TextToSpeech import TextToSpeech
from converter.SpeechToText import SpeechToText
from generator.TextGenerator import TextGenerator
from generator.ImageGenerator import ImageGenerator
from flask import Flask, request, jsonify, send_file, abort
from openai import OpenAI
from utilities import *
import pyttsx3

# Config
PROJECT_DIRECTORY = create_project_directory("MeetAI")
ALLOWED_EXTENSIONS = ['png', 'wav']

# Libraries
set_environment_variables()
pyttsx = pyttsx3.init()
openAI = OpenAI()

# API Classes
stt = SpeechToText(PROJECT_DIRECTORY, openAI)
tts = TextToSpeech(PROJECT_DIRECTORY, pyttsx, openAI)
tg = TextGenerator(PROJECT_DIRECTORY, openAI)
ig = ImageGenerator(PROJECT_DIRECTORY, openAI)

# Flask config
app = Flask(__name__)


# TODO Run script refactor and conda/venv environment (ask for api key)
# TODO Postmen new config and test all output
# TODO Make documentation and Postman/Conda config
# TODO New documentation with clearer way to show endpoints
# TODO Finish and test MeetAI Endpoints (Text and Image)

# ==========================
#       General API
# ==========================
@app.route('/set_api_key/', methods=['POST'])
def set_api_key():
    request_data = request.get_json()
    request_api = request_data["api"]
    request_key = request_data["key"]

    if request_api is None or request_key is None:
        return jsonify({'status': 'Incorrect request parameters'})

    if request_api == "OpenAI":
        os.environ['OPENAI_API_KEY'] = str(request_key)
        openAI.api_key = os.environ['OPENAI_API_KEY']
        return jsonify({'status': 'OpenAI API key added successfully'})

    return jsonify({'status': 'Requested API is not supported'})


@app.route('/speech_to_text/<model>/', methods=['POST'])
def speech_to_text(model):
    result = save_file()

    if result['status'] != 'File uploaded successfully':
        return jsonify(result)

    return jsonify(stt.generate(model, result['filename']))


@app.route('/text_to_speach/', methods=['POST'])
def text_to_speach():
    request_data = request.get_json()
    request_model = request_data["model"]
    request_voice = request_data["voice"]
    request_text = request_data["text"]

    if any(arg is None or arg == "" for arg in [request_model, request_voice, request_text]):
        return jsonify({'status': 'Incorrect or missing data'})

    return jsonify(tts.generate(request_model, request_voice, request_text))


@app.route('/image_generation/', methods=['POST'])
def image_generation():
    request_data = request.get_json()
    request_model = request_data["model"]
    request_description = request_data["description"]

    if any(arg is None or arg == "" for arg in [request_model, request_description]):
        return jsonify({'status': 'Incorrect or missing data'})

    return jsonify(ig.generate(request_model, request_description))


@app.route('/text_generation/', methods=['POST'])
def text_generation():
    request_data = request.get_json()
    request_model = request_data["model"]
    request_query = request_data["query"]

    if any(arg is None or arg == "" for arg in [request_model, request_query]):
        return jsonify({'status': 'Incorrect or missing data'})

    return jsonify(tg.generate(request_model, request_query))


@app.route('/download_file/<filename>/', methods=['GET'])
def download_file(filename):
    filepath = PROJECT_DIRECTORY + filename
    extension = filepath.rsplit('.', 1)[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        abort(400)

    if not os.path.exists(filepath):
        abort(404)

    mimetype = "image/png" if extension == "png" else "audio/wav"
    return send_file(filepath, mimetype=mimetype, as_attachment=True)


@app.route('/upload_file/', methods=['POST'])
def upload_file():
    return jsonify(save_file())


@app.route('/status/', methods=['POST'])
def status():
    return jsonify({'status': 'Server is working'})


# ==========================
#        MeetAI API
# ==========================
@app.route('/generate_text/', methods=['POST'])
def generate_text():
    request_data = request.get_json()
    request_model = request_data["text_model"]
    request_sst = request_data["stt_model"]
    request_tts_model = request_data["tts_model"]
    request_tts_voice = request_data["tts_voice"]
    request_type = request_data["query_type"]
    request_query = request_data["query_content"]

    if any(arg is None or arg == "" for arg in [request_model, request_sst, request_tts_model, request_tts_voice, request_type, request_query]):
        return jsonify({'status': 'Incorrect or missing data'})

    if request_type != 'Microphone' and request_type != 'Keyboard':
        return jsonify({'status': 'Unknown request type'})

    if request_type == 'Microphone':
        audio_filename = save_file_and_decode(PROJECT_DIRECTORY, request_query)
        transcription = stt.generate(request_sst, audio_filename)
        if transcription['status'] != 'Speech recognized successfully':
            return jsonify({'status': 'Unable to recognize speech'})
        request_query = transcription['text']

    if request_query is None or len(request_query) == 0:
        return jsonify({'status': 'Failed to process input data'})

    tg_result = tg.generate(request_model, request_query)
    if tg_result['status'] != 'Text generated successfully':
        return jsonify(tg_result)

    tts_result = tts.generate(request_tts_model, request_tts_voice, tg_result['text'])
    if tts_result['status'] != 'Speech generated successfully':
        return jsonify(tts_result)

    filepath = PROJECT_DIRECTORY + tts_result['filename']
    return jsonify({
        'status': 'Text generated successfully',
        'text': tg_result['text'],
        'len': tts_result['len'],
        'file': load_file_and_encode(filepath)
    })


@app.route('/generate_image/', methods=['POST'])
def generate_image():
    request_data = request.get_json()
    request_model = request_data["image_model"]
    request_sst = request_data["stt_model"]
    request_type = request_data["query_type"]
    request_query = request_data["query_content"]

    if any(arg is None or arg == "" for arg in [request_model, request_sst, request_type, request_query]):
        return jsonify({'status': 'Incorrect or missing data'})

    if request_type != 'Microphone' and request_type != 'Keyboard':
        return jsonify({'status': 'Unknown request type'})

    if request_type == 'Microphone':
        audio_filename = save_file_and_decode(PROJECT_DIRECTORY, request_query)
        transcription = stt.generate(request_sst, audio_filename)
        if transcription['status'] != 'Speech recognized successfully':
            return jsonify({'status': 'Unable to recognize speech'})
        request_query = transcription['text']

    result = ig.generate(request_model, request_query)
    if result['status'] != 'Image generated successfully':
        return jsonify(result)

    filepath = PROJECT_DIRECTORY + result['filename']
    return jsonify({
        'status': 'Image generated successfully',
        'file': load_file_and_encode(filepath)
    })


# ==========================
#       Helpers
# ==========================
def save_file():
    if 'file' not in request.files:
        return {'status': 'No file in request'}

    file = request.files['file']
    if file.filename == '' or file is None:
        return {'status': 'No selected file or file empty'}

    extension = file.filename.rsplit('.', 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return {'status': 'File extension not allowed'}

    filetype = "image" if extension == "png" else "audio"
    filename = datetime.now().strftime(f"{filetype}_%d-%m-%Y_%H-%M-%S.{extension}")
    filepath = PROJECT_DIRECTORY + filename
    file.save(filepath)

    return {'status': 'File uploaded successfully', 'filename': filename}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
