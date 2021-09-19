import sqlite3
from sqlite3 import Error
from domain.Student import Student
from repository.student_repo import StudentRepo


class StudentSqlRepo(StudentRepo):
    def __init__(self, database_name):
        super().__init__()
        self._database = database_name
        self._connection = self.create_connection(database_name)
        # self.main()
        self._load_database()

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
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS students (
                                            id text PRIMARY KEY,
                                            name text NOT NULL,
                                            _group text NOT NULL
                                    ); """

        # create tables
        if self._connection is not None:
            # create projects table
            self.create_table(sql_create_projects_table)
        else:
            print("Error! cannot create the database connection.")

    def store(self, obj):
        """
        :param obj: type: class <Student>
        :return:
        """
        super().add(obj)
        obj = (obj.id, obj.name, obj.group)
        sql = '''INSERT OR REPLACE INTO students (id, name, _group) VALUES (?, ?, ?);'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    def update_student(self, old_id, id, name, group):
        """
        update
        :return:
        """
        super().update(old_id, id, name, group)
        obj = (id, name, group, old_id)
        sql = ''' UPDATE students
                  SET id = ? ,
                      name = ? ,
                      _group = ?
                  WHERE id = ?'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    def delete(self, obj_id):
        super().remove(obj_id)
        sql = 'DELETE FROM students WHERE id = ?'
        current = self._connection.cursor()
        current.execute(sql, (obj_id,))
        self._connection.commit()

    def _load_database(self):
        current = self._connection.cursor()
        current.execute("SELECT * FROM students")
        rows = current.fetchall()
        for row in rows:
            self._students.append(Student(row[0], row[1], row[2]))


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
    database = r"C:\\sqlite\\db\\store.db"
    #create_connection(database)