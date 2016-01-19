import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

app = Flask(__name__)
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
            if line[0] != '':
                path = line[1].split('+')
                i = 0
                last = len(path)-1

                for part in path:
                    if i == 0:
                        parent = '#'
                    else:
                        parent = '+'.join(path[0:i])
                    exists = False
                    for item in tree_array:
                        if item['text'] == part.replace('_', ' '):
                            exists = True
                            break
                    if not exists:
                        id = '+'.join(path[0:i+1])
                        tree_array.append({
                            'id': id,
                            'text': part.replace('_', ' '),
                            'parent': parent
                            })
                    i += 1

                leaf = line[3].replace('_', ' ')
                idpath = path + [leaf]
                id = '+'.join(idpath)
                parent = '+'.join(path)
                tree_array.append({
                    'id': id,
                    'text': leaf,
                    'parent': parent,
                    'type': 'numeric'})

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
    return render_template('tree.html', json=json)

if __name__ == '__main__':
    app.debug = True
    app.run()
