import cx_Oracle
from faker import Faker
import random
from tqdm import tqdm
import numpy as np

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


def generate_num_companies_per_warehouse(n, mean=20.5, std_dev=10, min_value=1, max_value=40):
    """
    Generuje listę wartości z rozkładu normalnego w zakresie od min_value do max_value.
    """
    values = np.random.normal(mean, std_dev, n)
    clipped_values = np.clip(values, min_value, max_value)
    return np.round(clipped_values).astype(int).tolist()  # Zaokrąglanie wartości do najbliższej liczby całkowitej

def assign_companies_to_warehouses(cursor):
    cursor.execute("SELECT id FROM Warehouses")
    warehouse_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM companies")
    all_companies = [row[0] for row in cursor.fetchall()]

    num_companies_per_warehouse = generate_num_companies_per_warehouse(len(warehouse_ids))

    for warehouse_id, num_companies in tqdm(zip(warehouse_ids, num_companies_per_warehouse), total=len(warehouse_ids)):

        assigned_companies = random.choices(all_companies, k=num_companies)  # Używamy choices zamiast sample, by pozwolić na powtórzenia

        # Dodajemy każdą przypisaną firmę do tabeli Warehouse_Company
        for company_id in assigned_companies:
            cursor.execute(
                "INSERT INTO Warehouse_Company (warehouse_id, company_id) VALUES (:warehouse_id, :company_id)",
                {'warehouse_id': warehouse_id, 'company_id': company_id}
            )


# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        # Call the assign function
        assign_companies_to_warehouses(cursor)

        # Commit the updates
        connection.commit()
print("Operation completed!")