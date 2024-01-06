from datetime import datetime
import soundfile
import base64
import json
import glob
import os


def create_project_directory(project_name):
    home_directory = os.path.expanduser('~')
    project_directory = os.path.join(home_directory, project_name)

    if not os.path.isdir(project_directory):
        os.mkdir(project_directory)

    return project_directory + '\\'


def clear_project_directory(project_name):
    project_directory = create_project_directory(project_name)
    if project_directory == '':
        return

    files = glob.glob(os.path.join(project_directory, "*"))
    for file in files:
        os.remove(file)


def resample_file(input_path, output_path):
    data, samplerate = soundfile.read(input_path)
    soundfile.write(output_path, data, samplerate, subtype='PCM_16')


def load_config():
    try:
        with open('./environment/config.env', 'r') as file:
            current_config = json.load(file)
    except Exception as e:
        print(f"Load config error: {e}")
        return

    for key, value in current_config.items():
        os.environ[key] = value

    return current_config


def save_config(current_config):
    with open('./environment/config.env', 'w') as file:
        json.dump(current_config, file, indent=4)


def load_image_and_encode(filepath):
    with open(filepath, "rb") as file:
        file_binary = file.read()

    file_base64 = base64.b64encode(file_binary)
    file_base64_utf8 = file_base64.decode('utf-8')
    return file_base64_utf8


def save_file_and_decode(project_directory, request_query):
    filename = datetime.now().strftime(f"query_%d-%m-%Y_%H-%M-%S.wav")
    filepath = project_directory + filename
    file_decoded = base64.b64decode(request_query)

    with open(filepath, "wb") as file:
        file.write(file_decoded)

    return filename


def sanitize(string):
    characters = ['\"', '\'', '\\', '\r']
    for char in characters:
        string = string.replace(char, " ")
    return string
