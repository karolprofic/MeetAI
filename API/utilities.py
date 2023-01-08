import contextlib
import glob
import os
import wave


def create_project_directory_path(project_name):
    home_directory = os.path.expanduser('~')
    project_directory = os.path.join(home_directory, project_name)

    if not os.path.isdir(project_directory):
        os.mkdir(project_directory)

    return project_directory


def clear_project_directory(project_name):
    project_directory = create_project_directory_path(project_name)
    if project_directory == '':
        return

    files = glob.glob(os.path.join(project_directory, "*"))
    for file in files:
        os.remove(file)


def audio_duration(src):
    with contextlib.closing(wave.open(src, 'r')) as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration = frames / float(rate)
        return duration


def sanitize(string):
    characters = ['\"', '\'', '\\', '\r']
    for char in characters:
        string = string.replace(char, " ")
    return string


def change_voice(tts_engine, language, gender):
    for voice in tts_engine.getProperty('voices'):
        if language in voice.name:
            if gender == 0 and ("Zira" in voice.name or "Hazel" in voice.name):
                tts_engine.setProperty('voice', voice.id)
                return True
            if gender == 1 and "David" in voice.name:
                tts_engine.setProperty('voice', voice.id)
                return True
    return False
