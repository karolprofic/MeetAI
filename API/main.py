import pyttsx3
from flask import Flask, request, jsonify
from utilities import *
from openai import OpenAI
from converter.TextToSpeech import TextToSpeech
from converter.SpeechToText import SpeechToText

pyttsx = pyttsx3.init()
openAI = OpenAI()
openAI.api_key = "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"
project_directory = project_directory_path("MeetAI")

app = Flask(__name__)

stt = SpeechToText(project_directory, openAI)
tts = TextToSpeech(project_directory, pyttsx, openAI)


# TODO Refactor ImageGenerator
# TODO Implement TextGenerator
# TODO Finish Main Refactor
# TODO Check if current windows TTS work

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
            openAI.api_key = request_key
            return jsonify({'status': 'OpenAI API key added successfully'})
        case _:
            return jsonify({'status': 'Requested API is not supported'})


@app.route('/spech_to_text/', methods=['POST'])
def spech_to_text():
    pass


@app.route('/text_to_speach/', methods=['POST'])
def text_to_speach():
    pass


@app.route('/download_file/', methods=['POST'])
def download_file():
    pass


@app.route('/upload_file/', methods=['POST'])
def upload_file():
    pass


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
