"""
- Implement a new repository that is able to persist data to text files
- Keep the functionalities from Repository class (code reuse, don't write things twice,
    swap the memory-repo with the text-repo) -> modules are independent and interchangeable
- Learn about inheritance
"""
from domain.Student import Student
from repository.student_repo import StudentRepo


class BinaryFileRepository(StudentRepo):
    pass


class ProductTextFileRepository(StudentRepo):
    pass


class StudentTextFileRepository(StudentRepo):
    """
    Inheritance -> TextFileRepository 'IS A' Repository
    What we want:
        1. TextFileRepository behaves EXACTLY like Repository
            with one exception
        2. Students are saved to/loaded from a text file
    """

    def __init__(self, file_name='students.txt'):
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
        f = open(self._file_name, 'wt')
        for student in self._students:
            line = str(student.id) + ';' + student.name + ';' + str(student.group)
            f.write(line)
            f.write('\n')
        f.close()

    def _load(self):
        """
        Load data from file
        We assume file-saved data is valid
        """
        student_list = []

        try:
            f = open(self._file_name, 'rt')  # read text

            line = f.readline().strip()

            while len(line) > 0:
                line = line.split(";")
                student_list.append(Student(line[0], line[1], line[2]))
                line = f.readline().strip()

            for st in student_list:
                super().add(st)
        except FileNotFoundError as e:
            raise FileNotFoundError()