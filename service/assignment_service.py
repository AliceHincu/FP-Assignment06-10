from domain.Assignment import Assignment
from validator.assignment_validator import AssignmentValidator, AssignmentException
from service.undo_service import FunctionCall, Operation

# ---- classes for exceptions ----


class AssignmentIdException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AssignmentService:
    """
    The service for assignment - bridge between ui and repository.
    """
    def __init__(self, ass_repo, ass_validator, service_undo):
        self._repo = ass_repo
        self._validator = ass_validator()
        self._undo = service_undo

    def return_ass_with_id(self, ID):
        """
        Check to see if the ID of the assignment exists already.
        :param ID: type: string
        :return: true if the id is found, else false
        """
        assignments = self._repo.get_list()
        for assignment in assignments:
            if assignment[0] == ID:
                return [assignment[1], assignment[2], assignment[3]]

    def check_for_unique_id(self, ID):
        """
        Check to see if the ID of the assignment exists already.
        :param ID: type: string
        :return: true if the id is found, else false
        """
        assignments = self._repo.get_list()
        for assignment in assignments:
            if assignment[0] == ID:
                return True
        return False

    def create_assignment(self, id, description, deadline):
        """
        Add assignment to the list
        :param id: type: string
        :param description: type: string 
        :param deadline: type: string
        :return: raises AssignmentIdException if the id is already used or if the student is not valid
        """""
        if self.check_for_unique_id(id):
            raise AssignmentIdException("The ID is already used!")
        else:
            self._validator.validate(Assignment(id, description, deadline))
            new_ass = Assignment(id, description, deadline)
            self._repo.store(new_ass)
            redo = FunctionCall(self._repo.store, new_ass)
            undo = FunctionCall(self._repo.delete, id)
            op = Operation(undo, redo)
            self._undo.recordOperation(op)

    def remove_assignment(self, id):
        """
        Remove the assignment
        :param id: the id from the assignment (type: string)
        :return: raises AssignmentIdException if the ID doesn't exist
        """
        if not self.check_for_unique_id(id):
            raise AssignmentIdException("The ID doesn't exist!")
        else:
            redo = FunctionCall(self._repo.delete, id)
            ass = self.return_ass_with_id(id)
            new_ass = Assignment(id, ass[0], [ass[1], ass[2]])
            undo = FunctionCall(self._repo.store, new_ass)
            op = Operation(undo, redo)
            self._undo.recordOperation(op)

            self._repo.delete(id)

    def update_assignment(self, old_id, id, description, day, month):
        """
        Updates an assignment
        :param old_id: type: string
        :param id: type: string
        :param description: type: string
        :param day: type: string
        :param month: type: string
        :return: raises AssignmentIdException errors if the id is not good or the student is not valid
        """
        if not self.check_for_unique_id(old_id):
            raise AssignmentIdException("The Old ID doesn't exist!")
        else:
            self._validator.validate(Assignment(id, description, [day, month]))
            if self.check_for_unique_id(id):
                raise AssignmentIdException("The New ID is already used!")
            else:
                ass = self.return_ass_with_id(old_id)
                redo = FunctionCall(self._repo.update_assignment, old_id, id, description, day, month)
                undo = FunctionCall(self._repo.update_assignment, id, old_id, ass[0], ass[1], ass[2])
                op = Operation(undo, redo)
                self._undo.recordOperation(op)

                self._repo.update_assignment(old_id, id, description, day, month)

    def display(self):
        """
        Gets the students
        :return: the list of students
        """
        return self._repo.get_list()

    def transform_month(self, month):
        options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        return options_month[month-1]

    def get_late_homework(self, homeworks, day, month):
        homework_list = self._repo.get_late_homework(self.display(), homeworks, day, month)
        return homework_list
