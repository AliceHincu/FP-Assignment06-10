"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Assignment import Assignment
from repository.assignment_repo import AssignmentRepo

import json


class AssignmentJsonFileRepository(AssignmentRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='assignments.pickle'):
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
        assignments = {}
        for i in range(len(self._assignments)):
            assignments[i] = str(self._assignments[i].id) + ',' + self._assignments[i].description + ',' + str(self._assignments[i].deadline_day + ',' + str(self._assignments[i].deadline_month))
        with open(self._file_name, 'w') as f:
            json.dump(assignments, f)
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        assignment_list = []

        with open(self._file_name) as f:
            try:
                data = json.load(f)
            except Exception:
                f.close()
                return
        for i in data.keys():
            data[i] = data[i].split(',')
            self.store(Assignment(data[i][0], data[i][1], [data[i][2], data[i][3]]))
        f.close()