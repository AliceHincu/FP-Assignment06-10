from Iterable.IterableObject import Iterable


class AssignmentRepo(Iterable):
    """
    The repository for the assignments
    """
    def __init__(self):
        super(AssignmentRepo, self).__init__()
        self._assignments = []

    @property
    def assignments(self):
        """
        :return: the list of assignments
        """
        return self._assignments

    def __str__(self):
        return str(self._assignments)

    def __repr__(self):
        return str(self._assignments)

    def __len__(self):
        return len(self._assignments)

    def add(self, assignment):
        """
        We add a student
        :param assignment: (type: class)
        """
        self._assignments.append(assignment)

    def add_all(self, assignments):
        """
        We add multiple students
        :param assignments: (type: list of classes)
        """
        for assignment in assignments:
            self.add(assignment)

    def remove(self, id):
        """
        Remove the assignment
        :param id: type: string
        """
        assignments = self._assignments
        nr = 0
        for assignment in assignments:
            if assignment.id == id:
                self._assignments.pop(nr)
            nr += 1

    def update(self, old_id, id, description, day, month):
        """
        Update the assignment
        :param old_id: type: string
        :param id: type: string
        :param description: type: string
        :param day: type: string
        :param month: type: string
        """
        assignments = self._assignments
        for assignment in assignments:
            if assignment.id == old_id:
                assignment.set_id(id)
                assignment.set_description(description)
                assignment.set_deadline_day(day)
                assignment.set_deadline_month(month)

    def get_list(self):
        """
        We transform the list of classes into a normal list
        :return: the list of students
        """
        display_list = []
        for assignment in self.assignments:
            mini_list = list()
            mini_list.append(assignment.id)
            mini_list.append(assignment.description)
            mini_list.append(assignment.deadline_day)
            mini_list.append(assignment.deadline_month)
            display_list.append(mini_list)
        return display_list

    def transform(self, month):
        options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        index = options_month.index(month)
        return index+1

    def get_late_homework(self, assignments, homeworks, day_number, month_number):
        late_homework = []
        for homework in homeworks:
            for assignment in assignments:
                if assignment[0] == homework[1]:
                    day = int(assignment[2])
                    month = int(self.transform(assignment[3]))
                    if month < month_number:
                        if assignment[0] not in late_homework:
                            late_homework.append(assignment[0])
                    elif month == month_number:
                        if day < day_number:
                            if assignment[0] not in late_homework:
                                late_homework.append(assignment[0])
        return late_homework