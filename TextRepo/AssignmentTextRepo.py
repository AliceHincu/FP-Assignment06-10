"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Assignment import Assignment
from repository.assignment_repo import AssignmentRepo


class AssignmentTextFileRepository(AssignmentRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='assignments.txt'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def store(self, item):
        super().add(item)
        self._save()

    def delete(self, id_):
        super().remove(id_)
        self._save()

    def update_assignment(self, id_old, id_new, descr, day, month):
        super().update(id_old, id_new, descr, day, month)
        self._save()

    def _save(self):
        f = open(self._file_name, 'wt')
        text = ""
        for assign in self._assignments:
            line = str(assign.id) + ';' + assign.description + ';' + str(assign.deadline_day) + ';' + str(assign.deadline_month)
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        ass_list = []

        try:
            f = open(self._file_name, 'rt')  # read text

            line = f.readline().strip()

            while len(line) > 0:
                line = line.split(";")
                ass_list.append(Assignment(line[0], line[1], [line[2], line[3]]))
                line = f.readline().strip()

            for assign in ass_list:
                super().add(assign)
        except FileNotFoundError as e:
            raise FileNotFoundError()