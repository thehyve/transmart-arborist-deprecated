import os
from collections import OrderedDict

from flask import Flask, request, redirect, url_for, render_template, json, \
 Response, send_from_directory
from werkzeug import secure_filename

import urllib
from markupsafe import Markup

from functions.params import Study_params, Clinical_params
from functions.exceptions import HyveException, HyveIOException
from functions.clinical import columns_to_json, json_to_columns, getchildren

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

app = Flask(__name__)

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

columnmappingfilename = 'columns.txt'


@app.template_filter('urlencode')
def urlencode_filter(s):
    ''' Necessary addition to Jinja2 filters, to escape chars for in url '''
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/prepare_columnsfile', methods=['GET', 'POST'])
def prepare_columnsfile():
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


@app.route('/')
def index():
    return redirect(url_for('studies_overview_root'))


@app.route('/folder/')
def studies_overview_root():
    return studies_overview('')


@app.route('/folder/<path:studiesfolder>/')
def studies_overview(studiesfolder):
    studiesfolder = '/'+studiesfolder
    parentfolder = os.path.abspath(os.path.join(studiesfolder, os.pardir))
    studies = {}

    for file in os.listdir(studiesfolder):
        filepath = os.path.join(studiesfolder, file)
        if os.path.isdir(filepath) and not file.startswith('.'):
            studies[file] = {'type': 'folder'}
            studyparamsfile = os.path.join(filepath, 'study.params')
            clinicalparamsfile = os.path.join(filepath, 'clinical.params')
            if os.path.exists(studyparamsfile) or \
                    os.path.exists(clinicalparamsfile):
                studies[file]['type'] = 'study'
    orderedstudies = OrderedDict(sorted(studies.items(),
                                        key=lambda x: x[0].lower()))

    studiesfolder = studiesfolder.strip('/')
    parentfolder = parentfolder.strip('/')

    return render_template('studiesoverview.html',
                           studiesfolder=studiesfolder,
                           parentfolder=parentfolder,
                           studies=orderedstudies)


@app.route('/folder/<path:studiesfolder>/study/<study>/')
def study_page(studiesfolder, study):
    studiesfolder = '/'+studiesfolder
    app.logger.debug(studiesfolder)

    studyparamsfile = os.path.join(studiesfolder, study, 'study.params')
    try:
        studyparams = Study_params(studyparamsfile).get_variables()
    except (HyveException, HyveIOException) as e:
        studyparams = {type(e).__name__: str(e)}
    except IOError as e:
        studyparams = {}

    clinicalparamsfile = os.path.join(studiesfolder, study, 'clinical.params')
    try:
        clinicalparams = Clinical_params(clinicalparamsfile).get_variables()
    except (HyveException, HyveIOException) as e:
        clinicalparams = {type(e).__name__: str(e)}
    except IOError as e:
        clinicalparams = {}

    studiesfolder = studiesfolder.strip('/')

    return render_template('studypage.html',
                           studiesfolder=studiesfolder,
                           study=study,
                           studyparams=studyparams,
                           clinicalparams=clinicalparams)


# @app.route('/study/<study>/clinical/upload/', methods=['GET', 'POST'])
# def upload_file(study):
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('edit_tree',
#                                     filename=filename,
#                                     study=study))
#     return render_template('upload.html', study=study)


@app.route('/folder/<path:studiesfolder>/study/<study>/tree/')
def edit_tree(studiesfolder, study):
    studiesfolder = '/'+studiesfolder

    clinicalparamsfile = os.path.join(studiesfolder, study, 'clinical.params')
    try:
        clinicalparams = Clinical_params(clinicalparamsfile).get_variables()
    except (HyveException, HyveIOException) as e:
        clinicalparams = {type(e).__name__: str(e)}
    except IOError as e:
        clinicalparams = {}

    if 'COLUMN_MAP_FILE' in clinicalparams:
        columnsfile = clinicalparams['COLUMN_MAP_FILE']
        json = columns_to_json(columnsfile)
    else:
        json = {}

    studiesfolder = studiesfolder.strip('/')

    return render_template('tree.html',
                           studiesfolder=studiesfolder,
                           study=study,
                           json=json)


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
