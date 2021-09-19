"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Grade import Grade
from repository.grade_repo import GradeRepo


class GradeTextFileRepository(GradeRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='grades.txt'):
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
        f = open(self._file_name, 'wt')
        for gr in self._grades:
            line = str(gr[0]) + ';' + str(gr[1]) + ';' + str(gr[2])
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        grade_list = []

        try:
            f = open(self._file_name, 'rt')  # read text

            line = f.readline().strip()

            while len(line) > 0:
                line = line.split(";")
                grade_list.append(Grade(line[0], line[1], line[2]))
                line = f.readline().strip()

            for grade in grade_list:
                super().add_grade(grade)
        except FileNotFoundError as e:
            raise FileNotFoundError()