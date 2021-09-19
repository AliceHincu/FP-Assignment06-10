from unittest import TestCase

from validator.grade_validator import GradeException, GradeValidator
from domain.Grade import Grade


class TestGrade(TestCase):
    def test_a_id(self):
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('12345', '739', '15.7')
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('12345', 'a39', '15.7')
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('12345', 'a39', '10')
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('1234h', '739', '10')

        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('12345', 'a', '1234')
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('12345', '20', '1234')
        gr = Grade('12345', '1234', '9')
        self.assertEqual(gr.s_id, '12345')

        with self.assertRaises(GradeException):
            hw = GradeValidator.validate_hw('12345', '391')
        with self.assertRaises(GradeException):
            hw = GradeValidator.validate_hw('12345', '39vv')

    def test_s_id(self):
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('12a45', '739', '15.7')
        with self.assertRaises(GradeException):
            gr = GradeValidator.validate_grade('144345', '739', '15.7')
        gr = Grade('12345', '1234', '9')
        self.assertEqual(gr.a_id, '1234')

        with self.assertRaises(GradeException):
            hw = GradeValidator.validate_hw('12v345', '7391')
        with self.assertRaises(GradeException):
            hw = GradeValidator.validate_hw('12v45', '7391')

    def test_value(self):
        gr = Grade('12345', '1234', '9')
        self.assertEqual(gr.value, '9')
