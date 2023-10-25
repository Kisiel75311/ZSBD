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

# Seed the Companies table
company_insert_query = """
    INSERT INTO Companies (id, name, address, business_number, regon, krs, account_number)
    VALUES (company_seq.nextval, :name, :address, :business_number, :regon, :krs, :account_number)
"""


def generate_valid_company_name(fake, max_length=30):
    while True:
        company_name = fake.company()
        if len(company_name) <= max_length:
            return company_name

# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        for _ in tqdm(range(50000)):
            insert_data(cursor, "Companies", company_insert_query, {
                'name': fake.company()[:25],  # Truncate to 30 characters
                'address': fake.address(),
                'business_number': fake.random_int(min=1000000000, max=9999999999),
                'regon': fake.random_int(min=100000000, max=999999999),
                'krs': fake.random_int(min=100000000, max=999999999),
                'account_number': fake.iban()
            })
        connection.commit()  # Commit after all inserts

print("Operation completed!")
