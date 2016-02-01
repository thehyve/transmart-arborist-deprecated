import os
import csv
from flask import Flask, request, redirect, url_for, render_template, json, \
 Response, send_from_directory
from werkzeug import secure_filename
from collections import OrderedDict
from shutil import copyfile
from functions.params import Study_params, Clinical_params
from functions.exceptions import HyveException, HyveIOException


UPLOAD_FOLDER = 'files'
DEFAULT_STUDIES_FOLDER = 'studies'
SETTINGS_FILE = 'arborist-settings.json'
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

app = Flask(__name__)

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
if not os.path.isdir(DEFAULT_STUDIES_FOLDER):
    os.mkdir(DEFAULT_STUDIES_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

outoftree = 'OUT OF TREE'
filenamelabel = 'Filename'
categorycodelabel = 'Category Code'
columnnumberlabel = 'Column Number'
datalabellabel = 'Data Label'
datalabelsourcelabel = 'Data Label Source'
controlvocabcdlabel = 'Control Vocab Cd'
columnsfileheaders = [filenamelabel, categorycodelabel, columnnumberlabel,
                      datalabellabel, datalabelsourcelabel,
                      controlvocabcdlabel]
columnmappingfilename = 'columns.txt'


def read_settings():
    TEMPLATE_SETTINGS_FILE = 'arborist-settings-default.json'

    if not os.path.isfile(SETTINGS_FILE):
        copyfile(TEMPLATE_SETTINGS_FILE, SETTINGS_FILE)
    with open(SETTINGS_FILE, 'rb') as data_file:
        settings = json.load(data_file)

    if 'studiesfolder' in settings:
        studiesfolder = settings['studiesfolder']
    else:
        studiesfolder = DEFAULT_STUDIES_FOLDER

    return settings


def write_settings(newsettings):
    settings = read_settings()
    for setting in newsettings:
        settings[setting] = newsettings[setting]
    with open(SETTINGS_FILE, 'wb') as data_file:
        data_file.write(json.dumps(settings))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def columns_to_json(filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as \
     csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        tree_array = []

        # Skipping header
        next(csvreader)

        for line in csvreader:
            # Skip lines without filename, column number or data label
            if line[0] != '' and line[2] != '' and line[3] != '':
                # If categorycode is empty this is a special concept that is
                # not in the tree
                # Eg SUBJ_ID, STUDY_ID, OMIT or DATA LABEL
                if line[1] == '':
                    line[1] = outoftree

                path = line[1].split('+')
                i = 0

                for part in path:
                    if i == 0:
                        parent = '#'
                    else:
                        parent = '+'.join(path[0:i])

                    id = '+'.join(path[0:i+1])

                    exists = False
                    for item in tree_array:
                        if item['id'] == id:
                            exists = True
                            break

                    if not exists:
                        text = part.replace('_', ' ')
                        tree_array.append({
                            'id': id,
                            'text': text,
                            'parent': parent
                            })

                    i += 1

                leaf = line[3]
                idpath = path + [leaf, line[0], line[2]]
                id = '+'.join(idpath)
                text = leaf.replace('_', ' ')
                parent = '+'.join(path)
                leafnode = {
                    'id': id,
                    'text': text,
                    'parent': parent,
                    'type': 'numeric',
                    'data': {
                        filenamelabel:     line[0],
                        categorycodelabel: line[1],
                        columnnumberlabel: line[2],
                        datalabellabel:    line[3]
                        }}
                if len(line) > 4:
                    leafnode['data'][datalabelsourcelabel] = line[4]
                if len(line) > 5:
                    leafnode['data'][controlvocabcdlabel] = line[5]
                if text in ['SUBJ ID', 'STUDY ID', 'DATA LABEL', 'DATALABEL',
                            'OMIT']:
                    leafnode['type'] = 'codeleaf'
                tree_array.append(leafnode)

        return json.dumps(tree_array)


def getchildren(node, columnsfile, path):
    if node['type'] != 'default' and node['type'] != 'highdim':
        filename = node['data'][filenamelabel]
        if path == [outoftree]:
            categorycode = ''
        else:
            categorycode = '+'.join(path).replace(' ', '_')
        columnnumber = int(node['data'][columnnumberlabel])
        datalabel = node['text'].replace(' ', '_')
        if datalabelsourcelabel in node['data']:
            datalabelsource = node['data'][datalabelsourcelabel]
        else:
            datalabelsource = ''
        if controlvocabcdlabel in node['data']:
            controlvocabcd = node['data'][controlvocabcdlabel]
        else:
            controlvocabcd = ''

        columnsfile.append([filename, categorycode, columnnumber, datalabel,
                            datalabelsource, controlvocabcd])
        return columnsfile
    else:
        path = path + [node['text']]
        for child in node['children']:
            columnsfile = getchildren(child, columnsfile, path)
        return columnsfile


def json_to_columns(tree):
    columnsfile = []
    path = []
    for node in tree:
        columnsfile = getchildren(node, columnsfile, path)

    # Sort on column number and filename
    columnsfile = sorted(columnsfile, key=lambda x: x[2])
    columnsfile = sorted(columnsfile, key=lambda x: x[0])

    columnsfiledata = '\t'.join(columnsfileheaders)+'\n'
    for row in columnsfile:
        columnsfiledata += '\t'.join(map(str, row))+'\n'
    return columnsfiledata


@app.route('/prepare_columnsfile', methods=['GET', 'POST'])
def prepare_columnsfile():
    # app.logger.debug("tree = "+ str(request.get_json()))

    tree = request.get_json()
    tree = json_to_columns(tree)

    columnmappingfile = open(os.path.join(app.config['UPLOAD_FOLDER'],
                                          columnmappingfilename), 'wb')
    columnmappingfile.write(tree)

    return json.jsonify(columnsfile=columnmappingfilename)


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def studies_overview():
    if request.method == 'POST':
        newstudiesfolder = request.form['studiesfolder']
        if os.path.isdir(newstudiesfolder):
            newsettings = {'studiesfolder': newstudiesfolder}
            write_settings(newsettings)
    settings = read_settings()
    studiesfolder = settings['studiesfolder']
    studies = []
    for file in os.listdir(studiesfolder):
        if os.path.isdir(os.path.join(studiesfolder, file)):
            studies = studies + [file]
    return render_template('studiesoverview.html',
                           studiesfolder=studiesfolder,
                           studies=studies)


@app.route('/study/<study>/')
def study_page(study):
    settings = read_settings()
    studiesfolder = settings['studiesfolder']

    studyparamsfile = os.path.join(studiesfolder, study, 'study.params')
    try:
        studyparams = Study_params(studyparamsfile).get_variables()
    except (HyveException, HyveIOException) as e:
        studyparams = {'HyveException': str(e)}
    except IOError as e:
        studyparams = {}

    clinicalparamsfile = os.path.join(studiesfolder, study, 'clinical.params')
    try:
        clinicalparams = Clinical_params(clinicalparamsfile).get_variables()
    except (HyveException, HyveIOException) as e:
        clinicalparams = {'HyveException': str(e)}
    except IOError as e:
        clinicalparams = {}

    return render_template('studypage.html',
                           study=study,
                           studyparams=studyparams,
                           clinicalparams=clinicalparams)


@app.route('/study/<study>/clinical/upload/', methods=['GET', 'POST'])
def upload_file(study):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('edit_tree',
                                    filename=filename, study=study))
    return render_template('upload.html')


@app.route('/study/<study>/tree/<filename>')
def edit_tree(study, filename):
    json = columns_to_json(filename)
    return render_template('tree.html', study=study, json=json)


@app.errorhandler(404)
def errorhandler(e):
    code = 404
    return render_template('error.html', error=str(e), code=code), code


@app.errorhandler(403)
def errorhandler(e):
    code = 403
    return render_template('error.html', error=str(e), code=code), code


@app.errorhandler(410)
def errorhandler(e):
    code = 410
    return render_template('error.html', error=str(e), code=code), code


@app.errorhandler(500)
def errorhandler(e):
    code = 500
    return render_template('error.html', error=str(e), code=code), code

if __name__ == '__main__':
    app.debug = True
    app.run()
