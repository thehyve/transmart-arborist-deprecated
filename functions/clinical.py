import csv
import os
from flask import json

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


def columns_to_json(filename):
    with open(filename, 'rb') as \
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
