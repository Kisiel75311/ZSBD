import cx_Oracle

# Initialize the Oracle client
cx_Oracle.init_oracle_client(
    lib_dir=r"C:\Users\szymon.kisiela\Downloads\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11")

# Specify connection details
username = "c##zsbd"
password = "zsbd"
hostname = "localhost"
port = "1521"
sid = "XE"
dsn = cx_Oracle.makedsn(hostname, port, sid)

import subprocess


def export_oracle_schema(username, password, hostname, port, sid, schema, dump_dir, dumpfile, logfile):
    # Ustawienie polecenia expdp
    command = [
        "expdp",
        f"{username}/{password}@{hostname}:{port}/{sid}",
        f"schemas={schema}",
        f"directory={dump_dir}",
        f"dumpfile={dumpfile}",
        f"logfile={logfile}"
    ]

    # Wywołanie polecenia expdp
    result = subprocess.run(command, capture_output=True, text=True)

    # Wydrukowanie wyniku
    if result.returncode == 0:
        print("Eksport zakończony pomyślnie!")
    else:
        print(f"Błąd podczas eksportu: {result.stderr}")


# Ustawienie wartości
hostname = "localhost"
port = "1521"
sid = "XE"
schema = "C##ZSBD"
dump_dir = "/vagrant/"  # Asumując, że wcześniej utworzyłeś tę ścieżkę w bazie Oracle
dumpfile = "zsbd_schema.dmp"
logfile = "zsbd_export.log"

export_oracle_schema(username, password, hostname, port, sid, schema, dump_dir, dumpfile, logfile)
