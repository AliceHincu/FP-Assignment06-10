class Student:
    """
    Here we define the Student
    """
    def __init__(self, student_id, name, group):
        self._ID = student_id
        self._name = name
        self._group = group

    @property
    def id(self):
        """
        :return: get the id
        """
        return self._ID

    @property
    def name(self):
        """
        :return: get the name
        """
        return self._name

    @property
    def group(self):
        """
        :return: get the group
        """
        return self._group

    def set_id(self, id):
        """
        :param id: set the id
        """
        self._ID = id

    def set_name(self, name):
        """
        :param name: set the name
        """
        self._name = name

    def set_group(self, group):
        """
        :param group: set the group
        """
        self._group = group

    def __str__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.group)

    def __repr__(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.group)
