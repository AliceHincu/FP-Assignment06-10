from service.student_service import StudentService
from service.assignment_service import AssignmentService
from service.grade_service import GradeService
from validator.student_validator import StudentValidator
from validator.assignment_validator import AssignmentValidator
from validator.grade_validator import GradeValidator
from repository.student_repo import StudentRepo
from repository.assignment_repo import AssignmentRepo
from repository.grade_repo import GradeRepo
from service.undo_service import UndoService
from ui.ui_app import start_gui, start_ui, generate_assignments, generate_students
from ui.Settings import Settings


def start():
    try:
        s = Settings("settings.properties")
        file_student = s.get_student_repo()
        file_ass = s.get_assignment_repo()
        file_grade = s.get_grade_repo()

        student_validator = StudentValidator
        ass_validator = AssignmentValidator
        grade_validator = GradeValidator
        undo_service = UndoService()

        student_service = None
        ass_service = None
        grade_service = None


        if s.get_type() == 'inmemory':
            from MemoryRepo.StudentMemoryRepo import StudentMemoryRepository
            student_repo = StudentMemoryRepository()
            student_service = StudentService(student_repo, student_validator, undo_service)
            generate_students(student_service)

            from MemoryRepo.AssignmentMemoryRepo import AssignmentMemoryRepository
            ass_repo = AssignmentMemoryRepository()
            ass_service = AssignmentService(ass_repo, ass_validator, undo_service)
            generate_assignments(ass_service)

            from MemoryRepo.GradeMemoryRepository import GradeMemoryRepository
            grade_repo = GradeMemoryRepository
            grade_service = GradeService(grade_repo, grade_validator, undo_service)

        if s.get_type() == 'intextfiles':
            from TextRepo.StudentTextRepo import StudentTextFileRepository
            student_repo = StudentTextFileRepository(file_student)
            student_service = StudentService(student_repo, student_validator, undo_service)

            from TextRepo.AssignmentTextRepo import AssignmentTextFileRepository

            ass_repo = AssignmentTextFileRepository(file_ass)
            ass_service = AssignmentService(ass_repo, ass_validator, undo_service)

            from TextRepo.GradeTextRepo import GradeTextFileRepository
            grade_repo = GradeTextFileRepository(file_grade)
            grade_service = GradeService(grade_repo, grade_validator, undo_service)

        if s.get_type() == 'inpicklefiles':
            from PickleRepo.StudentPickleRepo import StudentPickleFileRepository
            student_repo = StudentPickleFileRepository(file_student)
            student_service = StudentService(student_repo, student_validator, undo_service)
            # generate_students(student_service)

            from PickleRepo.AssignmentPickleRepo import AssignmentPickleFileRepository
            ass_repo = AssignmentPickleFileRepository(file_ass)
            ass_service = AssignmentService(ass_repo, ass_validator, undo_service)
            # generate_assignments(ass_service)

            from PickleRepo.GradePickleRepo import GradePickleFileRepository
            grade_repo = GradePickleFileRepository(file_grade)
            grade_service = GradeService(grade_repo, grade_validator, undo_service)

        if s.get_type() == 'injsonfiles':
            from JsonRepo.StudentJsonRepo import StudentJsonFileRepository
            student_repo = StudentJsonFileRepository(file_student)
            student_service = StudentService(student_repo, student_validator, undo_service)
            # generate_students(student_service)

            from JsonRepo.AssignmentJsonRepo import AssignmentJsonFileRepository
            ass_repo = AssignmentJsonFileRepository(file_ass)
            ass_service = AssignmentService(ass_repo, ass_validator, undo_service)
            # generate_assignments(ass_service)

            from JsonRepo.GradeJsonRepo import GradeJsonFileRepository
            grade_repo = GradeJsonFileRepository(file_grade)
            grade_service = GradeService(grade_repo, grade_validator, undo_service)

        if s.get_type() == 'database':
            from DatabaseRepo.DatabaseStudent import StudentSqlRepo
            student_repo = StudentSqlRepo(file_student)
            student_service = StudentService(student_repo, student_validator, undo_service)

            from DatabaseRepo.DatabaseAssignment import AssignmentSqlRepo
            ass_repo = AssignmentSqlRepo(file_ass)
            ass_service = AssignmentService(ass_repo, ass_validator, undo_service)

            from DatabaseRepo.DatabaseGrade2 import GradeSqlRepo
            grade_repo = GradeSqlRepo(file_grade)
            grade_service = GradeService(grade_repo, grade_validator, undo_service)
            #from domain.Student import Student
            #student_repo.add(Student('22334', 'michale', '23'))
            #student_repo.get_list()

        if s.get_gui():
            start_gui(student_service, ass_service, grade_service, undo_service)
        else:
            start_ui(student_service, ass_service, grade_service, undo_service)

        #s.main()
    except ValueError as err:
        print(err)

start()