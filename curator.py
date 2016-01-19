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
            if line[0] != '' and line[2] != '' and line[3] != '':
                if line[1] == '':
                    line[1] = 'OTHER'

                path = line[1].split('+')
                i = 0
                last = len(path)-1

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
                idpath = path + [leaf,line[0],line[2]]
                id = '+'.join(idpath)
                text = leaf.replace('_', ' ')
                parent = '+'.join(path)
                leafnode = {
                    'id': id,
                    'text': text,
                    'parent': parent,
                    'type': 'numeric',
                    'data':{
                        'Filename': line[0],
                        'Category Code': line[1],
                        'Column Number': line[2],
                        'Data Label': line[3]
                        }}
                if len(line) > 4:
                    leafnode['data']['Data Label Source'] = line[4]
                if len(line) > 5:
                    leafnode['data']['Control Vocab Cd'] = line[5]
                tree_array.append(leafnode)

        return json.dumps(tree_array)

def json_to_columns(json):
    app.logger.debug("test")

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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    json = columns_to_json(filename)
    return render_template('tree.html', json=json)

if __name__ == '__main__':
    app.debug = True
    app.run()
