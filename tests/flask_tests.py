import os
import arborist
import unittest
import tempfile
import shutil
import re


column_map_list = ['file1\tCharacteristic\t8\tAge',
                   'fil1\tCharacteristic\t9\tGender',
                   'f2\tSubjects\t1\tSUBJ_ID',
                   'f2\tMolecular profiling\KRAS()\t2\tGeneral_call',
                   'f3\tMolecular profiling_FKFK\t3\tNon-synonymous_mutations',
                   '',
                   ]


test_clin_params = ['COLUMN_MAP_FILE=col_map_file.tsv',
                    'SECURITY_REQUIRED=Y',
                    'STUDY_ID=test_study',
                    ]


class ArboristBaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        exec_path = os.path.split(os.path.abspath(__file__))[0]
        cls.url_prefix = '/folder/'
        cls.prefixed_path = cls.url_prefix + exec_path
        cls.tmp_root = tempfile.mkdtemp()
        cls.tmp_study = os.path.join(cls.tmp_root, 'test_study')
        cls.tmp_clinical = os.path.join(cls.tmp_study, 'clinical')
        cls.tmp_expression = os.path.join(cls.tmp_study, 'expression')
        cls.tmp_empty_study = os.path.join(cls.tmp_root, 'empty_study')
        temporary_dir_list = [cls.tmp_study,
                              cls.tmp_clinical,
                              cls.tmp_expression,
                              cls.tmp_empty_study,
                              ]
        for dir_name in temporary_dir_list:
            print("Creating tmp dir: {}".format(dir_name))
            os.mkdir(dir_name)
        cls.test_study_path = cls.url_prefix + cls.tmp_root + '/s/test_study'
        cls.empty_study_path = cls.url_prefix + cls.tmp_root + '/s/empty_study'
        with open(cls.tmp_clinical + '/col_map_file.tsv', 'w') as col_map_file:
            for line in column_map_list:
                col_map_file.write(line)
                col_map_file.write('\n')

        with open(cls.tmp_study + '/clinical.params', 'w') as clin_params:
            for line in test_clin_params:
                clin_params.write(line)
                clin_params.write('\n')

    @classmethod
    def tearDownClass(cls):
        print("Finished. Cleaning up temporary files.")
        shutil.rmtree(cls.tmp_root)

    def setUp(self):
        arborist.app.config['TESTING'] = True
        self.app = arborist.app.test_client()

    def test_if_root_redirect_works(self):
        rv = self.app.get('/', follow_redirects=True)
        assert b'Studies overview' in rv.data

    def test_navigator_working(self):
        path = arborist.single_forward_slashed(self.url_prefix + self.tmp_root)
        rv = self.app.get(path, follow_redirects=True)
        assert b'Studies overview' in rv.data

    def test_create_new_folder(self):
        path = arborist.single_forward_slashed(self.url_prefix + self.tmp_root + '/create/')
        form_data = dict(foldername='empty_test_folder')
        rv = self.app.post(path, follow_redirects=True, data=form_data)
        assert b'data-foldername="empty_test_folder"' in rv.data

    def test_create_clinical_params(self):
        clin_param_path = arborist.single_forward_slashed(self.empty_study_path + '/params/clinical/')
        create_path = arborist.single_forward_slashed(clin_param_path + '/create/')
        create_path = create_path[:-1]  # TODO fix this: Strips the last forward slash, else it wont create.
        form_data = dict(COLUMN_MAP_FILE='col_map_file.tsv',
                         SECURITY_REQUIRED='Y',
                         STUDY_ID='empty_study')
        rv = self.app.get(self.empty_study_path, follow_redirects=True)
        assert b'COLUMN_MAP_FILE:' not in rv.data
        rv = self.app.post(create_path, follow_redirects=True)
        assert b'Successfully created clinical.params.' in rv.data
        rv = self.app.post(clin_param_path, follow_redirects=True, data=form_data)
        assert b'Set variable COLUMN_MAP_FILE to ' in rv.data
        rv = self.app.get(self.empty_study_path, follow_redirects=True)
        assert b'COLUMN_MAP_FILE:' in rv.data

    def test_column_map_open_and_save(self):
        tree_view = arborist.single_forward_slashed(self.test_study_path + '/tree/')
        tree_save = arborist.single_forward_slashed(self.test_study_path + '/tree/save_columnsfile/')
        rv = self.app.get(tree_view, follow_redirects=True)
        assert rv.status == '200 OK'
        json = re.search(b'\[\{.*\}\]', rv.data).group(0)
        json = json.replace(b'"Category Code": "Characteristic",', b'"Category Code": "Characteristic_modified",')
        rv = self.app.post(tree_save, follow_redirects=True,
                           headers=[('X-Requested-With', 'XMLHttpRequest'),
                                    ('Referer', tree_view),
                                    ('Content-Type', 'application/json')],
                           data=json)
        assert b'Saved column mapping file' in rv.data

if __name__ == '__main__':
    unittest.main()
