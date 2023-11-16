import pyttsx3 as pyttsx3
from utilities import *
from openai import OpenAI
from converter.TextToSpeech import TextToSpeech

project_directory = project_directory_path("MeetAI")
openAI = OpenAI(api_key="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")
# openAI = OpenAI(api_key="sk-ffffffffffffffffffff")
pyttsx = pyttsx3.init()

tts = TextToSpeech(project_directory, pyttsx, openAI)
print(tts.generate("openai_tts", "alloy", "Unable to find model or voice name"))

# TODO Setting API Key during setup and check





# ig = ImageGenerator("cuda", project_directory)
# ig.generate("stabilityai/stable-diffusion-2", "dog")
#
#
#
#
# app = Flask(__name__)
#
# app.secret_key = "secret key"  # todo ?
# app.config['PROJECT_DIRECTORY'] = project_directory_path("MeetAI")
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # todo ?
#
# # TODO: Remove unneeded app.config
# # TODO: Text generator (voice gender input) + cpp generated in ue5
# # TODO: Utilities refactor
# # TODO: Main refactor
#
#
# @app.route('/status', methods=['GET', 'POST'])
# def status():
#     return jsonify({'status': 0, 'description': 'Server is working'})
#
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return jsonify({'status': 1, 'description': 'No file part in the request'})
#
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'status': 2, 'description': 'No file selected for uploading'})
#
#     file.save(os.path.join(app.config['PROJECT_DIRECTORY'], file.filename))
#     return jsonify({'status': 0, 'description': 'File successfully uploaded'})
#
#
# @app.route('/download/<file_name>', methods=['GET'])
# def download(file_name):
#     file_path = os.path.join(app.config['PROJECT_DIRECTORY'], file_name)
#     file_type = file_path[-3:]
#
#     if file_type != "png" and file_type != "wav":
#         return Response(status=400)
#
#     if not os.path.exists(file_path):
#         return Response(status=404)
#
#     with open(file_path, mode='rb') as file:
#         file_content = file.read()
#         file_bytes = BytesIO(file_content)
#         file_wrapper = FileWrapper(file_bytes)
#         if file_type == "png":
#             return Response(file_wrapper, mimetype="image/png", direct_passthrough=True, status=200)
#         if file_type == "wav":
#             return Response(file_wrapper, mimetype="converter/wav", direct_passthrough=True, status=200)
#
#     return Response(status=404)
#
#
# @app.route('/dummy_image_generation', methods=['GET', 'POST'])
# def status():
#     return jsonify({
#         'status': 0,
#         'description': 'Image generated successfully',
#         'file_name': "example.png"
#     })
#
#
# @app.route('/dummy_text_generation', methods=['GET', 'POST'])
# def status():
#     return jsonify({
#         'status': 0,
#         'description': 'Text generated successfully',
#         'text': "Sure, I'd recommend the movie 'Inception' directed by Christopher Nolan.",
#         'converter': "speach.wav"
#     })
#
#
#
# # image genraion
# # text generaion
# # request_data = request.get_json()
# # request_text = request_data["text"]
# # request_voice = int(request_data["voice"])
# # request_rate = int(request_data["rate"])
# #
# # if request_text is None or request_voice is None or request_rate is None or request_text == "":
# #     return jsonify({'status': 'Unable to generate speech', 'src': '-', 'len': 0.0})
# #
# # if request_voice != 0 and request_voice != 1:
# #     return jsonify({'status': 'Unable to generate speech', 'src': '-', 'len': 0.0})
#
# # #
# # @app.route('/experiment/', methods=['POST'])
# # def experiment():
# #     try:
# #         requests_toolbelt.MultipartDecoder
# #
# #         request_json = json.loads(request.values.get('json'))
# #         input_type = request_json["InputType"]
# #         input_content = request_json["InputContent"]
# #
# #         if input_type == "Microphone":
# #             # TODO: Audio to text
# #             uploaded_file = request.files['file']
# #             if uploaded_file.filename != '':
# #                 uploaded_file.save(uploaded_file.filename)
# #             else:
# #                 return jsonify({'status': 'file error'})
# #             # TODO: Implementation
# #             return jsonify({'status': 'succ'})
# #
# #         if input_type == "Keyboard":
# #             if input_content == "":
# #                 return jsonify({'status': 'content empty'})
# #             # TODO: Implementation
# #             return jsonify({'status': 'succ'})
# #
# #         return jsonify({'status': 'unable to parse input_type'})
# #
# #     except:
# #         return jsonify({'status': 'python script throw exception '})
# #
# #
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
