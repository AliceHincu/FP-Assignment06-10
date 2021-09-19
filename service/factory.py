from domain.Student import Student


class StudentFactory:
    """
    Create validated instances of Student
    """

    def __init__(self, validator):
        self._validator = validator

    def create_student(self, id_, name, group):
        student = Student(id_, name, group)
        self._validator.validate(student)
        return student


"""
Example of starting up layers with Factory pattern
ingr_repo = Repository()
ingr_valid = IngredientValidator()
ingr_factory = IngredientFactory(ingr_valid)
ingr_service = IngredientService(ingr_repo,ingr_factory)
"""