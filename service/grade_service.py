from domain.Grade import Grade
from service.undo_service import FunctionCall, Operation
from Iterable.IterableObject import shell_sort

# ---- classes for exceptions ----


class GradeStudentException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class GradeService:
    """
    The service for grade - bridge between ui and repository.
    """
    def __init__(self, grade_repo, grade_validator, service_undo):
        self._repo = grade_repo
        self._validator = grade_validator()
        self._undo = service_undo

    def check_for_same_assignment(self, student, assignment):
        """
        Check if the student has already that assignment
        :param student: type: string(the id)
        :param assignment: type: string(the id)
        :return: true if it has the assignment, else false
        """
        mini_list = [student, assignment]
        homework_list = self._repo.get_homework()
        if mini_list in homework_list:
            return True
        else:
            return False

    def create_homework(self, student, assignment):
        """
        Create homework for a single student
        :param student: type: string
        :param assignment: type: string
        :return: raises GradeStudentException
        """
        if self.check_for_same_assignment(student, assignment):
            raise GradeStudentException("The student has already that assignment!")
        else:
            self._validator.validate_hw(student, assignment)
            new_homework = Grade(student, assignment, '-')

            redo = FunctionCall(self._repo.store_hw, new_homework)
            undo = FunctionCall(self._repo.delete_homework, new_homework)
            op = Operation(undo, redo)
            self._undo.recordOperation(op)

            self._repo.store_hw(new_homework)

    def create_homework_2(self, student, assignment):
        """
        Creates homework for a single student except it doesn't raise any errors
        :param student: type: string
        :param assignment: type: string
        """
        if not self.check_for_same_assignment(student, assignment):
            self._validator.validate_hw(student, assignment)
            new_homework = Grade(student, assignment, '-')

            redo = FunctionCall(self._repo.store_hw, new_homework)
            undo = FunctionCall(self._repo.delete_homework, new_homework)
            op = Operation(undo, redo)
            self._undo.recordOperation(op)

            self._repo.store_hw(new_homework)

    def create_homework_gr(self, group, assignment, student_service):
        """
        Creates homework for a group of students
        :param group: type: string
        :param assignment: type: string
        :param student_service: type: string
        """
        students = student_service.display()
        for student in students:
            if student[2] == group:
                self.create_homework_2(student[0], assignment)

    def display(self):
        """
        Gets the homework
        :return: the list of grades
        """
        return self._repo.get_list()

    def display_grades(self):
        """
        Gets the grades
        :return:
        """
        return self._repo.get_list_grade()

    def student_assignments(self, id):
        """
        Search student's assignments
        :param id: student id
        :return: its assignments
        """
        assignments = self._repo.get_list()
        student_assignment = self._repo.get_student_list(assignments, id)
        return student_assignment

    def grade_student(self, student_id, grade, assignment_id):
        self._validator.validate_grade(student_id, grade, assignment_id)
        new_grade = Grade(student_id, assignment_id, int(grade))

        redo = FunctionCall(self._repo.grade_st, new_grade)
        undo = FunctionCall(self._repo.undo_gr, Grade(student_id, assignment_id, '-'), new_grade)
        op = Operation(undo, redo)
        self._undo.recordOperation(op)

        self._repo.grade_st(new_grade)

    def delete_grade_student(self, student_id):
        self._repo.delete_student(student_id)

    def delete_grade_assignment(self, assignment_id):
        self._repo.delete_assignment(assignment_id)

    def order_grades(self, id):
        students = self._repo.students_for_assignment(id)
        result = self._repo.order_grades(students)
        return result

    def order_total_grades(self, students):
        list_ordered_by_name = shell_sort(self._repo.grades(), comp=lambda x, y: x[0] < y[0])
        average_list = self._repo.average_grade(list_ordered_by_name)
        final_list = shell_sort(average_list, comp=lambda x, y: x[1] < y[1], reverse=True)
        return final_list

    def get_late_students(self, homework_list):
        student_list = []
        for homework_id in homework_list:
            for students in self._repo.get_list():
                if students[1] == homework_id:
                    if students[0] not in student_list:
                        student_list.append(students[0])
        return student_list