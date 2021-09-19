"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Grade import Grade
from repository.grade_repo import GradeRepo
import json


class GradeJsonFileRepository(GradeRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='grades.json'):
        super().__init__()
        self._file_name = file_name
        self._load()

    def store_hw(self, item):
        super().add_hw(item)
        self._save()

    def store_grade(self, item):
        super().add_grade(item)
        self._save()

    def delete_homework(self, id_):
        super().delete_hw(id_)
        self._save()

    def delete_grade(self, id_):
        super().delete_gr(id_)
        self._save()

    def delete_st(self, id_):
        super().delete_student(id_)
        self._save()

    def delete_ass(self, id_):
        super().delete_assignment(id_)
        self._save()

    def grade_st(self, gr):
        super().grade_student(gr)
        self._save()

    def undo_gr(self, homework, grade):
        super().undo_grade(homework, grade)
        self._save()

    def _save(self):
        grades = {}
        for i in range(len(self._grades)):
            grades[i] = str(self._grades[i][0]) + ',' + str(self._grades[i][1]) + ',' + str(self._grades[i][2])
        with open(self._file_name, 'w') as f:
            json.dump(grades, f)
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
            self.store_grade(Grade(data[i][0], data[i][1], data[i][2]))
        f.close()
