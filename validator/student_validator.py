# ---- classes for exceptions ----


class StudentException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class StudentValidator:
    """
    Generic validator for Student
    """

    @staticmethod
    def validate(student):
        """
        Validate a given student.
        -The ID must have 5 digits
        -The name must only contain letters
        -The group must only contain digits
        :param student: the student (type: class)
        :return: Raise StudentValidationException if student instance is not valid
        """
        # validate ID
        if not len(student.id) == 5:
            raise StudentException("Invalid ID: the ID must have 5 digits")
        if not student.id.isdigit():
            raise StudentException("Invalid ID: the ID must contain only digits!")

        # validate name
        if student.name.isdigit():
            raise StudentException("Invalid name: the name must only contain letters!")

        # validate group
        if not student.group.isdigit():
            raise StudentException("Invalid group: the name must only contain digits!")
