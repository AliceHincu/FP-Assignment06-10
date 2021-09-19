from unittest import TestCase

from service.assignment_service import AssignmentService, AssignmentIdException
from repository.assignment_repo import AssignmentRepo
from validator.assignment_validator import AssignmentValidator
from service.undo_service import UndoService
from MemoryRepo.AssignmentMemoryRepo import AssignmentMemoryRepository
from domain.Assignment import Assignment
from Iterable.IterableObject import Iterable

from datetime import date


class TestAssignmentService(TestCase):
    def test_create_assignment(self):
        assignment_repo = AssignmentMemoryRepository()
        assignment_validator = AssignmentValidator
        undo_service = UndoService()
        assignment_service = AssignmentService(assignment_repo, assignment_validator, undo_service)

        assignment_service.create_assignment('1234', 'This is a description', ['20', 'nov'])
        with self.assertRaises(AssignmentIdException):
            assignment_service.create_assignment('1234', 'This is a description', ['20', 'nov'])
        assignment_service.create_assignment('1235', 'This is a description2', ['21', 'nov'])
        actual_list = assignment_service.display()
        expected_list = [['1234', 'This is a description', '20', 'nov'],
                         ['1235', 'This is a description2', '21', 'nov']]
        self.assertEqual(expected_list, actual_list)

    def test_remove_assignment(self):
        assignment_repo = AssignmentMemoryRepository()
        assignment_validator = AssignmentValidator
        undo_service = UndoService()
        assignment_service = AssignmentService(assignment_repo, assignment_validator, undo_service)

        assignment_service.create_assignment('1234', 'This is a description', ['20', 'nov'])
        assignment_service.create_assignment('1235', 'This is a description2', ['21', 'nov'])

        assignment_service.remove_assignment('1234')
        with self.assertRaises(AssignmentIdException):
            assignment_service.remove_assignment('1266')


        actual_list = assignment_service.display()
        expected_list = [['1235', 'This is a description2', '21', 'nov']]
        self.assertEqual(expected_list, actual_list)

    def test_update_assignment(self):
        assignment_repo = AssignmentMemoryRepository()
        assignment_validator = AssignmentValidator
        undo_service = UndoService()
        assignment_service = AssignmentService(assignment_repo, assignment_validator, undo_service)

        assignment_service.create_assignment('1234', 'This is a description', ['20', 'nov'])
        assignment_service.create_assignment('1235', 'This is a description2', ['21', 'nov'])
        assignment_service.create_assignment('1236', 'This is a description2', ['21', 'nov'])

        assignment_service.remove_assignment('1234')
        with self.assertRaises(AssignmentIdException):
            assignment_service.update_assignment('1234', '1244', 'This is a description', '20', 'nov')
        with self.assertRaises(AssignmentIdException):
            assignment_service.update_assignment('1235', '1236', 'This is a description', '20', 'nov')

        assignment_service.update_assignment('1235', '1247', 'I am a black sheep', '3', 'dec')
        actual_list = assignment_service.display()
        expected_list = [['1247', 'I am a black sheep', '3', 'dec'], ['1236', 'This is a description2', '21', 'nov']]
        self.assertEqual(expected_list, actual_list)

    def test_transform(self):
        assignment_repo = AssignmentMemoryRepository()
        assignment_validator = AssignmentValidator
        undo_service = UndoService()
        assignment_service = AssignmentService(assignment_repo, assignment_validator, undo_service)

        nr = assignment_service.transform_month(1)
        self.assertEqual(nr, "jan")

    def test_late_homework(self):
        assignment_repo = AssignmentMemoryRepository()
        assignment_validator = AssignmentValidator
        undo_service = UndoService()
        assignment_service = AssignmentService(assignment_repo, assignment_validator, undo_service)

        assignment_service.create_assignment('1234', 'This is a description', ['20', 'nov'])
        assignment_service.create_assignment('1235', 'This is a description2', ['21', 'dec'])
        assignment_service.create_assignment('1236', 'This is a description', ['1', 'dec'])
        homeworks = [['12345', '1234', '-'],
                     ['12356', '1235', '-'],
                     ['12347', '1236', '-']]

        today = date.today()
        day = today.day
        month_number = today.month
        homework_list = assignment_service.get_late_homework(homeworks, day, month_number)

        expected_list = ['1234', '1236']
        self.assertEqual(expected_list, homework_list)