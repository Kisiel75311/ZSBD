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


def insert_data(cursor, table_name, insert_query, data):
    try:
        cursor.execute(insert_query, data)  # Inserting the data once per call
    except cx_Oracle.Error as error:
        print(f"Error occurred when inserting into {table_name}:", error)

roles_to_seed = [
    "Accountant",  # 3% - Firma
    "ZSBD Specialist",  # 1% - Może być w obu (Magazyn/Firma), ale zakładam tutaj Firma
    "Customer",  # 5% - Firma
    "Sales Representative",  # 8% - Firma
    "Warehouse Operator",  # 25% - Magazyn
    "Warehouse Manager",  # 2% - Magazyn
    "Technical Support",  # 4% - Firma
    "Stock Coordinator",  # 4% - Magazyn
    "Forklift Operator",  # 10% - Magazyn
    "Warehouse SafetySpec",  # 2% - Magazyn
    "Warehouse Analyst",  # 3% - Magazyn
    "Customer ServiceSpec",  # 10% - Firma
    "Sales Director",  # 1% - Firma
    "Financial Analyst",  # 2% - Firma
    "Marketing Specialist"  # 20% - Firma
]


# Seed the Roles table
role_insert_query = """
    INSERT INTO Roles (id, name)
    VALUES (role_seq.nextval, :name)
"""

# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        for role_name in roles_to_seed:
            insert_data(cursor, "Roles", role_insert_query, {'name': role_name})

        connection.commit()  # Commit after all inserts

print("Operation completed!")
