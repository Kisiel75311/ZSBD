import os
import shutil
import time
import cx_Oracle
from tqdm import tqdm


# import resaults_parser


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

    def __init__(self, username, password, dsn, operation_types):
        self.username = username
        self.password = password
        self.dsn = dsn
        self.operation_types = operation_types if isinstance(operation_types, list) else [operation_types]
        self._clearResultsDirectory()
        os.makedirs(self._DB_RESULTS_DIR, exist_ok=True)

    def _clearResultsDirectory(self):
        # Clear only the results of the types that will be run
        for operation_type in self.operation_types:
            result_file = os.path.join(self._DB_RESULTS_DIR, f'{operation_type}_result.txt')
            if os.path.exists(result_file):
                os.remove(result_file)

    def _executeSQLStatements(self, cursor, sql_statements):
        total_elapsed_time = 0  # Suma czasów wykonania wszystkich instrukcji
        success = True
        for statement in sql_statements:
            statement = statement.strip()
            if statement:
                try:
                    start_time = time.time()  # Start time for this statement
                    cursor.execute(statement)
                    end_time = time.time()  # End time for this statement
                    elapsed_time = (end_time - start_time) * 1000
                    total_elapsed_time += elapsed_time  # Dodanie czasu wykonania do sumy
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    print(f"Error: {error.message}, SQL statement: {statement}")
                    success = False
                    break
        return success, total_elapsed_time

    def _runSQLScripts(self, cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache,
                       operation_type):
        with cx_Oracle.connect(sys_username, sys_password, sys_dsn) as sys_con:
            sys_cursor = sys_con.cursor()
            for file in tqdm(sql_files, desc="Running SQL Scripts"):
                tqdm.write(f"Processing SQL Script: {file}")
                with open(os.path.join(self._SQL_SCRIPTS_BASE_PATH, operation_type, file), 'r') as sql_file:
                    sql_script = sql_file.read()
                    sql_statements = sql_script.split(';')

                for _ in tqdm(range(execution_count), desc="Executions"):
                    cursor.execute("SAVEPOINT before_test")
                    if clear_cache:
                        sys_cursor.execute("ALTER SYSTEM FLUSH BUFFER_CACHE")
                        sys_cursor.execute("ALTER SYSTEM FLUSH SHARED_POOL")
                    success, elapsed_time = self._executeSQLStatements(cursor, sql_statements)  # Corrected line
                    cursor.execute("ROLLBACK TO SAVEPOINT before_test")
                    if not success:
                        break

                    self._writeResultsToFile(operation_type, file, elapsed_time, clear_cache)
                if not success:
                    continue

    def _writeResultsToFile(self, operation_type, file, elapsed_time, clear_cache):
        cache_status = 'with_cache_clear' if clear_cache else 'without_cache_clear'
        result_file_name = f"{operation_type}_result_{cache_status}.txt"
        with open(os.path.join(self._DB_RESULTS_DIR, result_file_name), 'a') as f:
            f.write(f"{file}, {elapsed_time:.2f}ms\n")

    def run(self, sys_username, sys_password, sys_dsn, clear_cache, execution_count=1):
        for operation_type in self.operation_types:
            sql_files = [f for f in os.listdir(os.path.join(self._SQL_SCRIPTS_BASE_PATH, operation_type)) if
                         f.endswith('.sql')]
            with cx_Oracle.connect(self.username, self.password, self.dsn) as connection:
                cursor = connection.cursor()
                self._runSQLScripts(cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn,
                                    clear_cache, operation_type)
                connection.commit()

        print("Load test completed and results are recorded in 'results/'")


# Configuration for the Oracle client
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

# operation_types = ['select', 'update', 'insert', 'delete']  # Adjust as needed
operation_types = ['select']  # Adjust as needed

# Usage of OracleClientManager and Database classes
with OracleClientManager(lib_dir):
    db = Database(zsbd_username, zsbd_password, dsn, operation_types)
    db.run(sys_username, sys_password, dsn, clear_cache, execution_count)

# # Parse the results
# parser = ResultsParser()
# parser.end_load_tests()
