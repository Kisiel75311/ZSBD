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

# Seed the Price_lists table
price_list_insert_query = """
    INSERT INTO Price_lists (id, products_fk, purchase, netto, brutto, sale)
    VALUES (price_list_seq.nextval, :products_fk, :purchase, :netto, :brutto, :sale)
"""


# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        for _ in tqdm(range(100000)):
            insert_data(cursor, "Price_lists", price_list_insert_query, {
                'products_fk': random.randint(220301, 320300),
                'purchase': round(random.uniform(1, 1000), 2),
                'netto': round(random.uniform(1, 1000), 2),
                'brutto': round(random.uniform(1, 1000), 2),
                'sale': round(random.uniform(1, 1000), 2)
            })



    connection.commit()  # Commit after all inserts

print("Operation completed!")