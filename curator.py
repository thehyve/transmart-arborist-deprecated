import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule('/favicon.ico',
                 redirect_to=url_for('static', filename='favicon.ico'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def columns_to_json(filename):
    import csv
    from collections import OrderedDict
    from flask import json
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        tree_array = []

        # Skipping header
        next(csvreader)

        for line in csvreader:
            path = line[1].split('+')
            i=0
            last = len(path)-1
            for part in path:
                if part != '':
                    part = part.replace('_',' ')
                    exists = False
                    for item in tree_array:
                        if item['text'] == part:
                            exists = True
                            break
                    if exists == False:
                        tree_array.append({'text':part})
                    # path_so_far = path[0:i]
                i+=1
        app.logger.debug(tree_array)
        return json.dumps(tree_array)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html')

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    json = columns_to_json(filename)
    app.logger.debug(json)
    return render_template('tree.html', json = json)
    # return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                            filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
