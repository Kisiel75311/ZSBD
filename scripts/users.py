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

generated_emails = set()
generated_phone_numbers = set()
generated_logins = set()


def insert_data(cursor, table_name, insert_query, data):
    try:
        cursor.execute(insert_query, data)  # Inserting the data once per call
    except cx_Oracle.Error as error:
        print(f"Error occurred when inserting into {table_name}:", error)


# Define the query for the Users table and the queries for fetching min and max ids
user_insert_query = """
    INSERT INTO Users (id, name, surname, role_fk, company_fk, warehouse_fk, email, phone_number, login, password, deleted)
    VALUES (user_seq.nextval, :name, :surname, :role_fk, :company_fk, :warehouse_fk, :email, :phone_number, :login, :password, :deleted)
"""

role_query = "SELECT MIN(id), MAX(id) FROM Roles"
company_query = "SELECT MIN(id), MAX(id) FROM Companies"
warehouse_query = "SELECT MIN(id), MAX(id) FROM Warehouses"

# Connect to the database, fetch min-max values and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        # Fetch the min and max values
        cursor.execute(role_query)
        role_min_id, role_max_id = cursor.fetchone()

        cursor.execute(company_query)
        company_min_id, company_max_id = cursor.fetchone()

        cursor.execute(warehouse_query)
        warehouse_min_id, warehouse_max_id = cursor.fetchone()

        for _ in tqdm(range(50000)):
            email = fake.email()
            while email in generated_emails:
                email = fake.email()
            generated_emails.add(email)

            phone_number = ''.join(filter(str.isdigit, fake.phone_number()))
            while phone_number in generated_phone_numbers:
                phone_number = ''.join(filter(str.isdigit, fake.phone_number()))
            generated_phone_numbers.add(phone_number)

            login = fake.user_name()[:15]
            while login in generated_logins or len(login) > 15:
                login = fake.user_name()[:15]
            generated_logins.add(login)

            insert_data(cursor, "Users", user_insert_query, {
                'name': fake.first_name(),
                'surname': fake.last_name(),
                'role_fk': random.randint(role_min_id+1, role_max_id-1),
                'company_fk': random.randint(company_min_id, company_max_id),
                'warehouse_fk': random.randint(warehouse_min_id, warehouse_max_id),
                'email': email,
                'phone_number': phone_number,
                'login': login,
                'password': fake.password(),
                'deleted': random.randint(0, 1)
            })

        connection.commit()  # Commit after all inserts

print("Operation completed!")
