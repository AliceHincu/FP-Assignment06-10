# ---- classes for exceptions ----


class AssignmentException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# ---- classes for validator ----


class AssignmentValidator:
    """
    Generic validator for assignment
    """

    @staticmethod
    def validate(ass):
        """
        Validate a given assignment.
        -The ID must have 4 digits
        :param ass: the assignment (type: class)
        :return:Raise AssignmentValidationException if assignment instance is not valid
        """
        # validate ID
        if not len(ass.id) == 4:
            raise AssignmentException("Invalid ID: the ID must have 4 digits")
        if not ass.id.isdigit():
            raise AssignmentException("Invalid ID: the ID must contain only 4 digits!")

        months = ['jan', 'mar', 'may', 'jul', 'aug', 'oct', 'dec']
        if ass.deadline_day == '31':
            if ass.deadline_month not in months:
                raise AssignmentException("Invalid deadline: there are not 31 days in that month")
        elif ass.deadline_day == '30' and ass.deadline_month == 'feb':
            raise AssignmentException("Invalid deadline: february can have up to 29days")
