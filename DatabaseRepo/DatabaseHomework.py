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
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS homeworks (
                                            s_id text PRIMARY KEY,
                                            a_id text NOT NULL,
                                            grade text NOT NULL
                                    ); """

        # create tables
        if self._connection is not None:
            self.create_table(sql_create_projects_table)
        else:
            print("Error! cannot create the database connection.")
