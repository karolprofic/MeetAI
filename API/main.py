from io import BytesIO
from wsgiref.util import FileWrapper
from flask import Flask, request, jsonify, Response, send_from_directory
from utilities import *

from ai.image_generator import ImageGenerator

app = Flask(__name__)

app.secret_key = "secret key"  # todo ?
app.config['PROJECT_DIRECTORY'] = create_project_directory_path("MeetAI")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # todo ?


@app.route('/status', methods=['GET', 'POST'])
def status():
    return jsonify({'status': 0, 'description': 'Server is working'})


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'status': 1, 'description': 'No file part in the request'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 2, 'description': 'No file selected for uploading'})

    file.save(os.path.join(app.config['PROJECT_DIRECTORY'], file.filename))
    return jsonify({'status': 0, 'description': 'File successfully uploaded'})


@app.route('/download/<file_name>', methods=['GET'])
def download(file_name):
    file_path = os.path.join(app.config['PROJECT_DIRECTORY'], file_name)
    file_type = file_path[-3:]

    if file_type != "png" and file_type != "wav":
        return Response(status=400)

    if not os.path.exists(file_path):
        return Response(status=404)

    with open(file_path, mode='rb') as file:
        file_content = file.read()
        file_bytes = BytesIO(file_content)
        file_wrapper = FileWrapper(file_bytes)
        if file_type == "png":
            return Response(file_wrapper, mimetype="image/png", direct_passthrough=True, status=200)
        if file_type == "wav":
            return Response(file_wrapper, mimetype="audio/wav", direct_passthrough=True, status=200)

    return Response(status=404)


@app.route('/dummy_image_generation', methods=['GET', 'POST'])
def status():
    return jsonify({
        'status': 0,
        'description': 'Image generated successfully',
        'file_name': "example.png"
    })


@app.route('/dummy_text_generation', methods=['GET', 'POST'])
def status():
    return jsonify({
        'status': 0,
        'description': 'Text generated successfully',
        'text': "Sure, I'd recommend the movie 'Inception' directed by Christopher Nolan.",
        'audio': "speach.wav",
        'timestamps': [
            {"conf": 1, "end": 0.6, "start": 0.09, "word": "sure"},
            {"conf": 1, "end": 1.11, "start": 0.93, "word": "i'd"},
            {"conf": 1, "end": 1.59, "start": 1.11, "word": "recommend"},
            {"conf": 1, "end": 1.68, "start": 1.59, "word": "the"},
            {"conf": 1, "end": 2.04, "start": 1.68, "word": "movie"},
            {"conf": 1, "end": 2.58, "start": 2.04, "word": "inception"},
            {"conf": 1, "end": 3.09, "start": 2.58, "word": "directed"},
            {"conf": 1, "end": 3.24, "start": 3.09, "word": "by"},
            {"conf": 1, "end": 3.81, "start": 3.24, "word": "christopher"},
            {"conf": 1, "end": 4.26, "start": 3.81, "word": "nolan"}
        ]
    })



# image genraion
# text generaion


#
# @app.route('/experiment/', methods=['POST'])
# def experiment():
#     try:
#         requests_toolbelt.MultipartDecoder
#
#         request_json = json.loads(request.values.get('json'))
#         input_type = request_json["InputType"]
#         input_content = request_json["InputContent"]
#
#         if input_type == "Microphone":
#             # TODO: Audio to text
#             uploaded_file = request.files['file']
#             if uploaded_file.filename != '':
#                 uploaded_file.save(uploaded_file.filename)
#             else:
#                 return jsonify({'status': 'file error'})
#             # TODO: Implementation
#             return jsonify({'status': 'succ'})
#
#         if input_type == "Keyboard":
#             if input_content == "":
#                 return jsonify({'status': 'content empty'})
#             # TODO: Implementation
#             return jsonify({'status': 'succ'})
#
#         return jsonify({'status': 'unable to parse input_type'})
#
#     except:
#         return jsonify({'status': 'python script throw exception '})
#
#

ig = ImageGenerator("cuda", "./")
ig.generate("stabilityai/stable-diffusion-2", "dog")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
