import configparser

class Settings:
    def __init__(self, settings_file):
        self._propFile = settings_file
        self._config = configparser.RawConfigParser()
        self._config.read(self._propFile)

    def get_type(self):
        return str(self._config["Settings"]["repository"])

    def get_student_repo(self):
        file_student = self._config.get('Settings', 'students')
        return file_student

    def get_assignment_repo(self):
        file_ass = self._config.get('Settings', 'assignments')
        return file_ass

    def get_grade_repo(self):
        file_grade = self._config.get('Settings', 'grades')
        return file_grade

    def get_gui(self):
        if str(self._config["Settings"]["ui"]) == 'gui':
            return True
        elif str(self._config["Settings"]["ui"]) == 'ui':
            return False