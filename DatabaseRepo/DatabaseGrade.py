import sqlite3
from sqlite3 import Error
from repository.grade_repo import GradeRepo


class GradeSqlRepo(GradeRepo):
    def __init__(self, database_name):
        super().__init__()
        self._database = database_name
        self._connection = self.create_connection(database_name)
        #self.main()
        #self._load_database()

    def create_connection(self, datab):
        """ create a database connection to the SQLite database
            specified by db_file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(datab)
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
                                            s_id text PRIMARY KEY,
                                            a_id text NOT NULL,
                                            grade text NOT NULL
                                    ); """
        sql_create_projects_table2 = """ CREATE TABLE IF NOT EXISTS homeworks (
                                            s_id text PRIMARY KEY,
                                            a_id text NOT NULL,
                                            grade text NOT NULL
                                    ); """

        # create tables
        if self._connection is not None:
            # create projects table
            self.create_table(sql_create_projects_table)
            self.create_table(sql_create_projects_table2)
        else:
            print("Error! cannot create the database connection.")

    def store_hw(self, obj):
        """
        :param obj: type: class <Grade>
        :return:
        """
        super().add_hw(obj)
        obj = (obj.s_id, obj.a_id, obj.value)
        sql = '''INSERT OR REPLACE INTO homeworks (s_id, a_id, grade) VALUES (?, ?, ?);'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    # def store_grade(self, obj):
    #     """
    #     :param obj: type: class <Grade>
    #     :return:
    #     """
    #     super().add_grade(obj)
    #     obj = (obj.s_id, obj.a_id, obj.value)
    #     print(obj)
    #     sql = '''INSERT OR REPLACE INTO grades (s_id, a_id, grade) VALUES (?, ?, ?);'''
    #     current = self._connection.cursor()
    #     current.execute(sql, obj)
    #     self._connection.commit()
    #
    def delete_homework(self, obj):
        super().delete_hw(obj)
        print(obj)
        sql = 'DELETE FROM homeworks WHERE s_id = ? and a_id = ?'
        current = self._connection.cursor()
        current.execute(sql, (obj.s_id, obj.a_id))
        self._connection.commit()
    #
    # def delete_grade(self, obj):
    #     super().delete_gr(obj)
    #     print(obj)
    #     sql = 'DELETE FROM grades WHERE s_id = ? and a_id = ? and grade = ?'
    #     current = self._connection.cursor()
    #     current.execute(sql, (obj.s_id, obj.a_id, obj.value))
    #     self._connection.commit()
    #
    # def delete_st(self, obj_id):
    #     super().delete_student(obj_id)
    #     sql = 'DELETE FROM homeworks WHERE s_id = ?'
    #     sql2 = 'DELETE FROM grades WHERE s_id = ?'
    #     current = self._connection.cursor()
    #     current.execute(sql, (obj_id,))
    #     current.execute(sql2, (obj_id,))
    #     self._connection.commit()
    #
    # def delete_ass(self, obj_id):
    #     super().delete_assignment(obj_id)
    #     sql = 'DELETE FROM homeworks WHERE a_id = ?'
    #     sql2 = 'DELETE FROM grades WHERE a_id = ?'
    #     current = self._connection.cursor()
    #     current.execute(sql, (obj_id,))
    #     current.execute(sql2, (obj_id,))
    #     self._connection.commit()
    #
    # def grade_st(self, obj):
    #     super().grade_student(obj)
    #     sql = 'DELETE FROM homeworks WHERE s_id = ? and a_id = ?'
    #     sql2 = '''INSERT OR REPLACE INTO grades (s_id, a_id, grade) VALUES (?, ?, ?);'''
    #     current = self._connection.cursor()
    #     current.execute(sql, (obj.s_id, obj.a_id))
    #     obj = (obj.s_id, obj.a_id, obj.value)
    #     current.execute(sql2, obj)
    #     self._connection.commit()
    #
    # def undo_gr(self, hw, gr):
    #     super().undo_grade(hw, gr)
    #     sql = 'DELETE FROM grades WHERE s_id = ? and a_id = ? and grade = ?'
    #     sql2 = '''INSERT OR REPLACE INTO homeworks (s_id, a_id, grade) VALUES (?, ?, ?);'''
    #     current = self._connection.cursor()
    #     current.execute(sql, (gr.s_id, gr.a_id, gr.value))
    #     obj = (hw.s_id, hw.a_id, hw.value)
    #     current.execute(sql2, obj)
    #     self._connection.commit()


    def _load_database(self):
        current = self._connection.cursor()
        current.execute("SELECT * FROM grades")
        rows = current.fetchall()
        for row in rows:
            self._grades.append([row[0], row[1], row[2]])

        current.execute("SELECT * FROM homeworks")
        rows = current.fetchall()
        for row in rows:
            self._homework.append([row[0], row[1], row[2]])


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    database = r"C:\\sqlite\\db\\grades_store.db"
    repo = GradeSqlRepo(database)
    repo.create_connection(database)