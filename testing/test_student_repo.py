from unittest import TestCase

from repository.student_repo import StudentRepo
from domain.Student import Student


class TestStudentRepo(TestCase):
    def test_add(self):
        student_repo = StudentRepo()
        student_repo.add(Student('12345', 'Alice', '1'))
        student_repo.add(Student('12346', 'Catra', '2'))
        actual_list = student_repo.get_list()
        expected_list = [['12345', 'Alice', '1'], ['12346', 'Catra', '2']]
        self.assertEqual(expected_list, actual_list)

    def test_add_all(self):
        student_repo = StudentRepo()
        student_repo.add_all([Student('12345', 'Alice', '1'),
                              Student('12346', 'Catra', '2')])
        actual_list = student_repo.get_list()
        expected_list = [['12345', 'Alice', '1'], ['12346', 'Catra', '2']]
        self.assertEqual(expected_list, actual_list)

    def test_remove(self):
        student_repo = StudentRepo()
        student_repo.add_all([Student('12345', 'Alice', '1'),
                              Student('12346', 'Catra', '2')])
        student_repo.remove('12345')
        expected_list = [['12346', 'Catra', '2']]
        actual_list = student_repo.get_list()
        self.assertEqual(expected_list, actual_list)

    def test_update(self):
        student_repo = StudentRepo()
        student_repo.add_all([Student('12345', 'Alice', '1'),
                              Student('12346', 'Catra', '2')])
        student_repo.remove('12345')
        student_repo.update('12346', '12457', 'A', '3')
        actual_list = student_repo.get_list()
        expected_list = [['12457', 'A', '3']]
        self.assertEqual(expected_list, actual_list)
