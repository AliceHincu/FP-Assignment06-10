from domain.Student import Student
from service.undo_service import FunctionCall, Operation

# ---- classes for exceptions ----


class StudentIdException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class StudentService:
    """
    The service for student - bridge between ui and repository.
    """
    def __init__(self, student_repo, student_validator, service_undo):
        self._repo = student_repo
        self._validator = student_validator()
        self._undo = service_undo

    def return_student_with_id(self, id):
        students = self._repo.get_list()
        for student in students:
            if student[0] == id:
                return [str(student[1]), int(student[2])]

    def check_for_unique_id(self, ID):
        """
        Check to see if the ID exists
        :param ID: type: string
        :return: true if the id is found, else false
        """
        students = self._repo.get_list()
        for student in students:
            if student[0] == ID:
                return True
        return False

    def check_for_unique_group(self, group):
        """
        Check to see if the group exists
        :param group: type: string
        :return: true if the group is found, else false
        """
        students = self._repo.get_list()
        for student in students:
            if student[2] == group:
                return True
        return False

    def create_student(self, id, name, group):
        """
        Add student to application
        :param id: type: string
        :param name: type: string 
        :param group: type: string
        :return: raises StudentIdException if the id is already used or if the student is not valid
        """""
        if self.check_for_unique_id(id):
            raise StudentIdException("The ID is already used!")
        else:
            self._validator.validate(Student(id, name, group))
            new_student = Student(id, name, group)
            self._repo.store(new_student)
            redo = FunctionCall(self._repo.store, new_student)
            undo = FunctionCall(self._repo.delete, id)
            op = Operation(undo, redo)
            self._undo.recordOperation(op)

    def display(self):
        """
        Gets the students
        :return: the list of students
        """
        return self._repo.get_list()

    def remove_student(self, id):
        """
        Remove the student
        :param id: the id from the student (type: string)
        :return: raises an error if the ID doesn't exist
        """
        if not self.check_for_unique_id(id):
            raise StudentIdException("The ID doesn't exist!")
        else:

            redo = FunctionCall(self._repo.delete, id)
            st = self.return_student_with_id(id)
            new_student = Student(id, st[0], st[1])
            undo = FunctionCall(self._repo.store, new_student)
            op = Operation(undo, redo)
            self._undo.recordOperation(op)

            self._repo.delete(id)

    def update_student(self, old_id, id, name, group):
        """
        Updates a student
        :param old_id: type: string
        :param id: type: string
        :param name: type: string
        :param group: type: string
        :return: raises StudentIdException if the id is not good or the student is not valid
        """
        if not self.check_for_unique_id(old_id):
            raise StudentIdException("The Old ID doesn't exist!")
        else:
            self._validator.validate(Student(id, name, group))
            if self.check_for_unique_id(id):
                raise StudentIdException("The New ID is already used!")
            else:
                st = self.return_student_with_id(old_id)
                redo = FunctionCall(self._repo.update_student, old_id, id, name, group)
                undo = FunctionCall(self._repo.update_student, id, old_id, st[0], st[1])
                op = Operation(undo, redo)
                self._undo.recordOperation(op)

                self._repo.update_student(old_id, id, name, group)
