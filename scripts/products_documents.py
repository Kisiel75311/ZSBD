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
        cursor.execute(insert_query, data)
    except cx_Oracle.Error as error:
        print(f"Error occurred when inserting into {table_name}:", error)


# Seed the Product_documents table
product_document_insert_query = """
    INSERT INTO Product_documents (document_fk, product_fk, amount, product_value)
    VALUES (:document_fk, :product_fk, :amount, :product_value)
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

        # Pobierz dostępne ID z tabeli Documents (załóżmy, że kolumna z ID nazywa się 'document_id')
        available_document_ids = get_existing_ids(cursor, "documents", "ID")
        available_product_ids = get_existing_ids(cursor, "products",
                                                 "ID")  # zakładając, że istnieje taka tabela

        for _ in tqdm(range(100000)):
            document_fk = random.choice(available_document_ids)
            product_fk = random.choice(available_product_ids)

            insert_data(cursor, "Product_documents", product_document_insert_query, {
                'document_fk': document_fk,
                'product_fk': product_fk,
                'amount': round(random.uniform(0.01, 1000), 2),
                'product_value': round(random.uniform(0.01, 1000), 2)
            })

        connection.commit()  # Commit after all inserts

print("Operation completed!")
