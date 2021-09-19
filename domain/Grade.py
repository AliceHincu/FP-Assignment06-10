class Grade:
    """
    Here we define the Grade
    """
    def __init__(self, student_id, assignment_id, grade_value):
        self._a_id = assignment_id
        self._s_id = student_id
        self._value = grade_value

    @property
    def a_id(self):
        """
        Get assignment id
        """
        return self._a_id

    @property
    def s_id(self):
        """
        Get student id
        """
        return self._s_id

    @property
    def value(self):
        """
        Get grade value
        """
        return self._value
