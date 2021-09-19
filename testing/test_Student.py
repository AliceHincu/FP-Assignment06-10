from unittest import TestCase

from domain.Student import Student
from validator.student_validator import StudentException, StudentValidator


class TestStudent(TestCase):
    def test_id(self):
        st = Student('12345', 'Alice', '1')
        vl = StudentValidator()
        self.assertEqual(st.id, '12345')
        with self.assertRaises(StudentException):
            vl.validate(Student('1245', 'Alice', '1'))
        with self.assertRaises(StudentException):
            vl.validate(Student('12a45', 'Alice', '1'))

    def test_name(self):
        st = Student('12345', 'Alice', '1')
        vl = StudentValidator()
        self.assertEqual(st.name, 'Alice')
        with self.assertRaises(StudentException):
            vl.validate(Student('12425', '432', '1'))

    def test_group(self):
        st = Student('12345', 'Alice', '1')
        self.assertEqual(st.group, '1')
        vl = StudentValidator()
        with self.assertRaises(StudentException):
            vl.validate(Student('12435', 'Alice', '1fsaf'))

    def test_set_id(self):
        st = Student('12345', 'Alice', '1')
        st.set_id('3456')
        self.assertEqual(st.id, '3456')

    def test_set_name(self):
        st = Student('12345', 'Alice', '1')
        st.set_name('Dora')
        self.assertEqual(st.name, 'Dora')

    def test_set_group(self):
        st = Student('12345', 'Alice', '1')
        st.set_group('2')
        self.assertEqual(st.group, '2')
