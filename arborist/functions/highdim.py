import csv
import os

from params import Expression_params

subject_sample_map_headers = ['STUDY_ID', 'SITE_ID', 'SUBJECT_ID', 'SAMPLE_ID',
                              'PLATFORM', 'TISSUETYPE', 'ATTR1', 'ATTR2',
                              'CATEGORY_CD', 'SOURCE_CD']

studyidcolumn = 0
siteidcolumn = 1
subjectidcolumn = 2
sampleidcolumn = 3
platformcolumn = 4
tissuetypecolumn = 5
attr1column = 6
attr2column = 7
categorycodecolumn = 8
sourcecdcolumn = 9


def subject_sample_to_tree(filename, tree_array):

    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        # Skipping header
        next(csvreader)

        for line in csvreader:

            path = line[categorycodecolumn].replace(' ', '_').split('+')
            leaf = path[-1]
            path = path[:-1]
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
            if path != ['']:
                parent = '+'.join(path)
            else:
                parent = '#'

            idpath = path + [leaf]
            id = '+'.join(idpath)

            # TODO store the data values for all samples in subject_sample_map

            exists = False
            for item in tree_array:
                if item['id'] == id:
                    exists = True
                    break

            if not exists:
                text = leaf.replace('_', ' ')
                leafnode = {
                    'id': id,
                    'text': text,
                    'parent': parent,
                    'type': 'highdim',
                    'data': {}}

                i = 0
                for header in subject_sample_map_headers:
                    leafnode['data'][header] = line[i]
                    i += 1

                tree_array.append(leafnode)

    return tree_array


def get_subject_sample_map(studiesfolder, study, datatype):
    if datatype == 'expression':
        expressionparamsfile = os.path.join(studiesfolder,
                                            study,
                                            'expression.params')
        paramsobject = Expression_params(expressionparamsfile)
        if paramsobject is not None:
            subject_sample_map = paramsobject.get_variable_path('MAP_FILENAME')
            return subject_sample_map
        else:
            return
