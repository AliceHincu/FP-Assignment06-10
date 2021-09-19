from Iterable.IterableObject import Iterable, shell_sort


class GradeRepo(Iterable):
    """
    The repository for the grade
    """
    def __init__(self):
        super(GradeRepo, self).__init__()
        self._grades = []
        self._homework = []

    def grades(self):
        """
        :return: the list of grades
        """
        return self._grades

    def get_homework(self):
        """
        :return: the list of homeworks
        """
        return self._homework

    def __str__(self):
        return str(self._grades)

    def __repr__(self):
        return str(self._grades)

    def __len__(self):
        return len(self._grades)

    def add_hw(self, homework):
        """
        We add homework
        :param homework: (type: class)
        """
        self._homework.append([homework.s_id, homework.a_id])

    def add_grade(self, grade):
        """
        Add grade
        :param grade: type: class
        :return:
        """
        self._grades.append([grade.s_id, grade.a_id, grade.value])

    def delete_hw(self, homework):
        """
        Delete a homework because it was graded
        :param homework:
        :return:
        """
        index = 0
        for i in range(len(self._homework)):
            if self._homework[i] == homework:
                index = i
        self._homework.pop(index)

    def delete_gr(self, grade):
        index = 0
        for i in range(len(self._grades)):
            if self._grades[i] == grade:
                index = i
        self._grades.pop(index)

    def undo_grade(self, homework, grade):
        self.add_hw(homework)
        self.delete_gr(grade)

    def delete_student(self, id):
        index = []
        index2 = []
        for i in range(len(self._grades)):
            if self._grades[i][0] == id:
                index.append(i)
        for i in range(len(self._homework)):
            if self._homework[i][0] == id:
                index2.append(i)

        for j in range(len(index)-1, -1, -1):
            self._grades.pop(index[j])
        for j in range(len(index2)-1, -1, -1):
            self._homework.pop(index2[j])

    def delete_assignment(self, id):
        index = []
        index2 = []
        for i in range(len(self._grades)):
            if self._grades[i][1] == id:
                index.append(i)
        for i in range(len(self._homework)):
            if self._homework[i][1] == id:
                index2.append(i)

        for j in range(len(index)-1, -1, -1):
            self._grades.pop(index[j])
        for j in range(len(index2)-1, -1, -1):
            self._homework.pop(index2[j])

    def get_list(self):
        """
        We transform the list of classes into a normal list
        :return: the list of students
        """
        display_list = []
        for hw in self.get_homework():
            mini_list = list()
            mini_list.append(hw[0])
            mini_list.append(hw[1])
            display_list.append(mini_list)
        return display_list

    def get_list_grade(self):
        """
        We transform the list of classes into a normal list
        :return: the list of students
        """
        display_list = []
        for grade in self.grades():
            mini_list = list()
            mini_list.append(grade[0])
            mini_list.append(grade[1])
            mini_list.append(grade[2])
            display_list.append(mini_list)
        return display_list

    def get_student_list(self, assignments, id):
        """
        Get student's assignments
        :param assignments: the list of all assignments
        :param id: id of student
        :return: the student's assignments (type: list)
        """
        st_assignments = []
        for i in range(len(assignments)):
            if assignments[i][0] == id:
                st_assignments.append(assignments[i][1])
        return st_assignments

    def students_for_assignment(self, assignment_id):
        """
        Get the students that have a specific assignment
        :param assignment_id:
        :return:
        """
        display_list = []
        for grade in self.grades():
            if grade[1] == assignment_id:
                display_list.append([grade[0], grade[1], int(grade[2])])
        return display_list

    def grade_student(self, grade):
        """
        Grade a student
        :param grade:
        :return:
        """
        old_homework = [grade.s_id, grade.a_id]
        self.delete_hw(old_homework)
        self.add_grade(grade)

    def order_grades(self, students):
        """
        Order grades
        :param students:
        :return:
        """
        grades = shell_sort(students, comp=lambda x, y: x[2] <= y[2])
        return grades

    def average_grade(self, init_list):
        """
        Get the average grade for every student
        :param init_list:
        :return:
        """
        final_list = []
        id_list = []
        for student in init_list:
            if student[0] not in id_list:
                #                         lista cu note(id stud,...)  #daca id-ul studentului din lista =
                student_grades = [x for x in self.get_list_grade() if x[0] == student[0]]
                sum = 0
                nr = 0
                for i in range(len(student_grades)):
                    sum += int((student_grades[i][2]))
                    nr += 1
                average_grade = sum/nr
                final_list.append([student[0], average_grade])
                id_list.append(student[0])
        return final_list