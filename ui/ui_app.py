import tkinter as tk
from tkinter import messagebox
from service.student_service import StudentService, StudentIdException
from service.assignment_service import AssignmentService, AssignmentIdException
from service.grade_service import GradeService, GradeStudentException
from validator.student_validator import StudentValidator, StudentException
from validator.assignment_validator import AssignmentValidator, AssignmentException
from validator.grade_validator import GradeValidator, GradeException
from repository.student_repo import StudentRepo
from repository.assignment_repo import AssignmentRepo
from repository.grade_repo import GradeRepo
from service.undo_service import UndoService, UndoRedoException
import names
import random
import tabulate
from datetime import date
import configparser


class GUI(tk.Frame):
    def __init__(self, student_service, assignment_service, grade_service, undo_service, root=None):
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service= grade_service
        self._undo_service = undo_service
        super().__init__(root)  # so UI can inherit the tkinter
        self.root = root
        root.geometry("1300x625")
        self.create_widgets_student_add()
        self.create_widgets_student_remove()
        self.create_widgets_student_update()
        self.create_widgets_student_list()
        self.create_widgets_assignment_add()
        self.create_widgets_assignment_remove()
        self.create_widgets_assignment_update()
        self.create_widgets_assignment_list()
        self.create_widgets_give_homework_student()
        self.create_widgets_give_homework_group()
        self.create_widgets_list_homework()
        self.create_widgets_give_grade()
        self.create_widgets_show_grades()
        self.create_widgets_statistics1()
        self.create_widgets_statistics2()
        self.create_widgets_statistics3()
        self.create_widgets_undo()

    def create_widgets_student_add(self):
        # the beginning
        student_label = tk.Label(self.root, text="----- Student ¯\_(⌣̯̀⌣́)_/¯ -----")
        student_label.grid(row=0, column=0, columnspan=2)
        # the white bars for add
        student_id = tk.Entry()
        name = tk.Entry()
        group = tk.Entry()
        student_id.grid(row=1, column=1)
        name.grid(row=2, column=1)
        group.grid(row=3, column=1)

        # the labels
        id_label = tk.Label(self.root, text="ID:")
        name_label = tk.Label(self.root, text="Name:")
        group_label = tk.Label(self.root, text="Group:")
        id_label.grid(row=1, column=0)
        name_label.grid(row=2, column=0)
        group_label.grid(row=3, column=0)

        # Create the application variable and set it to some value.
        # Tell the entry widget to watch this variable.
        student_id["textvariable"] = tk.StringVar().set("")
        name["textvariable"] = tk.StringVar().set("")
        group["textvariable"] = tk.StringVar().set("")

        button_add = tk.Button(self.root, text="Add student", padx=40, pady=10,
                               command=lambda: self.button_add(student_id.get(), name.get(), group.get()))

        button_add.grid(row=4, column=0, columnspan=2)

    def create_widgets_assignment_add(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=0, column=3)
        student_label = tk.Label(self.root, text="----- Assignment ╚(•⌂•)╝ -----")
        student_label.grid(row=0, column=4, columnspan=3)

        # the white bars for add
        ass_id = tk.Entry()
        description = tk.Entry()
        ass_id.grid(row=1, column=5, columnspan=2)
        description.grid(row=2, column=5, columnspan=2)

        # the labels for bars
        id_label = tk.Label(self.root, text="ID:")
        description_label = tk.Label(self.root, text="Description:")
        deadline_label = tk.Label(self.root, text="Deadline:")
        id_label.grid(row=1, column=4)
        description_label.grid(row=2, column=4)
        deadline_label.grid(row=3, column=4)

        # Create the application variable and set it to some value.
        # Tell the entry widget to watch this variable.
        ass_id["textvariable"] = tk.StringVar().set("")
        description["textvariable"] = tk.StringVar().set("")

        # for deadline: dropdown menu
        options_day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                       "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                       "24", "25", "26", "27", "28", "29", "30", "31"]
        options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        clicked_day = tk.StringVar()
        clicked_day.set(options_day[0])
        clicked_month = tk.StringVar()
        clicked_month.set(options_month[0])

        deadline_day = tk.OptionMenu(self.root, clicked_day, *options_day)
        deadline_month = tk.OptionMenu(self.root, clicked_month, *options_month)
        deadline_day.grid(row=3, column=5)
        deadline_month.grid(row=3, column=6)

        button_add = tk.Button(self.root, text="Add assignment", padx=40, pady=10,
                               command=lambda: self.button_add_assignment(ass_id.get(), description.get(),
                                                                          clicked_day.get(), clicked_month.get()))

        button_add.grid(row=4, column=4, columnspan=3)

    def create_widgets_student_remove(self):
        # the labels
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=5, column=0)
        id_label = tk.Label(self.root, text="ID:")
        id_label.grid(row=6, column=0)

        # the white bars for add
        student_id = tk.Entry()
        student_id.grid(row=6, column=1)
        student_id["textvariable"] = tk.StringVar().set("")

        button_remove = tk.Button(self.root, text="Remove student", padx=31, pady=10,
                                  command=lambda: self.button_remove(student_id.get()))

        button_remove.grid(row=7, column=0, columnspan=2)

    def create_widgets_assignment_remove(self):
        # the labels
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=5, column=4)
        id_label = tk.Label(self.root, text="ID:")
        id_label.grid(row=6, column=4)

        # the white bars for add
        student_id = tk.Entry()
        student_id.grid(row=6, column=5, columnspan=2)
        student_id["textvariable"] = tk.StringVar().set("")

        button_remove = tk.Button(self.root, text="Remove assignment", padx=31, pady=10,
                                  command=lambda: self.button_remove_assignment(student_id.get()))

        button_remove.grid(row=7, column=4, columnspan=3)

    def create_widgets_student_update(self):
        # the labels
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=8, column=0)
        old_id_label = tk.Label(self.root, text="Old ID:")
        new_id_label = tk.Label(self.root, text="New ID:")
        name_label = tk.Label(self.root, text="New Name:")
        group_label = tk.Label(self.root, text="New Group:")
        old_id_label.grid(row=9, column=0)
        new_id_label.grid(row=10, column=0)
        name_label.grid(row=11, column=0)
        group_label.grid(row=12, column=0)

        # the white bars for add
        old_id = tk.Entry()
        new_id = tk.Entry()
        name = tk.Entry()
        group = tk.Entry()
        old_id.grid(row=9, column=1)
        new_id.grid(row=10, column=1)
        name.grid(row=11, column=1)
        group.grid(row=12, column=1)

        button_update = tk.Button(self.root, text="Update student", padx=40, pady=10,
                                  command=lambda: self.button_update(old_id.get(), new_id.get(), name.get(),
                                                                     group.get()))
        button_update.grid(row=13, column=0, columnspan=2)

    def create_widgets_assignment_update(self):
        # the labels
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=8, column=4)

        old_id_label = tk.Label(self.root, text="Old ID:")
        new_id_label = tk.Label(self.root, text="New ID:")
        description_label = tk.Label(self.root, text="New Description:")
        deadline_label = tk.Label(self.root, text="New Deadline:")
        old_id_label.grid(row=9, column=4)
        new_id_label.grid(row=10, column=4)
        description_label.grid(row=11, column=4)
        deadline_label.grid(row=12, column=4)

        # the white bars for add
        old_id = tk.Entry()
        new_id = tk.Entry()
        description = tk.Entry()
        old_id.grid(row=9, column=5, columnspan=2)
        new_id.grid(row=10, column=5, columnspan=2)
        description.grid(row=11, column=5, columnspan=2)

        # for deadline: dropdown menu
        options_day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                       "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                       "24", "25", "26", "27", "28", "29", "30", "31"]
        options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        clicked_day = tk.StringVar()
        clicked_day.set(options_day[0])
        clicked_month = tk.StringVar()
        clicked_month.set(options_month[0])

        deadline_day = tk.OptionMenu(self.root, clicked_day, *options_day)
        deadline_month = tk.OptionMenu(self.root, clicked_month, *options_month)
        deadline_day.grid(row=12, column=5)
        deadline_month.grid(row=12, column=6)

        button_update_assignment = tk.Button(self.root, text="Update assignment", padx=40, pady=10,
                                             command=lambda: self.button_update_assignment(old_id.get(), new_id.get(),
                                                                                           description.get(),
                                                                                           clicked_day.get(),
                                                                                           clicked_month.get()))
        button_update_assignment.grid(row=13, column=4, columnspan=3)

    def create_widgets_student_list(self):
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=14, column=0)

        button_list = tk.Button(self.root, text="Show students", padx=40, pady=10,
                                command=self.button_list)
        button_list.grid(row=15, column=0, columnspan=2)

    def create_widgets_assignment_list(self):
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=14, column=4)

        button_list = tk.Button(self.root, text="Show assignments", padx=40, pady=10,
                                command=self.button_list_assignment)
        button_list.grid(row=15, column=4, columnspan=3)

    def create_widgets_give_homework_student(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=0, column=7)
        homework_label = tk.Label(self.root, text="----- Homework (〜￣▽￣)〜 -----")
        homework_label.grid(row=0, column=8, columnspan=2)

        # to a student
        one_student_label = tk.Label(self.root, text="--- to a student ---")
        one_student_label.grid(row=1, column=8, columnspan=2)

        st_label = tk.Label(self.root, text="Student ID:")
        st_label.grid(row=2, column=8)
        student_id = tk.Entry()
        student_id.grid(row=2, column=9)
        student_id["textvariable"] = tk.StringVar().set("")

        ass_label = tk.Label(self.root, text="Assignment ID:")
        ass_label.grid(row=3, column=8)
        assignment_id = tk.Entry()
        assignment_id.grid(row=3, column=9)
        assignment_id["textvariable"] = tk.StringVar().set("")

        button_add = tk.Button(self.root, text="Give homework to student", padx=40, pady=10,
                               command=lambda: self.give_homework_to_student(student_id.get(), assignment_id.get()))

        button_add.grid(row=4, column=8, columnspan=2)

    def create_widgets_give_homework_group(self):
        # to a group
        one_group_label = tk.Label(self.root, text="--- to a group ---")
        one_group_label.grid(row=6, column=8, columnspan=2)

        gr_label = tk.Label(self.root, text="Group Number:")
        gr_label.grid(row=7, column=8)
        group_id = tk.Entry()
        group_id.grid(row=7, column=9)
        group_id["textvariable"] = tk.StringVar().set("")

        ass_label = tk.Label(self.root, text="Assignment ID:")
        ass_label.grid(row=8, column=8)
        assignment_id = tk.Entry()
        assignment_id.grid(row=8, column=9)
        assignment_id["textvariable"] = tk.StringVar().set("")

        button_add = tk.Button(self.root, text="Give homework to group", padx=40, pady=10,
                               command=lambda: self.give_homework_to_group(group_id.get(), assignment_id.get()))

        button_add.grid(row=9, column=8, columnspan=2)

    def create_widgets_list_homework(self):
        button_add = tk.Button(self.root, text="List homework", padx=40, pady=10,
                               command=self.list_homework)

        button_add.grid(row=12, column=8, columnspan=2)

    def create_widgets_give_grade(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=0, column=10)
        homework_label = tk.Label(self.root, text="----- Grades (〜￣▽￣)〜 -----")
        homework_label.grid(row=0, column=11, columnspan=2)

        # to a student
        one_student_label = tk.Label(self.root, text="--- grade student ---")
        one_student_label.grid(row=1, column=11, columnspan=2)

        st_label = tk.Label(self.root, text="Student ID:")
        st_label.grid(row=2, column=11)
        student_id = tk.Entry()
        student_id.grid(row=2, column=12)
        student_id["textvariable"] = tk.StringVar().set("")

        # button
        button_add = tk.Button(self.root, text="See student's assignments", padx=40, pady=10,
                               command=lambda: self.create_widgets_student_assignment(student_id.get()))

        button_add.grid(row=3, column=11, columnspan=2)

    def create_widgets_student_assignment(self, id):
        if self._student_service.check_for_unique_id(id) == False:
            messagebox.showerror("This is a popup!", "The student doesn't exist!")
        else:
            one_student_label = tk.Label(self.root, text="--- give grade ---")
            one_student_label.grid(row=5, column=11, columnspan=2)

            st_label = tk.Label(self.root, text="Assignment ID:")
            st_label.grid(row=6, column=11)

            homeworks = self._grade_service.student_assignments(id)

            # for deadline: dropdown menu
            if len(homeworks) == 0:
                none_label = tk.Label(self.root, text="-")
                none_label.grid(row=6, column=12)
            else:
                options = homeworks
                clicked = tk.StringVar()
                clicked.set(" ")

                choose_assignment = tk.OptionMenu(self.root, clicked, *options)
                choose_assignment.grid(row=6, column=12)

                grade_label = tk.Label(self.root, text="Grade:")
                grade_label.grid(row=7, column=11)
                grade = tk.Entry()
                grade.grid(row=7, column=12)
                grade["textvariable"] = tk.StringVar().set("")

                button_grade_assignment = tk.Button(self.root, text="Grade assignment", padx=40, pady=10,
                                                     command=lambda: self.button_grade_assignment(id, choose_assignment,
                                                                                                  grade.get(),
                                                                                                  clicked.get()),
                                                    )
                button_grade_assignment.grid(row=8, column=11, columnspan=2)

    def create_widgets_show_grades(self):
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=9, column=11)

        button_list = tk.Button(self.root, text="Show grades", padx=40, pady=10,
                                command=self.show_grades)
        button_list.grid(row=10, column=11, columnspan=2)

    def create_widgets_statistics1(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=0, column=13)
        homework_label = tk.Label(self.root, text="----- Statistics (〜￣▽￣)〜 -----")
        homework_label.grid(row=0, column=14, columnspan=2)

        # first statistic
        one_label = tk.Label(self.root, text="1. All students.txt who received a given assignment,")
        one_label.grid(row=1, column=14, columnspan=2)

        two_label = tk.Label(self.root, text="ordered by average grade for that assignment.")
        two_label.grid(row=2, column=14, columnspan=2)

        id_label = tk.Label(self.root, text="Assignment ID:")
        id_label.grid(row=3, column=14)
        id = tk.Entry()
        id.grid(row=3, column=15)
        id["textvariable"] = tk.StringVar().set("")
        # button
        button_add = tk.Button(self.root, text="Show statistics", padx=40, pady=10,
                               command=lambda: self.statistics1(id.get()))

        button_add.grid(row=4, column=14, columnspan=2)

    def create_widgets_statistics2(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=5, column=13)

        # first statistic
        one_label = tk.Label(self.root, text="2. All students.txt who are late in handing in at least")
        one_label.grid(row=6, column=14, columnspan=2)

        two_label = tk.Label(self.root, text=" one assignment. These are all the students.txt who have")
        two_label.grid(row=7, column=14, columnspan=2)

        third_label = tk.Label(self.root, text="an ungraded assignment for which the deadline has passed.")
        third_label.grid(row=8, column=14, columnspan=2)

        # button
        button_add = tk.Button(self.root, text="Show statistics", padx=40, pady=10,
                               command=self.statistics2)

        button_add.grid(row=9, column=14, columnspan=2)

    def create_widgets_statistics3(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=9, column=13)

        # first statistic
        one_label = tk.Label(self.root, text="3. Students with the best school situation, sorted in")
        one_label.grid(row=10, column=14, columnspan=2)

        two_label = tk.Label(self.root, text=" descending order of the average grade received")
        two_label.grid(row=11, column=14, columnspan=2)

        third_label = tk.Label(self.root, text="for all assignments.")
        third_label.grid(row=12, column=14, columnspan=2)

        # button
        button_add = tk.Button(self.root, text="Show statistics", padx=40, pady=10,
                               command=self.statistics3)

        button_add.grid(row=13, column=14, columnspan=2)

    def create_widgets_undo(self):
        # the beginning
        space_label = tk.Label(self.root, text=" ")
        space_label.grid(row=14, column=13)

        button_undo = tk.Button(self.root, text="Undo", padx=40, pady=10,
                               command=self.undo)

        button_undo.grid(row=16, column=14, columnspan=2)

        button_redo= tk.Button(self.root, text="Redo", padx=40, pady=10,
                                command=self.redo)

        button_redo.grid(row=17, column=14, columnspan=2)

    def statistics1(self, id):
        grades = self._grade_service.order_grades(id)
        height = len(grades) + 1
        width = 3
        table_window = tk.Toplevel()
        table_header_list = ["student_ID", "assignment_ID", "grade"]

        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(table_window, text="")
                b.grid(row=i, column=j)
                if i == 0:
                    b.insert(0, table_header_list[j])
                else:
                    b.insert(0, grades[i - 1][j])
                b.config(state='disabled')

    def statistics2(self):
        today = date.today()
        day = today.day
        month_number = today.month
        homeworks = self._grade_service.display()
        homework_list = self._assignment_service.get_late_homework(homeworks, day, month_number)
        student_list = self._grade_service.get_late_students(homework_list)

        height = len(student_list) + 1
        table_window = tk.Toplevel()
        table_header_list = ["student_ID"]

        for i in range(height):  # Rows
            b = tk.Entry(table_window, text="")
            b.grid(row=i, column=0)
            if i == 0:
                b.insert(0, table_header_list[i])
            else:
                b.insert(0, student_list[i-1])
                b.config(state='disabled')

    def statistics3(self):
        grades = self._grade_service.order_total_grades(self._student_service.display())
        height = len(grades) + 1
        width = 2
        table_window = tk.Toplevel()
        table_header_list = ["student_ID", "grade"]

        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(table_window, text="")
                b.grid(row=i, column=j)
                if i == 0:
                    b.insert(0, table_header_list[j])
                else:
                    b.insert(0, grades[i - 1][j])
                b.config(state='disabled')

    def button_add(self, id, name, group):
        try:
            self._student_service.create_student(id, name, group)
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Student added successfully!")
        except (StudentException, StudentIdException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def button_add_assignment(self, id, description, deadline_day, deadline_month):
        try:
            self._assignment_service.create_assignment(id, description, [deadline_day, deadline_month])
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Assignment added successfully!")
        except (AssignmentException, AssignmentIdException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def button_remove(self, id):
        try:
            self._student_service.remove_student(id)
            self._grade_service.delete_grade_student(id)
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Student removed successfully!")
        except (StudentException, StudentIdException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def button_remove_assignment(self, id):
        try:
            self._assignment_service.remove_assignment(id)
            self._grade_service.delete_grade_assignment(id)
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Assignment removed successfully!")
        except (AssignmentException, AssignmentIdException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def button_update(self, old_id, new_id, name, group):
        try:
            self._student_service.update_student(old_id, new_id, name, group)
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Student updated successfully!")
        except (StudentException, StudentIdException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def button_update_assignment(self, old_id, new_id, description, deadline_day, deadline_month):
        try:
            self._assignment_service.update_assignment(old_id, new_id, description, deadline_day, deadline_month)
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Assignment updated successfully!")
        except (AssignmentException, AssignmentIdException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def button_list(self):
        students = self._student_service.display()
        height = len(students)+1
        width = 3
        table_window = tk.Toplevel()
        table_header_list = ["ID", "Name", "Group"]

        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(table_window, text="")
                b.grid(row=i, column=j)
                if i == 0:
                    b.insert(0, table_header_list[j])
                else:
                    b.insert(0, students[i-1][j])
                b.config(state='disabled')

    def button_list_assignment(self):
        assignments = self._assignment_service.display()
        height = len(assignments) + 1
        width = 4
        table_window = tk.Toplevel()
        table_header_list = ["ID", "Description", "deadline day", "deadline month"]

        for i in range(height):  # Rows
            for j in range(width):  # Columns
                if j == 1:
                    b = tk.Entry(table_window, text="", width=50)
                else:
                    b = tk.Entry(table_window, text="")
                b.grid(row=i, column=j)
                if i == 0:
                    b.insert(0, table_header_list[j])
                else:
                    b.insert(0, assignments[i - 1][j])
                b.config(state='disabled')

    def give_homework_to_student(self, student_id, assignment_id):
        try:
            if self._student_service.check_for_unique_id(student_id):
                if self._assignment_service.check_for_unique_id(assignment_id):
                    self._grade_service.create_homework(student_id, assignment_id)
                    messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Homework assigned successfully!")
                else:
                    raise GradeException("The assignment does not exist")
            else:
                raise GradeStudentException("The student does not exist")
        except (GradeException, GradeStudentException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def give_homework_to_group(self, group_number, assignment_id):
        try:
            if self._student_service.check_for_unique_group(group_number):
                if self._assignment_service.check_for_unique_id(assignment_id):
                    self._grade_service.create_homework_gr(group_number, assignment_id, self._student_service)
                    messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Homework assigned successfully!")
                else:
                    raise GradeException("The assignment does not exist")
            else:
                raise GradeException("The group does not exist")
        except (GradeException, GradeStudentException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def list_homework(self):
        homeworks = self._grade_service.display()
        height = len(homeworks) + 1
        width = 2
        table_window = tk.Toplevel()
        table_header_list = ["student_ID", "assignment_ID"]

        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(table_window, text="")
                b.grid(row=i, column=j)
                if i == 0:
                    b.insert(0, table_header_list[j])
                else:
                    b.insert(0, homeworks[i - 1][j])
                b.config(state='disabled')

    def button_grade_assignment(self, student_id, choose_assignment, grade, assignment_id):
        try:
            choose_assignment.destroy()
            self._grade_service.grade_student(student_id, grade, assignment_id)
            messagebox.showinfo("This is a popup!", "ヾ(･ω･*)ﾉ Grade assigned successfully!")
            self.create_widgets_student_assignment(student_id)
        except (GradeException, GradeStudentException) as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def show_grades(self):
        grades = self._grade_service.display_grades()
        height = len(grades) + 1
        width = 3
        table_window = tk.Toplevel()
        table_header_list = ["student_ID", "assignment_ID", "grade"]

        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(table_window, text="")
                b.grid(row=i, column=j)
                if i == 0:
                    b.insert(0, table_header_list[j])
                else:
                    b.insert(0, grades[i - 1][j])
                b.config(state='disabled')

    def undo(self):
        try:
            self._undo_service.undo()
        except UndoRedoException as val_err:
            messagebox.showerror("This is a popup!", val_err)

    def redo(self):
        try:
            self._undo_service.redo()
        except UndoRedoException as val_err:
            messagebox.showerror("This is a popup!", val_err)


def generate_students(service):
    id_list = []
    for i in range(10):
        name = str(names.get_full_name())
        id = str(random.randint(10000, 99999))
        while id is id_list:
            id = str(random.randint(10000, 99999))
        id_list.append(id)
        group = str(random.randint(1,10))
        service.create_student(id, name, group)


def generate_assignments(service):
    id_list = []
    for i in range(10):
        id = str(random.randint(1000, 9999))
        while id is id_list:
            id = str(random.randint(1000, 9999))
        id_list.append(id)

        day = str(random.randint(1, 28))

        options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        month = random.choice(options_month)

        descriptions = []
        options_description = ["For english just an essay", "japanese - 400word essay",
                               "Just do it on time", "Cats vs dogs: but make it spicy",
                               "Why Gravity falls is the best cartoon: 300words",
                               "Abortion in Poland :legal only in cases of rape and incest -1000words",
                               "Markiplier: Why is he the best youtuber",
                               "Top of the morning to ya ladies", "History of Corpse and his music",
                               "It's not much but it's honest work", "you're actually reading the descriptions?",
                               "cum intrebi un orb daca are guma? -Ai oribit?",
                               "why you should always accept cash instead of criticism",
                               "Why the H from boys comes from the word 'honesty'"]
        description = random.choice(options_description)
        while description in descriptions:
            description = random.choice(options_description)

        service.create_assignment(id, description, [day, month])


def start_gui(student_service, ass_service, grade_service, undo_service):
    root = tk.Tk()
    myapp = GUI(student_service, ass_service, grade_service, undo_service, root)
    myapp.mainloop()


# ---- UI FUNCTIONS -----


def print_menu_ui():
    print("---- Student ----")
    print("\t1. Add student")
    print("\t2. Remove student")
    print("\t3. Update student")
    print("\t4. Show students.txt")
    print("---- Assignment ----")
    print("\t5. Add assignment")
    print("\t6. Remove assignment")
    print("\t7. Update assignment")
    print("\t8. Show assignment")
    print("---- Homework ----")
    print("\t9. Give assignment to student")
    print("\t10. Give assignment to group")
    print("\t11. Show homework list")
    print("---- Exit ----")
    print("\t0. Exit")


def add_student_ui(student_service):
    id = input("Give id: ")
    name = input("Give name: ")
    group = input("Give group: ")
    try:
        student_service.create_student(id, name, group)
        print("\nヾ(･ω･*)ﾉ Student added successfully!")
    except (StudentException, StudentIdException) as val_err:
        print("\n" + str(val_err))


def remove_student_ui(student_service):
    id = input("Give id: ")
    try:
        student_service.remove_student(id)
        print("\nヾ(･ω･*)ﾉ Student removed successfully!")
    except (StudentException, StudentIdException) as val_err:
        print("\n" + str(val_err))


def update_student_ui(student_service):
    old_id = input("Give old_id: ")
    new_id = input("Give new_id: ")
    name = input("Give name: ")
    group = input("Give group: ")
    try:
        student_service.update_student(old_id, new_id, name, group)
        print("\nヾ(･ω･*)ﾉ Student removed successfully!")
    except (StudentException, StudentIdException) as val_err:
        print("\n" + str(val_err))


def list_student_ui(student_service):
    students = student_service.display()
    headers = ["ID", "Name", "Group"]
    print(tabulate.tabulate(students, headers, tablefmt="pretty"))


def add_assignment_ui(assignment_service):
    id = input("Give id: ")
    description = input("Give description: ")
    deadline_day = input("Give deadline day: ")
    deadline_month = input("Give deadline month: ")
    options_day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                   "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                   "24", "25", "26", "27", "28", "29", "30", "31"]
    options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                     "sep", "oct", "nov", "dec"]
    try:
        if not deadline_day in options_day:
            raise ValueError
        if not deadline_month in options_month:
            raise ValueError
        try:
            assignment_service.create_assignment(id, description, [deadline_day, deadline_month])
            print("\nヾ(･ω･*)ﾉ Assignment added successfully!")
        except (AssignmentException, AssignmentIdException) as val_err:
            print("\n" + str(val_err))
    except ValueError:
        print("The deadline is not good!")


def remove_assignment_ui(assignment_service):
    id = input("Give id: ")
    try:
        assignment_service.remove_assignment(id)
        print("\nヾ(･ω･*)ﾉ Assignment removed successfully!")
    except (AssignmentException, AssignmentIdException) as val_err:
        print("\n" + str(val_err))


def update_assignment_ui(assignment_service):
    old_id = input("Give old_id: ")
    new_id = input("Give new_id: ")
    description = input("Give description: ")
    deadline_day = input("Give deadline day: ")
    deadline_month = input("Give deadline month: ")
    options_day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                   "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                   "24", "25", "26", "27", "28", "29", "30", "31"]
    options_month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                     "sep", "oct", "nov", "dec"]
    try:
        if not deadline_day in options_day:
            raise ValueError
        if not deadline_month in options_month:
            raise ValueError
        try:
            assignment_service.update_assignment(old_id, new_id, description, deadline_day, deadline_month)
            print("\nヾ(･ω･*)ﾉ Assignment removed successfully!")
        except (AssignmentException, AssignmentIdException) as val_err:
            print("\n" + str(val_err))
    except ValueError:
        print("The deadline is not good")


def list_assignment_ui(assignment_service):
    assignments = assignment_service.display()
    headers = ["ID", "Description", "Deadline day", "Deadline month"]
    print(tabulate.tabulate(assignments, headers, tablefmt="pretty"))


def give_homework_to_student_ui(student_service, assignment_service, grade_service):
    student_id = input("Give student ID: ")
    assignment_id = input("Give assignment ID: ")
    try:
        if student_service.check_for_unique_id(student_id):
            if assignment_service.check_for_unique_id(assignment_id):
                grade_service.create_homework(student_id, assignment_id)
                print("ヾ(･ω･*)ﾉ Homework assigned successfully!")
            else:
                raise GradeException("The assignment does not exist")
        else:
            raise GradeStudentException("The student does not exist")
    except (GradeException, GradeStudentException) as val_err:
        print(val_err)


def give_homework_to_group_ui(student_service, assignment_service, grade_service):
    group_number = input("Give group number: ")
    assignment_id = input("Give assignment ID: ")
    try:
        if student_service.check_for_unique_group(group_number):
            if assignment_service.check_for_unique_id(assignment_id):
                grade_service.create_homework_gr(group_number, assignment_id, student_service)
                print("ヾ(･ω･*)ﾉ Homework assigned successfully!")
            else:
                raise GradeException("The assignment does not exist")
        else:
            raise GradeException("The group does not exist")
    except (GradeException, GradeStudentException) as val_err:
        print(val_err)


def list_homework_ui(grade_service):
    homeworks = grade_service.display()
    headers = ["student_ID", "assignment_ID", "grade"]
    print(tabulate.tabulate(homeworks, headers, tablefmt="pretty"))


def start_ui(student_service, ass_service, grade_service, undo_service):
    print_menu_ui()
    done = False
    while not done:
        command = input("\ncommand> ")
        if command == "1":
            add_student_ui(student_service)
        elif command == "2":
            remove_student_ui(student_service)
        elif command == "3":
            update_student_ui(student_service)
        elif command == "4":
            list_student_ui(student_service)
        elif command == "5":
            add_assignment_ui(ass_service)
        elif command == "6":
            remove_assignment_ui(ass_service)
        elif command == "7":
            update_assignment_ui(ass_service)
        elif command == "8":
            list_assignment_ui(ass_service)
        elif command == "9":
            give_homework_to_student_ui(student_service, ass_service, grade_service)
        elif command == "10":
            give_homework_to_group_ui(student_service, ass_service, grade_service)
        elif command == "11":
            list_homework_ui(grade_service)
        elif command == "0":
            print("Goodbye!")
            done = True
        else:
            print("Wrong command!")


def start_menu(student_service, ass_service, grade_service, undo_service):
    print("1. GUI")
    print("2. UI")
    done = True
    while done:
        command = input("command> ")
        if command == "1":
            start_gui(student_service, ass_service, grade_service, undo_service)
            done = False
        elif command == "2":
            start_ui(student_service, ass_service, grade_service, undo_service)
            done = False
        else:
            print("Wrong command!")


def start():
    undo_service = UndoService()
    config = configparser.ConfigParser()
    config.read("settings.properties")
    student_repo = None
    student_validator = StudentValidator
    student_service = None
    ass_repo = None
    ass_validator = AssignmentValidator
    ass_service = None
    grade_repo = None
    grade_validator = GradeValidator
    grade_service = None

    if str(config["Settings"]["repository"]) == 'inmemory':
        from MemoryRepo.StudentMemoryRepo import StudentMemoryRepository
        student_repo = StudentMemoryRepository()
        student_service = StudentService(student_repo, student_validator, undo_service)
        generate_students(student_service)

        from MemoryRepo.AssignmentMemoryRepo import AssignmentMemoryRepository
        ass_repo = AssignmentMemoryRepository
        ass_service = AssignmentService(ass_repo, ass_validator, undo_service)
        generate_assignments(ass_service)

        from MemoryRepo.GradeMemoryRepository import GradeMemoryRepository
        grade_repo = GradeMemoryRepository
        grade_service = GradeService(grade_repo, grade_validator, undo_service)

        start_menu(student_service, ass_service, grade_service, undo_service)

    if str(config["Settings"]["repository"]) == 'intextfiles':
        from TextRepo.StudentTextRepo import StudentTextFileRepository
        file_student = config.get('Settings', 'students')

        student_repo = StudentTextFileRepository(file_student)
        student_service = StudentService(student_repo, student_validator, undo_service)

        from TextRepo.AssignmentTextRepo import AssignmentTextFileRepository
        file_ass = config.get('Settings', 'assignments')

        ass_repo = AssignmentTextFileRepository(file_ass)
        ass_service = AssignmentService(ass_repo, ass_validator, undo_service)

        from TextRepo.GradeTextRepo import GradeTextFileRepository
        file_grade = config.get('Settings', 'grades')

        grade_repo = GradeTextFileRepository(file_grade)
        grade_service = GradeService(grade_repo, grade_validator, undo_service)

    if str(config["Settings"]["repository"]) == 'inpicklefiles':
        from TextRepo.StudentTextRepo import StudentTextFileRepository
        file_student = config.get('Settings', 'students')

        from PickleRepo.StudentPickleRepo import StudentPickleFileRepository
        student_repo = StudentPickleFileRepository(file_student)
        student_service = StudentService(student_repo, student_validator, undo_service)
        #generate_students(student_service)

        from PickleRepo.AssignmentPickleRepo import AssignmentPickleFileRepository
        file_ass = config.get('Settings', 'assignments')

        ass_repo = AssignmentPickleFileRepository(file_ass)
        ass_service = AssignmentService(ass_repo, ass_validator, undo_service)
        #generate_assignments(ass_service)

        from PickleRepo.GradePickleRepo import GradePickleFileRepository
        file_grade = config.get('Settings', 'grades')

        grade_repo = GradePickleFileRepository(file_grade)
        grade_service = GradeService(grade_repo, grade_validator, undo_service)

    if str(config["Settings"]["repository"]) == 'injsonfiles':
        from JsonRepo.StudentJsonRepo import StudentJsonFileRepository
        file_student = config.get('Settings', 'students')

        student_repo = StudentJsonFileRepository(file_student)
        student_service = StudentService(student_repo, student_validator, undo_service)
        #generate_students(student_service)

        from JsonRepo.AssignmentJsonRepo import AssignmentJsonFileRepository
        file_ass = config.get('Settings', 'assignments')

        ass_repo = AssignmentJsonFileRepository(file_ass)
        ass_service = AssignmentService(ass_repo, ass_validator, undo_service)
        #generate_assignments(ass_service)

        from JsonRepo.GradeJsonRepo import GradeJsonFileRepository
        file_grade = config.get('Settings', 'grades')

        grade_repo = GradeJsonFileRepository(file_grade)
        grade_service = GradeService(grade_repo, grade_validator, undo_service)

    if str(config["Settings"]["ui"]) == 'gui':
        start_gui(student_service, ass_service, grade_service, undo_service)
    elif str(config["Settings"]["ui"]) == 'ui':
        start_ui(student_service, ass_service, grade_service, undo_service)



#start()
