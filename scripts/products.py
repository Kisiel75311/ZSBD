import cx_Oracle
from faker import Faker
import random
from tqdm import tqdm
import faker_commerce

# Initialize the Oracle client
cx_Oracle.init_oracle_client(
    lib_dir=r"C:\Users\szymon.kisiela\Downloads\instantclient-basic-windows.x64-21.11.0.0.0dbru\instantclient_21_11")

# Initialize the Faker instance
fake = Faker('pl_PL')
fake.add_provider(faker_commerce.Provider)

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


# Seed the Products table
product_insert_query = """
    INSERT INTO Products (id, name, product_weight, product_height, product_width, product_length, specification, contractor_fk)
    VALUES (product_seq.nextval, :name, :product_weight, :product_height, :product_width, :product_length, :specification, :contractor_fk)
"""

generated_names = set()


def get_existing_ids(cursor, table_name, column_name):
    """
    Pobiera istniejące ID z podanej tabeli i kolumny.
    """
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def get_existing_product_names(cursor):
    """
    Pobiera istniejące nazwy produktów z bazy danych.
    """
    query = "SELECT name FROM Products"
    cursor.execute(query)
    return {row[0] for row in cursor.fetchall()}


# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        cursor.execute("SELECT MIN(id), MAX(id) FROM contractors")
        min_id, max_id = cursor.fetchone()

        available_contractors_ids = get_existing_ids(cursor, "contractors", "ID")

        # Pobierz istniejące nazwy produktów i dodaj je do zbioru generated_names
        generated_names.update(get_existing_product_names(cursor))

        for _ in tqdm(range(123543)):  # Inserting 6326 products

            contractor_fk = random.choice(available_contractors_ids)

            name = fake.ecommerce_name()
            color = fake.color_name()
            size = fake.random_element(elements=('Small', 'Medium', 'Large'))
            shape = fake.random_element(elements=('Round', 'Square', 'Oval'))
            full_name = f"{color} {name} ({size}, {shape})"

            # Upewnij się, że generujesz unikalną nazwę produktu
            while full_name in generated_names:
                name = fake.ecommerce_name()
                color = fake.color_name()
                size = fake.random_element(elements=('Small', 'Medium', 'Large'))
                shape = fake.random_element(elements=('Round', 'Square', 'Oval'))
                full_name = f"{color} {name} ({size}, {shape})"

            generated_names.add(full_name)
            insert_data(cursor, "Products", product_insert_query, {
                'name': full_name,
                'product_weight': round(random.uniform(0.01, 1000), 2),
                'product_height': round(random.uniform(0.01, 1000), 2),
                'product_width': round(random.uniform(0.01, 1000), 2),
                'product_length': round(random.uniform(0.01, 1000), 2),
                'specification': fake.text(max_nb_chars=200),
                'contractor_fk': contractor_fk
            })

        connection.commit()  # Commit after all inserts

print("Operation completed!")
