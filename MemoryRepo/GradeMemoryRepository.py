from repository.grade_repo import GradeRepo


class GradeMemoryRepository(GradeRepo):
    def __init__(self):
        super().__init__()

    def store_hw(self, item):
        super().add_hw(item)

    def store_grade(self, item):
        super().add_grade(item)

    def delete_homework(self, id_):
        super().delete_hw(id_)

    def delete_grade(self, id_):
        super().delete_gr(id_)

    def delete_st(self, id_):
        super().delete_student(id_)

    def delete_ass(self, id_):
        super().delete_assignment(id_)

    def grade_st(self, gr):
        super().grade_student(gr)

    def undo_gr(self, homework, grade):
        super().undo_grade(homework, grade)