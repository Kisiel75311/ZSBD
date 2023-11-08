import cx_Oracle
import time
import os
from tqdm import tqdm


class OracleClientManager:
    def __init__(self, lib_dir):
        self.lib_dir = lib_dir

    def __enter__(self):
        cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Database:
    _SQL_SCRIPTS_BASE_PATH = 'load_test_sql_scripts'
    _DB_RESULTS_DIR = 'results'


    def __init__(self, username, password, dsn, operation_type):
        self.username = username
        self.password = password
        self.dsn = dsn
        self.operation_type = operation_type
        self._sql_scripts_path = os.path.join(self._SQL_SCRIPTS_BASE_PATH, operation_type)
        self._db_results_file = f'{operation_type}_result.txt'
        os.makedirs(self._DB_RESULTS_DIR, exist_ok=True)

    def _runSQLScripts(self, cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache):
        with cx_Oracle.connect(sys_username, sys_password, sys_dsn) as sys_con:
            sys_cursor = sys_con.cursor()
            for file in tqdm(sql_files, desc="Running SQL Scripts"):
                with open(os.path.join(self._sql_scripts_path, file), 'r') as sql_file:
                    sql_script = sql_file.read()
                    sql_statements = sql_script.split(';')

                for _ in tqdm(range(execution_count), desc="Executions"):
                    if clear_cache:
                        print("Flushing buffer cache and shared pool")
                        sys_cursor.execute("ALTER SYSTEM FLUSH BUFFER_CACHE")
                        sys_cursor.execute("ALTER SYSTEM FLUSH SHARED_POOL")

                    # Set a savepoint before executing the SQL statements
                    cursor.execute("SAVEPOINT before_test")

                    _, elapsed_time, _ = self._executeSQLStatements(cursor, sql_statements)

                    # Rollback to the savepoint after executing the SQL statements
                    cursor.execute("ROLLBACK TO SAVEPOINT before_test")

                    self._writeResultsToFile(file, elapsed_time)

    def _executeSQLStatements(self, cursor, sql_statements):
        start_time = time.time()
        for statement in tqdm(sql_statements, desc="Executing Statements"):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    print(f"Error: {error.message}, SQL statement: {statement}")
                    continue
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        return start_time, elapsed_time, end_time

    def _writeResultsToFile(self, file, elapsed_time):
        with open(os.path.join(self._DB_RESULTS_DIR, self._db_results_file), 'a') as f:
            f.write(f"{file}, {elapsed_time:.2f}ms\n")

    def run(self, sys_username, sys_password, sys_dsn, clear_cache, execution_count=1):
        with cx_Oracle.connect(self.username, self.password, self.dsn) as connection:
            cursor = connection.cursor()
            sql_files = [f for f in os.listdir(self._sql_scripts_path) if f.endswith('.sql')]
            self._runSQLScripts(cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache)
            connection.commit()

        print("Load test completed and results are recorded in 'results/exec_time.txt'.")


lib_dir = r"C:\Users\szymon.kisiela\Downloads\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11"
zsbd_username = "c##zsbd"
zsbd_password = "zsbd"
sys_username = "system"
sys_password = "SysPassword1"
hostname = "localhost"
port = "1521"
sid = "XE"
dsn = cx_Oracle.makedsn(hostname, port, sid)
execution_count = 10
clear_cache = True

operation_type = 'update'  # 'select' or 'insert', 'update', 'delete', 'all'

with OracleClientManager(lib_dir):
    db = Database(zsbd_username, zsbd_password, dsn, operation_type)
    db.run(sys_username, sys_password, dsn, clear_cache, execution_count)

