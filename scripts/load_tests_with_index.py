import os
import time
import cx_Oracle
from tqdm import tqdm
import glob


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
    _INDEX_SCRIPTS_PATH = 'load_test_sql_scripts/indexs'

    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
        self._clearResultsDirectory()
        os.makedirs(self._DB_RESULTS_DIR, exist_ok=True)

    def _addIndexes(self, cursor, index_type):
        index_files = glob.glob(os.path.join(self._INDEX_SCRIPTS_PATH, index_type, '*.sql'))
        for file_path in index_files:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith("--"):
                        print(f"Executing SQL: {line}")  # Dodanie logowania
                        try:
                            cursor.execute(line)
                        except cx_Oracle.DatabaseError as e:
                            error, = e.args
                            print(f"Error: {error.message}, SQL statement: {line}")

    def _deleteIndexes(self, cursor, index_type):
        # Wybierz odpowiedni plik w zależności od typu indeksu
        if index_type == 'normal':
            index_file = os.path.join(self._INDEX_SCRIPTS_PATH, 'dropIndex.sql')
        elif index_type == 'bitmap':
            index_file = os.path.join(self._INDEX_SCRIPTS_PATH, 'dropbitmapindex.sql')
        else:
            raise ValueError("Nieznany typ indeksu")

        # Wykonaj polecenia SQL z wybranego pliku
        with open(index_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("--"):
                    print(f"Executing SQL: {line}")  # Dodanie logowania
                    try:  # Ignoruj puste linie i komentarze
                        cursor.execute(line)
                    except cx_Oracle.DatabaseError as e:
                        error, = e.args
                        print(f"Error: {error.message}, SQL statement: {line}")

    def _clearResultsDirectory(self):
        result_files = glob.glob(os.path.join(self._DB_RESULTS_DIR, 'results_*.txt'))
        for result_file in result_files:
            if os.path.exists(result_file):
                os.remove(result_file)

    def _executeSQLStatements(self, cursor, sql_statements, iteration, file, index_type):
        total_elapsed_time = 0
        success = True
        for statement in sql_statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute("SELECT * FROM users FETCH FIRST 10 ROWS ONLY")
                    cursor.execute(f"EXPLAIN PLAN FOR {statement}")  # Explain the plan for the statement
                    start_time = time.time()  # Start time for this statement
                    cursor.execute(statement)
                    end_time = time.time()  # End time for this statement
                    elapsed_time = (end_time - start_time) * 1000
                    total_elapsed_time += elapsed_time  # Dodanie czasu wykonania do sumy

                    # Get the cost of the last statement
                    cursor.execute("SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY)")
                    rows = cursor.fetchall()
                    self._writeExplainPlanToFile(file, rows, index_type)  # Write the explain plan to a file

                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    print(f"Error: {error.message}, SQL statement: {statement}")
                    success = False
                    break
        return success, total_elapsed_time

    def _writeExplainPlanToFile(self, file, rows, index_type):
        explain_plan_dir = 'explain_plans'
        os.makedirs(explain_plan_dir, exist_ok=True)
        script_name = os.path.basename(file)
        explain_plan_file_name = f"{index_type}_{script_name}.txt"
        with open(os.path.join(explain_plan_dir, explain_plan_file_name), 'w') as f:
            for row in rows:
                f.write(str(row) + "\n")

    def _runSQLScripts(self, cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache,
                       index_type):
        with cx_Oracle.connect(sys_username, sys_password, sys_dsn) as sys_con:
            sys_cursor = sys_con.cursor()
            for i in tqdm(range(execution_count), desc="Executions"):
                cursor.execute("SAVEPOINT before_test")
                for file_path in tqdm(sql_files, desc="Running SQL Scripts"):
                    file_name = os.path.basename(file_path)  # Pobierz nazwę pliku
                    tqdm.write(f"Processing SQL Script: {file_name}")
                    with open(file_path, 'r') as sql_file:
                        sql_script = sql_file.read()
                        sql_statements = sql_script.split(';')

                    if clear_cache:
                        sys_cursor.execute("ALTER SYSTEM FLUSH BUFFER_CACHE")
                        sys_cursor.execute("ALTER SYSTEM FLUSH SHARED_POOL")

                    success, elapsed_time = self._executeSQLStatements(cursor, sql_statements, i + 1, file_name,
                                                                       index_type)
                    if not success:
                        break

                    self._writeResultsToFile(i + 1, file_name, elapsed_time, clear_cache, index_type)

                cursor.execute("ROLLBACK TO SAVEPOINT before_test")

    def _writeResultsToFile(self, iteration, file, elapsed_time, clear_cache, index_type):
        cache_status = 'with_cache_clear' if clear_cache else 'without_cache_clear'
        result_file_name = f'results_{index_type}_{cache_status}.txt'
        with open(os.path.join(self._DB_RESULTS_DIR, result_file_name), 'a') as f:
            script_name = os.path.basename(file)
            f.write(f"{iteration}, {script_name}, {elapsed_time:.2f}ms\n")

    def run(self, sys_username, sys_password, sys_dsn, clear_cache, execution_count=1, index_type='normal'):
        sql_files = glob.glob(os.path.join(self._SQL_SCRIPTS_BASE_PATH, '*.sql'))
        with cx_Oracle.connect(self.username, self.password, self.dsn) as connection:
            cursor = connection.cursor()
            if index_type != 'none':
                self._addIndexes(cursor, index_type)
            self._runSQLScripts(cursor, sql_files, execution_count, sys_username, sys_password, sys_dsn, clear_cache,
                                index_type)
            if index_type != 'none':
                self._deleteIndexes(cursor, index_type)

            connection.commit()
        print(f"Load test completed for {index_type} index and results are recorded in 'results/'")


# Oracle client configuration
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
index_type = ('none', 'normal', 'bitmap')

# Run the load tests
with OracleClientManager(lib_dir):
    db = Database(zsbd_username, zsbd_password, dsn)
    for index_type in index_type:
        db.run(sys_username, sys_password, dsn, clear_cache, execution_count, index_type)

# Optionally run for bitmap indexes
# with OracleClientManager(lib_dir):
#     db.run(sys_username, sys_password, dsn, clear_cache, execution_count, index_type='bitmap')

# # Parse the results
# parser = ResultsParser()
# parser.end_load_tests()
