import contextlib
import glob
import os


def project_directory_path(project_name):
    home_directory = os.path.expanduser('~')
    project_directory = os.path.join(home_directory, project_name)

    if not os.path.isdir(project_directory):
        os.mkdir(project_directory)

    return project_directory + '\\'


def clear_project_directory(project_name):
    project_directory = project_directory_path(project_name)
    if project_directory == '':
        return

    files = glob.glob(os.path.join(project_directory, "*"))
    for file in files:
        os.remove(file)


def sanitize(string):
    characters = ['\"', '\'', '\\', '\r']
    for char in characters:
        string = string.replace(char, " ")
    return string
