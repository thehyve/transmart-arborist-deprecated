import os


class HyveIOException(Exception):
    pass


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
                variable parameters.
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
        '''

        self.directory = os.path.join(
                            os.path.dirname(os.path.abspath(filename)),
                            datatype)
        self.possible_variables = possible_variables

        with open(filename, 'r') as handle:
            for line in handle.readlines():
                if line == "" or line.startswith('#'):
                    continue
                line = line.strip()
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
                            raise HyveIOException(msg)

                    if 'variable_type' in possible_variables[variable]:
                        # Check for existance of file (and ignore filename 'x')
                        if possible_variables[variable]['variable_type'] == \
                                'filename' and value.lower() != 'x':
                            value = os.path.join(self.directory, value)
                            if not os.path.exists(value):
                                msg = "The {} file {} doesn't exist.".format(
                                    variable, value)
                                raise HyveIOException(msg)
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
                        raise HyveException(msg)

    def __str__(self):
        variablesvalues = {}
        for variable in self.possible_variables:
            try:
                variablesvalues[variable] = getattr(self, variable)
            except Exception as e:
                print("no variable "+variable)
        return str(self.__class__) + ": " + str(variablesvalues)


class Study_params(Params):
    """Class for study.params file"""
    def __init__(self, filename):
        possible_variables = {
                                'SECURITY_REQUIRED': {
                                    'possible_values': ['Y', 'N']
                                },
                                'TOP_NODE': {},
                                'STUDY_ID': {},
                                'STUDY_NAME': {}
                             }
        # Not a datatype, but to stay in line with the datatype params:
        datatype = 'study'
        super(Study_params, self).__init__(filename,
                                           datatype,
                                           possible_variables)


class Clinical_params(Params):
    def __init__(self, filename, batch=False, all_none=True):
        ''' batch and all_none are in here for legacy purposes  '''
        possible_variables = {
                                'COLUMN_MAP_FILE': {
                                    'obligatory': True,
                                    'variable_type': 'filename'
                                    },
                                'WORD_MAP_FILE': {
                                    'variable_type': 'filename'
                                    },
                                "SECURITY_REQUIRED": {},
                                "TOP_NODE": {},
                                "STUDY_ID": {},
                                "XTRIAL_FILE": {},
                                "TAGS_FILE": {
                                    'variable_type': 'filename'
                                },
                                "RECORD_EXCLUSION_FILE": {
                                    'variable_type': 'filename'
                                },
                                "USE_R_UPLOAD": {},
                                "TOP_NODE_PREFIX": {}
                              }
        datatype = 'clinical'
        super(Clinical_params, self).__init__(filename,
                                              datatype,
                                              possible_variables)
