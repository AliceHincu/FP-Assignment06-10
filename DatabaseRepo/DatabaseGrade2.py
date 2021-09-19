import sqlite3
from sqlite3 import Error
from repository.grade_repo import GradeRepo


class GradeSqlRepo(GradeRepo):
    def __init__(self, database_name):
        super().__init__()
        self._database = database_name
        self._connection = self.create_connection(database_name)
        self.main()
        self._load_database()

    def create_connection(self, datab):
        """ create a database connection to the SQLite database
            specified by db_file
        :return: Connection object or None
        """
        conn = None
        try:
            import os.path

            BASE_DIR = os.path.dirname(os.path.abspath(datab))
            db_path = os.path.join(BASE_DIR, "grades_store.db")
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
        return conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self._connection.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def main(self):
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS grades (
                                            s_id text NOT NULL,
                                            a_id text NOT NULL,
                                            grade text NOT NULL
                                    ); """

        # create tables
        if self._connection is not None:
            # create projects table
            self.create_table(sql_create_projects_table)
        else:
            print("Error! cannot create the database connection.")

    def store_hw(self, obj):
        """
        :param obj: type: class <Grade>
        :return:
        """
        super().add_hw(obj)

    def store_grade(self, obj):
        """
        :param obj: type: class <Grade>
        :return:
        """
        super().add_grade(obj)
        obj = (obj.s_id, obj.a_id, obj.value)
        sql = '''INSERT INTO grades (s_id, a_id, grade) VALUES (?, ?, ?);'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    def delete_homework(self, obj):
        super().delete_hw(obj)

    def delete_grade(self, obj):
        super().delete_gr(obj)
        sql = 'DELETE FROM grades WHERE s_id = ? and a_id = ? and grade = ?'
        current = self._connection.cursor()
        current.execute(sql, (obj.s_id, obj.a_id, obj.value))
        self._connection.commit()

    def grade_st(self, obj):
        super().grade_student(obj)
        obj = (obj.s_id, obj.a_id, obj.value)
        sql = '''INSERT INTO grades (s_id, a_id, grade) VALUES (?, ?, ?);'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    def delete_st(self, obj_id):
        super().delete_student(obj_id)
        sql = 'DELETE FROM grades WHERE s_id = ?'
        current = self._connection.cursor()
        current.execute(sql, (obj_id,))
        self._connection.commit()

    def delete_ass(self, obj_id):
        super().delete_assignment(obj_id)
        sql = 'DELETE FROM grades WHERE a_id = ?'
        current = self._connection.cursor()
        current.execute(sql, (obj_id,))
        self._connection.commit()

    def undo_gr(self, hw, gr):
        super().undo_grade(hw, gr)
        sql = 'DELETE FROM grades WHERE s_id = ? and a_id = ? and grade = ?'
        current = self._connection.cursor()
        current.execute(sql, (gr.s_id, gr.a_id, gr.value))
        self._connection.commit()

    def _load_database(self):
        current = self._connection.cursor()
        current.execute("SELECT * FROM grades")
        rows = current.fetchall()
        for row in rows:
            self._grades.append([row[0], row[1], row[2]])