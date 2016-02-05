import os
from exceptions import HyveException, HyveIOException


class Params(object):
    """Base class for all Params files"""
    def __init__(self, filename, datatype, possible_variables):
        ''' Used to create a params representation

        Args:
            filename (str): String representation of the path of the
                params file.
            datatype (str): The datatype for this params file. Should be one of
                the reserved datatypes and should match the foldername of the
                datatype.
            possible variables (dict): A dictionary with possible variables
                for this params file. Each item of the dict should contain the
                variable name as key and as value a dict containing the
                variable parameters. All variable parameters are optional.
                The variable parameters can include:
                    obligatory (bool, default: False): Whether this variable
                        is obligatory.
                    variable_type (str): The type of the variable. Should be
                        one of the following:
                        'filename': Indicates the variable is a filename. This
                            will check whether this filename exists in a
                            subfolder (named afer the datatype) of the params
                            folder.
                    possible_values (array of str): array with the possible
                        values for this variable.
                    default (str): The default value when the variable is not
                        set.
                    helptext (str): Description of the variable for the user.
        '''

        self.directory = os.path.join(
                            os.path.dirname(os.path.abspath(filename)),
                            datatype)
        self.possible_variables = possible_variables
        self.feedback = feedback = {'errors': [], 'warnings': [], 'infos': []}

        with open(filename, 'r') as handle:
            for line in handle.readlines():
                line = line.split('#')[0].strip()
                if line == "" or line.startswith('#'):
                    continue
                line = line.strip()
                print line
                variable, value = line.split("=")

                value = value.strip("'").strip("\"")

                if variable in possible_variables:
                    if 'possible_values' in possible_variables[variable]:
                        if value not in \
                         possible_variables[variable]['possible_values']:
                            msg = '''Value {} is not in the possible values for
                            variable {}. Should be one of {}'''.format(
                                value, variable,
                                str(possible_variables[variable]
                                    ['possible_values']))
                            feedback['errors'].append(msg)

                    if 'variable_type' in possible_variables[variable]:
                        # Check for existance of file (and ignore filename 'x')
                        if possible_variables[variable]['variable_type'] == \
                                'filename' and value.lower() != 'x':
                            value = os.path.join(self.directory, value)
                            if not os.path.exists(value):
                                msg = "The {} file {} doesn't exist.".format(
                                    variable, value)
                                feedback['errors'].append(msg)
                    setattr(self, variable, value)
                else:
                    msg = "{} doesn't have the variable {}".format(
                        self.__class__, variable)
                    print msg

        for variable in possible_variables:
            if 'obligatory' in possible_variables[variable]:
                if possible_variables[variable]['obligatory']:
                    if not hasattr(self, variable):
                        msg = "{} not in {}".format(variable, filename)
                        feedback['errors'].append(msg)

    def __str__(self):
        variablesvalues = self.get_variables()
        return str(self.__class__) + ": " + str(variablesvalues)

    def get_variables(self):
        variablesvalues = {}
        for variable in self.possible_variables:
            try:
                variablesvalues[variable] = getattr(self, variable)
            except Exception as e:
                print("no variable "+variable)
        return variablesvalues

    def get_possible_variables(self):
        return self.possible_variables

    def get_feedback(self):
        return self.feedback


class Study_params(Params):
    """Class for study.params file"""
    def __init__(self, filename):
        possible_variables = {
                                'SECURITY_REQUIRED': {
                                    'possible_values': ['Y', 'N'],
                                    'default': 'N',
                                    'helptext': ('Defines study as Private (Y)'
                                                 ' or Public (N).')
                                },
                                'TOP_NODE': {
                                    'default': ('\(Public|Private) Studies'
                                                '\<STUDY_ID>'),
                                    'helptext': 'The study top node.'
                                },
                                'STUDY_ID': {
                                    'default': ('Uppercased parent directory'
                                                'name of the params file is'
                                                ' default.'),
                                    'helptext': 'Identifier of the study.'
                                },
                                'STUDY_NAME': {}
                             }
        # Not a datatype, but to stay in line with the datatype params:
        datatype = 'study'
        super(Study_params, self).__init__(filename,
                                           datatype,
                                           possible_variables)


class Clinical_params(Params):
    """Class for clinical.params file"""
    def __init__(self, filename):
        possible_variables = {
                                'COLUMN_MAP_FILE': {
                                    'obligatory': True,
                                    'variable_type': 'filename',
                                    'helptext': 'Points to the column file.'
                                    },
                                'WORD_MAP_FILE': {
                                    'variable_type': 'filename',
                                    'helptext': ('Points to the file with'
                                                 ' dictionary to be used.')
                                    },
                                "SECURITY_REQUIRED": {
                                    'possible_values': ['Y', 'N'],
                                },
                                "TOP_NODE": {},
                                "STUDY_ID": {},
                                "XTRIAL_FILE": {
                                    'helptext': ('Points to the cross study'
                                                 ' concepts file.')
                                },
                                "TAGS_FILE": {
                                    'variable_type': 'filename',
                                    'helptext': ('Points to the concepts tags'
                                                 ' file.')
                                },
                                "RECORD_EXCLUSION_FILE": {
                                    'variable_type': 'filename'
                                },
                                "USE_R_UPLOAD": {
                                    'possible_values': ['Y', 'N']
                                },
                                "TOP_NODE_PREFIX": {}
                              }
        datatype = 'clinical'
        super(Clinical_params, self).__init__(filename,
                                              datatype,
                                              possible_variables)
