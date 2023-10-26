import cx_Oracle
from faker import Faker
import random
from tqdm import tqdm

# Initialize the Oracle client
cx_Oracle.init_oracle_client(
    lib_dir=r"C:\Users\szymon.kisiela\Downloads\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11")

# Initialize the Faker instance
fake = Faker('pl_PL')

# Specify connection details
username = "c##admin"
password = "admin"
hostname = "localhost"
port = "1521"
sid = "XE"
dsn = cx_Oracle.makedsn(hostname, port, sid)


def insert_data(cursor, table_name, insert_query, data):
    try:
        cursor.execute(insert_query, data)  # Inserting the data once per call
    except cx_Oracle.Error as error:
        print(f"Error occurred when inserting into {table_name}:", error)


# Seed the Warehouses table
warehouse_insert_query = """
    INSERT INTO Warehouses (id, name, address, companies_fk)
    VALUES (warehouse_seq.nextval, :name, :address, :companies_fk)
"""

def get_existing_ids(cursor, table_name, column_name):
    """
    Pobiera istniejące ID z podanej tabeli i kolumny.
    """
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        companies_ids = get_existing_ids(cursor, "Companies", "id")

        for _ in tqdm(range(50000)):
            company_pk = random.choice(companies_ids)
            insert_data(cursor, "Warehouses", warehouse_insert_query, {
                'name': fake.company_suffix(),
                'address': fake.address(),
                'companies_fk': company_pk  # 50 tys? nie wiem
            })
        connection.commit()  # Commit after all inserts

print("Operation completed!")
