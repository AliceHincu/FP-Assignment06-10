from repository.assignment_repo import AssignmentRepo


class AssignmentMemoryRepository(AssignmentRepo):
    def __init__(self):
        super().__init__()

    def store(self, item):
        super().add(item)

    def delete(self, id_):
        super().remove(id_)

    def update_assignment(self, id_old, id_new, descr, day, month):
        super().update(id_old, id_new, descr, day, month)