import os
from shutil import copyfile
from flask import json

SETTINGS_FILE = 'arborist-settings.json'
DEFAULT_STUDIES_FOLDER = 'studies'


def read_settings():
    TEMPLATE_SETTINGS_FILE = 'arborist-settings-default.json'

    if not os.path.isfile(SETTINGS_FILE):
        copyfile(TEMPLATE_SETTINGS_FILE, SETTINGS_FILE)
    with open(SETTINGS_FILE, 'rb') as data_file:
        settings = json.load(data_file)

    if 'studiesfolder' in settings:
        studiesfolder = settings['studiesfolder']
    else:
        if not os.path.isdir(DEFAULT_STUDIES_FOLDER):
            os.mkdir(DEFAULT_STUDIES_FOLDER)
        studiesfolder = DEFAULT_STUDIES_FOLDER
    studiesfolder = os.path.abspath(studiesfolder)
    settings['studiesfolder'] = studiesfolder

    return settings


def write_settings(newsettings):
    settings = read_settings()
    for setting in newsettings:
        settings[setting] = newsettings[setting]
    with open(SETTINGS_FILE, 'wb') as data_file:
        data_file.write(json.dumps(settings))
