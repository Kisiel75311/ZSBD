import cx_Oracle
import random
from tqdm import tqdm

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


def insert_data(table_name, insert_query, data):
    try:
        with cx_Oracle.connect(username, password, dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(insert_query, data)
    except cx_Oracle.Error as error:
        print(f"Error occurred when inserting into {table_name}:", error)


# Seed the Product_documents table
product_document_insert_query = """
    INSERT INTO Product_documents (document_fk, product_fk, amount, product_value)
    VALUES (:document_fk, :product_fk, :amount, :product_value)
"""



# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        # Fetch min and max IDs for relevant tables
        cursor.execute("SELECT MIN(id), MAX(id) FROM documents")
        min_doc_id, max_doc_id = cursor.fetchone()

        cursor.execute("SELECT MIN(id), MAX(id) FROM products")
        min_prod_id, max_prod_id = cursor.fetchone()
        for _ in tqdm(range(100000)):
            insert_data("Product_documents", product_document_insert_query, {
                'document_fk': random.randint(min_doc_id, max_doc_id+1),
                'product_fk': random.randint(min_prod_id, max_prod_id+1),
                'amount': round(random.uniform(0.01, 1000), 2),
                'product_value': round(random.uniform(0.01, 1000), 2)
            })
        connection.commit()

print("Operation completed!")
