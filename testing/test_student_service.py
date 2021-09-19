from unittest import TestCase

from service.student_service import StudentService
from MemoryRepo.StudentMemoryRepo import StudentMemoryRepository
from validator.student_validator import StudentValidator
from service.undo_service import UndoService


class TestStudentService(TestCase):
    def test_create_student(self):
        student_repo = StudentMemoryRepository()
        student_validator = StudentValidator
        undo_service = UndoService()
        student_service = StudentService(student_repo, student_validator, undo_service)

        # create
        student_service.create_student('12345', 'Alice', '1')
        student_service.create_student('12346', 'Catra', '2')

        res_true = student_service.check_for_unique_group('2')
        res_false = student_service.check_for_unique_group('3')
        self.assertEqual(res_false, False)
        self.assertEqual(res_true, True)

        actual_list = student_service.display()
        expected_list = [['12345', 'Alice', '1'], ['12346', 'Catra', '2']]
        self.assertEqual(expected_list, actual_list)

    def test_remove_student(self):
        student_repo = StudentMemoryRepository()
        student_validator = StudentValidator
        undo_service = UndoService()
        student_service = StudentService(student_repo, student_validator, undo_service)

        student_service.create_student('12345', 'Alice', '1')
        student_service.create_student('12346', 'Catra', '2')
        student_service.remove_student('12345')
        actual_list = student_service.display()
        expected_list = [['12346', 'Catra', '2']]
        self.assertEqual(expected_list, actual_list)

    def test_update_student(self):
        student_repo = StudentMemoryRepository()
        student_validator = StudentValidator
        undo_service = UndoService()
        student_service = StudentService(student_repo, student_validator, undo_service)

        student_service.create_student('12345', 'Alice', '1')
        student_service.create_student('12346', 'Catra', '2')
        student_service.remove_student('12345')
        student_service.update_student('12346', '12457', 'A', '3')
        actual_list = student_service.display()
        expected_list = [['12457', 'A', '3']]
        self.assertEqual(expected_list, actual_list)

