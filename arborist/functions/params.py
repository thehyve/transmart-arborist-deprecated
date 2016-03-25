import os

from .exceptions import HyveException, HyveIOException
from .feedback import get_feedback_dict, merge_feedback_dicts


class Params(object):
    """Base class for all Params files"""
    def __init__(self, filename, datatype, possible_variables):
        """ Used to create a params representation

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
                    mandatory (bool, default: False): Whether this variable
                        is mandatory.
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
        """

        study_specific_possible_variables = {
            "SECURITY_REQUIRED": {
                'possible_values': ['Y', 'N'],
                'default': 'N',
                'helptext': ('Defines study as Private (Y) or Public (N).')
            },
            "TOP_NODE": {
                'default': ('\(Public|Private) Studies\<STUDY_ID>'),
                'helptext': 'The study top node.'
            },
            "STUDY_ID": {
                'default': ('Uppercased parent directory name of the params'
                            ' file is default.'),
                'helptext': 'Identifier of the study.'
            }
        }

        possible_variables.update(study_specific_possible_variables)

        self.directory = os.path.join(
                            os.path.dirname(os.path.abspath(filename)),
                            datatype)
        self.study_directory = os.path.dirname(os.path.abspath(filename))
        self.datatype = datatype
        self.possible_variables = possible_variables
        self.feedback = get_feedback_dict()

        with open(filename, 'r') as handle:
            for line in handle.readlines():
                line = line.split('#')[0].strip()
                if line == "" or line.startswith('#'):
                    continue
                line = line.strip()
                variable, value = line.split("=")

                value = value.strip("'").strip("\"")

                self.set_variable(variable, value)

        for variable in possible_variables:
            if 'mandatory' in possible_variables[variable]:
                if possible_variables[variable]['mandatory']:
                    if self.get_variable(variable) is None or \
                            self.get_variable(variable) == '':
                        msg = "Mandatory variable {} not in {}".format(
                              variable, filename)
                        self.feedback['errors'].append(msg)

    def __str__(self):
        variablesvalues = self.get_variables()
        return str(self.__class__) + ": " + str(variablesvalues)

    def get_variable_path(self, variable):
        value = self.get_variable(variable)
        if value is not None:
            pathvalue = os.path.join(self.directory, value)
            if not os.path.exists(pathvalue):
                msg = "The {} file \'{}\' doesn't exist.".format(
                    variable, value)
                self.feedback['errors'].append(msg)
                return
            else:
                return pathvalue
        else:
            return

    def get_variable(self, variable):
        try:
            return getattr(self, variable)
        except Exception as e:
            return

    def get_variables(self):
        variablesvalues = {}
        for variable in self.possible_variables:
            value = self.get_variable(variable)
            if value is not None:
                variablesvalues[variable] = value
        return variablesvalues

    def set_variable(self, variable, value, update=False):
        possible_variables = self.possible_variables

        if variable in possible_variables:
            if 'possible_values' in possible_variables[variable]:
                if value not in \
                 possible_variables[variable]['possible_values']+['']:
                    msg = ('Value \'{}\' is not in the possible values for'
                           ' variable {}. Should be one of {}').format(
                        value, variable,
                        str(possible_variables[variable]
                            ['possible_values']))
                    self.feedback['errors'].append(msg)
                    return

            if 'variable_type' in possible_variables[variable]:
                # Check for existance of file
                if possible_variables[variable]['variable_type'] == 'filename':
                    pathvalue = os.path.join(self.directory, value)
                    if not os.path.exists(pathvalue):
                        msg = "The {} file \'{}\' doesn't exist.".format(
                            variable, value)
                        self.feedback['errors'].append(msg)

            if update:
                old_value = self.get_variable(variable)
                if old_value is not None:
                    if old_value != value:
                        setattr(self, variable, value)
                        msg = "Updated variable {} from \'{}\' to \'{}\'." \
                              .format(variable, old_value, value)
                        self.feedback['infos'].append(msg)
                elif value != '':
                    setattr(self, variable, value)
                    msg = "Set variable {} to \'{}\'.".format(
                        variable, value)
                    self.feedback['infos'].append(msg)
            else:
                setattr(self, variable, value)
        else:
            msg = ('Variable {} not in the list of possible variables for'
                   ' datatype {}.').format(variable, self.datatype)
            self.feedback['errors'].append(msg)

    def update_variable(self, variable, value):
        self.set_variable(variable, value, update=True)

    def get_possible_variables(self):
        return self.possible_variables

    def get_feedback(self):
        return self.feedback

    def save_to_file(self):
        filename = os.path.join(self.study_directory,
                                self.datatype+'.params')
        with open(filename, 'w') as handle:
            for variable in self.get_variables():
                handle.write(variable+'='+self.get_variable(variable)+'\n')
        handle.close()


class ClinicalParams(Params):
    """Class for clinical.params file"""
    def __init__(self, filename):
        possible_variables = {
            'COLUMN_MAP_FILE': {
                'mandatory': True,
                'variable_type': 'filename',
                'helptext': 'Points to the column file.'
                },
            'WORD_MAP_FILE': {
                'variable_type': 'filename',
                'helptext': ('Points to the file with dictionary to be used.')
                },
            "XTRIAL_FILE": {
                'helptext': ('Points to the cross study concepts file.')
            },
            "TAGS_FILE": {
                'variable_type': 'filename',
                'helptext': ('Points to the concepts tags file.')
            }
                              }
        datatype = 'clinical'
        super(ClinicalParams, self).__init__(filename,
                                             datatype,
                                             possible_variables)


class ExpressionParams(Params):
    """Class for expression.params file"""
    def __init__(self, filename):
        possible_variables = {
            'DATA_FILE': {
                'mandatory': True,
                'variable_type': 'filename',
                'helptext': 'Points to the HD data file.'
                },
            'DATA_TYPE': {
                'mandatory': True,
                'possible_values': ['R'],
                'default': 'R',
                'helptext': ('Must be R (raw values). Other types are not'
                             ' supported yet.')
                },
            "LOG_BASE": {
                'default': '2',
                'helptext': ('If present must be 2. The log base for'
                             ' calculating log values.')
            },
            "NODE_NAME": {
                'default': '<HD data type name>',
                'helptext': ('What to append to TOP_NODE for form the concept'
                             ' path of the HD node (before the part generated'
                             ' from category_cd).')
            },
            "MAP_FILENAME": {
                'mandatory': True,
                'variable_type': 'filename',
                'helptext': ('Filename of the mapping file.')
            },
            "ALLOW_MISSING_ANNOTATIONS": {
                'possible_values': ['Y', 'N'],
                'default': 'N',
                'helptext': ('Whether the job should be allowed to continue'
                             ' when the data set doesn\'t provide data for all'
                             ' the annotations (here probes).')
            }
                              }
        datatype = 'expression'
        super(ExpressionParams, self).__init__(filename,
                                               datatype,
                                               possible_variables)


def get_study_id(studiesfolder, study):
    # Try clinical.params first
    paramsfile = os.path.join(studiesfolder, study, 'clinical.params')

    if os.path.exists(paramsfile):
        paramsobject = ClinicalParams(paramsfile)
        studyid = paramsobject.get_variable('STUDY_ID')

    try:
        studyid
    except NameError:
        pass
    else:
        if studyid is not None:
            return studyid

    # Otherwise just return the uppercased version of the study folder name
    return study.upper()
