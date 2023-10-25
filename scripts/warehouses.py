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


# Seed the Warehouses table
warehouse_insert_query = """
    INSERT INTO Warehouses (id, name, address, companies_fk)
    VALUES (warehouse_seq.nextval, :name, :address, :companies_fk)
"""



# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        cursor.execute("SELECT MIN(id), MAX(id) FROM companies")
        min_id, max_id = cursor.fetchone()
        for _ in tqdm(range(10000)):
            # Get min and max values from companies table
            insert_data(cursor, "Warehouses", warehouse_insert_query, {
                'name': fake.company_suffix(),
                'address': fake.address(),
                'companies_fk': random.randint(min_id+1, max_id-1)  # 50 tys? nie wiem
            })
        connection.commit()  # Commit after all inserts

print("Operation completed!")


# import numpy as np
#
# # ...
#
# # Connect to the database and insert data
# with cx_Oracle.connect(username, password, dsn) as connection:
#     with connection.cursor() as cursor:
#         print("Connected successfully!")
#
#         # Get min and max values from companies table
#         cursor.execute("SELECT MIN(id), MAX(id) FROM companies")
#         min_id, max_id = cursor.fetchone()
#
#         for _ in tqdm(range(50000)):
#             # Generate a list of company ids using normal distribution
#             company_ids = np.random.normal(loc=(min_id+max_id)/2, scale=(max_id-min_id)/6, size=30).astype(int)
#
#             # Ensure the generated company ids are within the valid range
#             company_ids = [max(min_id, min(max_id, company_id)) for company_id in company_ids]
#
#             for company_id in company_ids:
#                 insert_data(cursor, "Warehouses", warehouse_insert_query, {
#                     'name': fake.company_suffix(),
#                     'address': fake.address(),
#                     'companies_fk': company_id
#                 })
#         connection.commit()  # Commit after all inserts
#
# print("Operation completed!")
