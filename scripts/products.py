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

# Seed the Products table
product_insert_query = """
    INSERT INTO Products (id, name, product_weight, product_height, product_width, product_length, specification, contractor_fk)
    VALUES (product_seq.nextval, :name, :product_weight, :product_height, :product_width, :product_length, :specification, :contractor_fk)
"""

generated_names = set()

# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        for _ in tqdm(range(100000)):  # Inserting 6326 products

            name = fake.ecommerce_name()
            color = fake.color_name()
            size = fake.random_element(elements=('Small', 'Medium', 'Large'))
            shape = fake.random_element(elements=('Round', 'Square', 'Oval'))

            full_name = f"{color} {name} ({size}, {shape})"

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
                'contractor_fk': random.randint(3547, 53546)
            })

        connection.commit()  # Commit after all inserts

print("Operation completed!")
