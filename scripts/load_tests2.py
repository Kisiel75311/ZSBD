import os
import shutil
import time
import cx_Oracle
from tqdm import tqdm
import glob


# import resaults_parser


class OracleClientManager:
    def __init__(self, lib_dir):
        self.lib_dir = lib_dir

    def __enter__(self):
        cx_Oracle.init_oracle_client(lib_dir=self.lib_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Database:
    _SQL_SCRIPTS_BASE_PATH = 'load_test_sql_scripts/final_scripts'
    _DB_RESULTS_DIR = 'results'

    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
        # self.operation_types = operation_types if isinstance(operation_types, list) else [operation_types]
        self._clearResultsDirectory()
        os.makedirs(self._DB_RESULTS_DIR, exist_ok=True)

    def _clearResultsDirectory(self):
        # Clear only the results of the types that will be run
        result_files = glob.glob(os.path.join(self._DB_RESULTS_DIR, 'results_*.txt'))  # Match both result file names
        for result_file in result_files:
            if os.path.exists(result_file):
                os.remove(result_file)

    def _executeSQLStatements(self, cursor, sql_statements, iteration, file):
        total_elapsed_time = 0  # Suma czasów wykonania wszystkich instrukcji
        success = True
        for statement in sql_statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(f"EXPLAIN PLAN FOR {statement}")  # Explain the plan for the statement
                    start_time = time.time()  # Start time for this statement
                    cursor.execute(statement)
                    end_time = time.time()  # End time for this statement
                    elapsed_time = (end_time - start_time) * 1000
                    total_elapsed_time += elapsed_time  # Dodanie czasu wykonania do sumy

                    # Get the cost of the last statement
                    cursor.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY)")
                    rows = cursor.fetchall()
                    self._writeExplainPlanToFile(iteration, file, rows)  # Write the explain plan to a file

                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    print(f"Error: {error.message}, SQL statement: {statement}")
                    success = False
                    break
        return success, total_elapsed_time

    def _writeExplainPlanToFile(self, iteration, file, rows):
        explain_plan_dir = 'explain_plans'
        os.makedirs(explain_plan_dir, exist_ok=True)
        script_name = os.path.basename(file)  # Get the script name from the file path
        explain_plan_file_name = f"{iteration}_{script_name}.txt"
        with open(os.path.join(explain_plan_dir, explain_plan_file_name), 'w') as f:
            for row in rows:
                f.write(str(row) + "\n")

    def _runSQLScripts(self, cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache):
        with cx_Oracle.connect(sys_username, sys_password, sys_dsn) as sys_con:
            sys_cursor = sys_con.cursor()
            for i in tqdm(range(execution_count), desc="Executions"):
                cursor.execute("SAVEPOINT before_test")
                for file in tqdm(sql_files, desc="Running SQL Scripts"):
                    tqdm.write(f"Processing SQL Script: {file}")
                    with open(file, 'r') as sql_file:  # Do not add the base path again
                        sql_script = sql_file.read()
                        sql_statements = sql_script.split(';')

                    if clear_cache:
                        sys_cursor.execute("ALTER SYSTEM FLUSH BUFFER_CACHE")
                        sys_cursor.execute("ALTER SYSTEM FLUSH SHARED_POOL")
                    success, elapsed_time = self._executeSQLStatements(cursor, sql_statements, i + 1,
                                                                       file)  # Pass iteration and file
                    if not success:
                        break

                    self._writeResultsToFile(i + 1, file, elapsed_time, clear_cache)  # Pass iteration number
                cursor.execute("ROLLBACK TO SAVEPOINT before_test")



    def _writeResultsToFile(self, iteration, file, elapsed_time, clear_cache):
        cache_status = 'with_cache_clear' if clear_cache else 'without_cache_clear'
        result_file_name = f'results_{cache_status}.txt'  # File name includes cache status
        with open(os.path.join(self._DB_RESULTS_DIR, result_file_name), 'a') as f:
            script_name = os.path.basename(file)  # Get the script name from the file path
            f.write(f"{iteration}, {script_name}, {elapsed_time:.2f}ms\n")  # Include iteration number, script name and elapsed time in the results

    def run(self, sys_username, sys_password, sys_dsn, clear_cache, execution_count=1):
        sql_files = glob.glob(os.path.join(self._SQL_SCRIPTS_BASE_PATH, '*.sql'))  # Use glob.glob() here
        with cx_Oracle.connect(self.username, self.password, self.dsn) as connection:
            cursor = connection.cursor()
            # Execute the initialization query
            cursor.execute("SELECT * FROM users FETCH FIRST 10 ROWS ONLY")
            self._runSQLScripts(cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache)
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

# operation_types = ['de', 'update', 'insert', 'delete']  # Adjust as needed
# operation_types = ['select']  # Adjust as needed

# Usage of OracleClientManager and Database classes
with OracleClientManager(lib_dir):
    db = Database(zsbd_username, zsbd_password, dsn)
    db.run(sys_username, sys_password, dsn, clear_cache, execution_count)

# # Parse the results
# parser = ResultsParser()
# parser.end_load_tests()
