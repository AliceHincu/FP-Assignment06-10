from unittest import TestCase

from service.assignment_service import Assignment, AssignmentException, AssignmentValidator


class TestAssignment(TestCase):
    def test_id(self):
        with self.assertRaises(AssignmentException):
            av = AssignmentValidator.validate(Assignment('123a45', 'This is a description', '20 nov'))
        with self.assertRaises(AssignmentException):
            av = AssignmentValidator.validate(Assignment('1a45', 'This is a description', '20 nov'))

    def test_description(self):
        av = AssignmentValidator.validate(Assignment('1234', 'This is a description', ['20', 'feb']))
        self.assertEqual(av, None)

    def test_deadline(self):
        with self.assertRaises(AssignmentException):
            av = AssignmentValidator.validate(Assignment('1234', 'This is a description', ['30', 'feb']))

    def test_deadline_day(self):
        av = AssignmentValidator.validate(Assignment('1234', 'This is a description', ['29', 'feb']))
        self.assertEqual(av, None)
        with self.assertRaises(AssignmentException):
            av = AssignmentValidator.validate(Assignment('1245', 'This is a description', ['31', 'nov']))


    def test_deadline_month(self):
        av = AssignmentValidator.validate(Assignment('1234', 'This is a description', ['30', 'bla']))
        self.assertEqual(av, None)

    def test_set_id(self):
        ass = Assignment('1234', 'This is a description', ['20', 'nov'])
        ass.set_id('3456')
        self.assertEqual(ass.id, '3456')

    def test_set_description(self):
        ass = Assignment('1234', 'This is a description', ['20', 'nov'])
        ass.set_description('ABC')
        self.assertEqual(ass.description, 'ABC')

    def test_set_deadline(self):
        ass = Assignment('1234', 'This is a description', ['20', 'nov'])
        ass.set_deadline(['19', 'jan'])
        self.assertEqual(ass.deadline, ['19', 'jan'])

    def test_set_deadline_day(self):
        ass = Assignment('1234', 'This is a description', ['20', 'nov'])
        ass.set_deadline_day('19')
        self.assertEqual(ass.deadline, ['19', 'nov'])

    def test_set_deadline_month(self):
        ass = Assignment('1234', 'This is a description', ['20', 'nov'])
        ass.set_deadline_month('jan')
        self.assertEqual(ass.deadline, ['20', 'jan'])
