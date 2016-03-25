import csv
import os

from .feedback import get_feedback_dict
from .params import ClinicalParams


outoftree = 'OUT OF TREE'

filenamelabel = 'Filename'
filenamecolumn = 0
categorycodelabel = 'Category Code'
categorycodecolumn = 1
columnnumberlabel = 'Column Number'
columnnumbercolumn = 2
datalabellabel = 'Data Label'
datalabelcolumn = 3
datalabelsourcelabel = 'Data Label Source'
datalabelsourcecolumn = 4
controlvocabcdlabel = 'Control Vocab Cd'
controlvocabcdcolumn = 5
columnsfileheaders = [filenamelabel, categorycodelabel, columnnumberlabel,
                      datalabellabel, datalabelsourcelabel,
                      controlvocabcdlabel]
wordmapheaders = ['Filename', 'Column Number', 'Original Data Value',
                  'New Data Value']


def columns_not_present(line, column_list):
    """Return True if one or more of column_list are not present"""
    if len(line) == 0:
        return False
    for column in column_list:
        if line[column] == '':
            return False
    return True


def columns_to_tree(filename):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        tree_array = []

        # Skipping header
        next(csvreader)

        for line in csvreader:
            # Skip lines without filename, column number or data label
            if columns_not_present(line, [filenamecolumn, columnnumbercolumn, datalabelcolumn]):
                # If categorycode is empty this is a special concept that is
                # not in the tree
                # Eg SUBJ_ID, STUDY_ID, OMIT or DATA LABEL

                path = line[categorycodecolumn].replace(' ', '_').split('+')
                i = 0

                # Create folders for all parts in the categorycode path
                if path != ['']:
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

                # Add the leaf node
                leaf = line[datalabelcolumn]

                if path != ['']:
                    parent = '+'.join(path)
                else:
                    parent = '#'

                idpath = [leaf, line[filenamecolumn], line[columnnumbercolumn]]
                id = '+'.join(idpath)

                text = leaf.replace('_', ' ')
                leafnode = {
                    'id': id,
                    'text': text,
                    'parent': parent,
                    'type': 'numeric',
                    'data': {
                        filenamelabel:     line[filenamecolumn],
                        categorycodelabel: line[categorycodecolumn],
                        columnnumberlabel: line[columnnumbercolumn],
                        datalabellabel:    line[datalabelcolumn]
                        }}
                if len(line) > 4:
                    leafnode['data'][datalabelsourcelabel] = \
                        line[datalabelsourcecolumn]
                if len(line) > 5:
                    leafnode['data'][controlvocabcdlabel] = \
                        line[controlvocabcdcolumn]
                if text in ['SUBJ ID', 'STUDY ID', 'DATA LABEL', 'DATALABEL',
                            'OMIT']:
                    leafnode['type'] = 'codeleaf'
                tree_array.append(leafnode)

        return tree_array


def getchildren(node, columnsfile, path, feedback):
    node_type = node.get('type', 'default')
    node_children = node.get('children', [])

    if node_type == 'numeric' or node_type == 'alpha' or node_type == 'codeleaf':
        filename = node['data'][filenamelabel]

        # Error handling for clinical concepts
        if len(node['text']) != len(node['text'].strip()):
            feedback['errors'].append(('The concept \'{}\' under folder \'{}\''
                                       ' contains leading or trailing'
                                       ' whitespace.')
                                      .format(node['text'], "/".join(path)))

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
        return columnsfile, feedback
    elif node_type == 'default':
        path = path + [node['text']]

        # Error handling for folders
        for char in ['+', '/', '\'']:
            if char in node['text']:
                feedback['errors'].append(('The folder \'{}\' contains a '
                                           '\'{}\' symbol, which will give'
                                           ' problems when loading data.')
                                          .format("/".join(path), char))
        if len(node['text']) != len(node['text'].strip()):
            feedback['errors'].append(('The folder \'{}\' contains leading or'
                                       ' trailing whitespace.')
                                      .format("/".join(path)))
        if not node_children:
            feedback['warnings'].append(('The folder \'{}\' has no children'
                                         ' and will thus be ignored.')
                                        .format("/".join(path)))

        for child in node_children:
            columnsfile, feedback = getchildren(child, columnsfile, path,
                                                feedback)
        return columnsfile, feedback
    else:
        return columnsfile, feedback


def json_to_columns(tree):
    columnsfile = []
    path = []
    feedback = get_feedback_dict()

    for node in tree:
        columnsfile, feedback = getchildren(node, columnsfile, path, feedback)

    # Sort on column number and filename
    columnsfile = sorted(columnsfile, key=lambda x: x[columnnumbercolumn])
    columnsfile = sorted(columnsfile, key=lambda x: x[filenamecolumn])

    columnsfiledata = '\t'.join(columnsfileheaders)+'\n'
    for row in columnsfile:
        columnsfiledata += '\t'.join(map(str, row))+'\n'

    return columnsfiledata, feedback


def get_datafiles(columnfilename):
    datafiles = set()

    with open(columnfilename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(csvreader)
        for line in csvreader:
            if len(line) > 0:
                datafiles.add(line[filenamecolumn])

    return datafiles


def get_column_map_file(studiesfolder, study):
    clinicalparamsfile = os.path.join(studiesfolder, study, 'clinical.params')
    paramsobject = ClinicalParams(clinicalparamsfile)
    if paramsobject is not None:
        columnsfile = paramsobject.get_variable_path('COLUMN_MAP_FILE')
        return columnsfile
    else:
        return


def add_to_column_file(datafilename, columnmappingfilename):
    with open(datafilename, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        headerline = next(csvreader)
        with open(columnmappingfilename, "a") as columnmappingfile:
            i = 1
            for header in headerline:
                filename = os.path.basename(datafilename)
                folder = os.path.splitext(filename)[0]
                columnmappingfile.write('\t'.join([filename, folder, str(i),
                                        header, '', ''])+'\n')
                i += 1


def get_word_map():
    wordmapdata = '\t'.join(wordmapheaders)+'\n'
    return wordmapdata
