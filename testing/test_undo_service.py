from unittest import TestCase

from service.student_service import StudentService
from MemoryRepo.StudentMemoryRepo import StudentMemoryRepository
from validator.student_validator import StudentValidator
from service.undo_service import FunctionCall, Operation, UndoService, UndoRedoException

class TestUndoService(TestCase):
    def test_undo_redo(self):
        student_repo = StudentMemoryRepository()
        student_validator = StudentValidator
        undo_service = UndoService()
        student_service = StudentService(student_repo, student_validator, undo_service)

        # create
        student_service.create_student('12345', 'Alice', '1')
        student_service.create_student('12346', 'Catra', '2')
        undo_service.undo()
        actual_list = student_service.display()
        expected_list = [['12345', 'Alice', '1']]
        self.assertEqual(expected_list, actual_list)

        undo_service.redo()
        expected_list = [['12345', 'Alice', '1'], ['12346', 'Catra', '2']]
        actual_list = student_service.display()
        self.assertEqual(expected_list, actual_list)

        undo_service.undo()
        undo_service.undo()

        with self.assertRaises(UndoRedoException):
            undo_service.undo()

        undo_service.redo()
        undo_service.redo()
        with self.assertRaises(UndoRedoException):
            undo_service.redo()
