"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
# from domain.Assignment import Assignment
from repository.assignment_repo import AssignmentRepo

import pickle


class AssignmentPickleFileRepository(AssignmentRepo):
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
        assignment_list = self._assignments

        f = open(self._file_name, 'wb')
        try:
            pickle.dump(assignment_list, f)
            f.close()
        except Exception:
            raise Exception("Something went wrong")

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        assignment_list = []

        try:
            f = open(self._file_name, 'rb')  # read text

            assignment_list = pickle.load(f)

            for assignment in assignment_list:
                self.store(assignment)

            f.close()

        except FileNotFoundError as e:
            raise FileNotFoundError()
        except EOFError:
            # EOFError is raised when one of the built-in functions input() or raw_input()
            # hits an end-of-file condition (EOF) without reading any data
            assignment_list = []
        except IOError as err:
            raise err

        f.close()