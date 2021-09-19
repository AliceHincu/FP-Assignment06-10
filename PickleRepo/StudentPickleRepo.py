"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
# from domain.Student import Student
from repository.student_repo import StudentRepo
import pickle


class BinaryFileRepository(StudentRepo):
    pass


class ProductTextFileRepository(StudentRepo):
    pass


class StudentPickleFileRepository(StudentRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='students.pickle'):
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
        student_list = self._students

        f = open(self._file_name, 'wb')
        try:
            pickle.dump(student_list, f)
            f.close()
        except Exception:
            raise Exception("Something went wrong")

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        student_list = []

        try:
            f = open(self._file_name, 'rb')  # read text

            student_list = pickle.load(f)

            for student in student_list:
                self.store(student)

            f.close()

        except FileNotFoundError as e:
            raise FileNotFoundError()
        except EOFError:
            #EOFError is raised when one of the built-in functions input() or raw_input()
            #hits an end-of-file condition (EOF) without reading any data
            student_list = []
        except IOError as err:
            raise err

        f.close()
