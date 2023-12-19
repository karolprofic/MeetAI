import soundfile
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


def set_environment_variables():
    if os.environ.get('OPENAI_API_KEY') is None:
        os.environ.setdefault('OPENAI_API_KEY', '')
