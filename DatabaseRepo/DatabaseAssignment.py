import sqlite3
from sqlite3 import Error
from domain.Assignment import Assignment
from repository.assignment_repo import AssignmentRepo


class AssignmentSqlRepo(AssignmentRepo):
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
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS assignments (
                                            id text PRIMARY KEY,
                                            description text NOT NULL,
                                            day_deadline text NOT NULL,
                                            month_deadline text NOT NULL
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
        obj = (obj.id, obj.description, obj.deadline[0], obj.deadline[1])
        sql = '''INSERT OR REPLACE INTO assignments 
                (id, description, day_deadline, month_deadline) VALUES (?, ?, ?, ?);'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    def update_assignment(self, id_old, id_new, descr, day, month):
        """
        update
        :return:
        """
        super().update(id_old, id_new, descr, day, month)
        obj = (id_new, descr, day, month, id_old)
        sql = ''' UPDATE assignments
                  SET id = ? ,
                      description = ? ,
                      day_deadline = ? ,
                      month_deadline = ? 
                  WHERE id = ?'''
        current = self._connection.cursor()
        current.execute(sql, obj)
        self._connection.commit()

    def delete(self, obj_id):
        super().remove(obj_id)
        sql = 'DELETE FROM assignments WHERE id = ?'
        current = self._connection.cursor()
        current.execute(sql, (obj_id,))
        self._connection.commit()

    def _load_database(self):
        current = self._connection.cursor()
        current.execute("SELECT * FROM assignments")
        rows = current.fetchall()
        for row in rows:
            self._assignments.append(Assignment(row[0], row[1], [row[2], row[3]]))


if __name__ == '__main__':
    database = r"C:\\sqlite\\db\\assignment_store.db"
    repo = AssignmentSqlRepo(database)
    #create_connection(database)