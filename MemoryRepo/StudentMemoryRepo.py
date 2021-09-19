from repository.student_repo import StudentRepo


class StudentMemoryRepository(StudentRepo):
    def __init__(self):
        super().__init__()

    def store(self, item):
        super().add(item)

    def delete(self, id_):
        super().remove(id_)

    def update_student(self, id_old, id_new, name, gr):
        super().update(id_old, id_new, name, gr)