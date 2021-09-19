from Iterable.IterableObject import Iterable


class StudentRepo(Iterable):
    """
    The repository for a student
    """
    def __init__(self):
        Iterable.__init__(self)
        self._students = Iterable()
        self._groups = []

    @property
    def students(self):
        """
        :return: the list of students
        """
        return self._students

    @property
    def groups(self):
        """
        :return: the list of groups
        """
        return self._groups

    def __str__(self):
        return str(self._students)

    def __repr__(self):
        return str(self._students)

    def __len__(self):
        return len(self._students)

    def add(self, student):
        """
        We add a student
        :param student: (type: class)
        """
        self._students.append(student)
        ok = True
        for group in self.groups:
            if student.group == group:
                ok = False
        if ok:
            self._groups.append(student.group)

    def add_all(self, students):
        """
        We add multiple students
        :param students: (type: list of classes)
        """
        for student in students:
            self.add(student)

    def get_list(self):
        """
        We transform the list of classes into a normal list
        :return: the list of students
        """
        display_list = []
        for student in self.students:
            mini_list = list()
            mini_list.append(student.id)
            mini_list.append(student.name)
            mini_list.append(student.group)
            display_list.append(mini_list)
        return display_list

    def remove(self, id):
        """
        Remove the student
        :param id: type: string
        """
        students = self._students
        nr = 0
        for student in students:
            if student.id == id:
                del self._students[nr]
            nr += 1

    def update(self, old_id, id, name, group):
        """
        Update the student
        :param old_id: type: string
        :param id: type: string
        :param name: type: string
        :param group: type: string
        """
        students = self._students
        for student in students:
            if student.id == old_id:
                student.set_id(id)
                student.set_name(name)
                student.set_group(group)
