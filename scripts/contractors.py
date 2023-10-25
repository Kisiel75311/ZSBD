import cx_Oracle
from faker import Faker
from tqdm import tqdm
import random

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


# Seed the Contractors table
contractor_insert_query = """
    INSERT INTO Contractors (id, address, country, name, business_number, account_number)
    VALUES (contractor_seq.nextval, :address, :country, :name, :business_number, :account_number)
"""

# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        for _ in tqdm(range(50000)):  # Inserting 50,000 contractors
            insert_data(cursor, "Contractors", contractor_insert_query, {
                'address': fake.address(),
                'country': fake.country_code(representation="alpha-2"),
                'name': fake.company(),
                'business_number': fake.random_int(min=1000000000, max=9999999999),
                'account_number': fake.iban()
            })

        connection.commit()  # Commit after all inserts

print("Operation completed!")
