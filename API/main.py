import pyttsx3
import soundfile
from flask import Flask, request, jsonify, send_file, abort
from datetime import datetime
from utilities import *
from openai import OpenAI
from converter.TextToSpeech import TextToSpeech
from converter.SpeechToText import SpeechToText

# Libraries
pyttsx = pyttsx3.init()
openAI = OpenAI()

# Config
openAI.api_key = os.getenv('OPENAI_API_KEY', '')
PROJECT_DIRECTORY = create_project_directory("MeetAI")
ALLOWED_EXTENSIONS = {'png', 'wav'}

# Flask config
app = Flask(__name__)

# API Classes
stt = SpeechToText(PROJECT_DIRECTORY, openAI)
tts = TextToSpeech(PROJECT_DIRECTORY, pyttsx, openAI)


# TODO Refactor ImageGenerator (generate - better model name handling)
# TODO Finish Main Refactor
# TODO Implement TextGenerator
# TODO Run script refactor and conda/venv environment
# TODO Postmen new config and test all output
# TODO Facebook Lama and dedicated server - read about it
# TODO Setting API Key during setup and check
# TODO Think about UE5 C++ Implementation

###############################
#        General API          #
###############################
@app.route('/set_api_key/', methods=['POST'])
def set_api_key():
    request_data = request.get_json()
    request_api = request_data["api"]
    request_key = request_data["key"]

    if request_api is None or request_key is None:
        return jsonify({'status': 'Incorrect request parameters'})

    match request_api:
        case "OpenAI":
            os.environ['OPENAI_API_KEY'] = str(request_key)
            openAI.api_key = os.environ['OPENAI_API_KEY']
            return jsonify({'status': 'OpenAI API key added successfully'})
        case _:
            return jsonify({'status': 'Requested API is not supported'})


@app.route('/speech_to_text/<model>/', methods=['POST'])
def speech_to_text(model):
    if model == "" or model is None:
        return jsonify({'status': 'STT model was not specified'})

    if 'file' not in request.files:
        return jsonify({'status': 'No file in request'})

    file = request.files['file']
    if file.filename == '' or file is None:
        return jsonify({'status': 'No selected file or file empty'})

    # Save file
    filename = datetime.now().strftime("audio_%d-%m-%Y_%H-%M-%S.wav")
    path = PROJECT_DIRECTORY + filename
    file.save(path)

    # Resample file
    data, samplerate = soundfile.read(path)
    soundfile.write(path, data, samplerate, subtype='PCM_16')

    return jsonify(stt.generate(model, filename))


@app.route('/text_to_speach/', methods=['POST'])
def text_to_speach():
    request_data = request.get_json()
    request_model = request_data["model"]
    request_voice = request_data["voice"]
    request_text = request_data["text"]

    if any(arg is None for arg in [request_model, request_voice, request_text]):
        return jsonify({'status': 'Incorrect or missing data'})

    return jsonify(tts.generate(request_model, request_voice, request_text))


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
    # TODO Implement
    # TODO Check filename and extension if is allowed
    # TODO Remove duplicated code
    pass
    # if 'file' not in request.files:
    #     return jsonify({'status': 'No file in request'})
    #
    # file = request.files['file']
    # if file.filename == '' or file is None:
    #     return jsonify({'status': 'No selected file or file empty'})
    #
    # filename = datetime.now().strftime("audio_%d-%m-%Y_%H-%M-%S.wav")
    # path = PROJECT_DIRECTORY + filename
    # file.save(path)
    #
    # return jsonify({'status': 'No selected file or file empty'})
    #


@app.route('/status/', methods=['POST'])
def status():
    return jsonify({'status': 'Server is working'})


###############################
#        MeetAI API           #
###############################
@app.route('/generate_image/', methods=['POST'])
def generate_image():
    pass


@app.route('/generate_text/', methods=['POST'])
def generate_text():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
