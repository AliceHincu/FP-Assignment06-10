"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Grade import Grade
from repository.grade_repo import GradeRepo
import pickle


class GradePickleFileRepository(GradeRepo):
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
        grade_list = self._grades

        f = open(self._file_name, 'wb')
        try:
            pickle.dump(grade_list, f)
            f.close()
        except Exception:
            raise Exception("Something went wrong")

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        grade_list = []

        try:
            f = open(self._file_name, 'rb')  # read text

            grade_list = pickle.load(f)

            for i in range(len(grade_list)):
                self.store_grade(Grade(grade_list[i][0], grade_list[i][1], grade_list[i][2]))

            f.close()

        except FileNotFoundError as e:
            raise FileNotFoundError()
        except EOFError:
            # EOFError is raised when one of the built-in functions input() or raw_input()
            # hits an end-of-file condition (EOF) without reading any data
            student_list = []
        except IOError as err:
            raise err

        f.close()