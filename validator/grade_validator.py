# ---- classes for exceptions ----


class GradeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# ---- classes for validation ----
class GradeValidator:
    """
    Generic validator for Grade
    """

    @staticmethod
    def validate_hw(student, assignment):
        """
        Validate a given homework.
        -The Student ID must have 5 digits
        -The Assignment ID must have 4 digits
        :param student: the student ID (type: string)
        :param assignment: the assignment ID (type: string)
        :return: Raise GradeException if the ID are not valid
        """
        # validate ID
        if not len(student) == 5:
            raise GradeException("Invalid ID: the Student ID must have 5 digits")
        if not student.isdigit():
            raise GradeException("Invalid ID: the Student ID must contain only digits!")

        if not len(assignment) == 4:
            raise GradeException("Invalid ID: the Assignment ID must have 4 digits")
        if not assignment.isdigit():
            raise GradeException("Invalid ID: the Assignment ID must contain only digits!")

    @staticmethod
    def validate_grade(student, grade, assignment):
        """
        Validate a given student.
        -The Student ID must have 5 digits
        -The Assignment ID must have 4 digits
        :param student: the student ID (type: string)
        :param assignment: the assignment ID (type: string)
        :return: Raise GradeException if the ID are not valid
        """
        # validate ID
        if not len(student) == 5:
            raise GradeException("Invalid ID: the Student ID must have 5 digits")
        if not student.isdigit():
            raise GradeException("Invalid ID: the Student ID must contain only digits!")

        if not len(assignment) == 4:
            raise GradeException("Invalid ID: the Assignment ID must have 4 digits")
        if not assignment.isdigit():
            raise GradeException("Invalid ID: the Assignment ID must contain only digits!")

        if not grade.isdigit():
            raise GradeException("The grade needs to be a number!")
        elif int(grade) < 1 or int(grade) > 10:
            raise GradeException("Invalid grade: the grade must be in the interval [1,10]")