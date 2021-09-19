
"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Student import Student
from repository.student_repo import StudentRepo
import json


class StudentJsonFileRepository(StudentRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='students.json'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def store(self, item):
        super().add(item)
        self._save()

    def delete(self, id_):
        super().remove(id_)
        self._save()

    def update_student(self, id_old, id_new, name, gr):
        super().update(id_old, id_new, name, gr)
        self._save()

    def _save(self):
        students = {}
        for i in range(len(self._students)):
            students[i] = str(self._students[i].id) + ',' + self._students[i].name + ',' + str(self._students[i].group)
        with open(self._file_name, 'w') as f:
            json.dump(students, f)
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        student_list = []

        with open(self._file_name) as f:
            try:
                data = json.load(f)
            except Exception:
                f.close()
                return
        for i in data.keys():
            data[i] = data[i].split(',')
            self.store(Student(data[i][0], data[i][1], data[i][2]))
        f.close()
