from unittest import TestCase

from repository.assignment_repo import AssignmentRepo
from domain.Assignment import Assignment
from datetime import date


class TestAssignmentRepo(TestCase):
    def test_add(self):
        assignment_repo = AssignmentRepo()
        assignment_repo.add(Assignment('1234', 'This is a description', ['20', 'nov']))
        assignment_repo.add(Assignment('1235', 'This is a description2', ['21', 'nov']))
        actual_list = assignment_repo.get_list()
        expected_list = [['1234', 'This is a description', '20', 'nov'],
                         ['1235', 'This is a description2', '21', 'nov']]
        self.assertEqual(expected_list, actual_list)

    def test_add_all(self):
        assignment_repo = AssignmentRepo()
        assignment_repo.add_all([Assignment('1234', 'This is a description', ['20', 'nov']),
                                 Assignment('1235', 'This is a description2', ['21', 'nov'])])
        actual_list = assignment_repo.get_list()
        expected_list = [['1234', 'This is a description', '20', 'nov'],
                         ['1235', 'This is a description2', '21', 'nov']]
        self.assertEqual(expected_list, actual_list)

    def test_remove(self):
        assignment_repo = AssignmentRepo()
        assignment_repo.add_all([Assignment('1234', 'This is a description', ['20', 'nov']),
                                 Assignment('1235', 'This is a description2', ['21', 'nov'])])
        assignment_repo.remove('1234')
        actual_list = assignment_repo.get_list()
        expected_list = [['1235', 'This is a description2', '21', 'nov']]
        self.assertEqual(expected_list, actual_list)

    def test_update(self):
        assignment_repo = AssignmentRepo()
        assignment_repo.add_all([Assignment('1234', 'This is a description', ['20', 'nov']),
                                 Assignment('1235', 'This is a description2', ['21', 'nov'])])
        assignment_repo.remove('1234')
        assignment_repo.update('1235', '1247', 'I am a black sheep', '3', 'dec')
        actual_list = assignment_repo.get_list()
        expected_list = [['1247', 'I am a black sheep', '3', 'dec']]
        self.assertEqual(expected_list, actual_list)

    def test_transform(self):
        assignment_repo = AssignmentRepo()
        nr = assignment_repo.transform('jan')
        self.assertEqual(nr, 1)

    def test_late_homework(self):
        assignment_repo = AssignmentRepo()
        assignments = [['1234', 'This is a description', '20', 'nov'],
                       ['1235', 'This is a description2', '21', 'dec'],
                       ['1236', 'This is a description', '1', 'dec']]
        homeworks = [['12345', '1234', '-'],
                     ['12356', '1235', '-'],
                     ['12347', '1236', '-']]

        today = date.today()
        day = today.day
        month_number = today.month
        homework_list = assignment_repo.get_late_homework(assignments, homeworks, day, month_number)

        expected_list = ['1234', '1236']
        self.assertEqual(expected_list, homework_list)