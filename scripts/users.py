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
username = "c##admin"
password = "admin"
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


# Define the query for the Users table
user_insert_query = """
    INSERT INTO Users (id, name, surname, role_fk, company_fk, warehouse_fk, email, phone_number, login, password, deleted)
    VALUES (user_seq.nextval, :name, :surname, :role_fk, :company_fk, :warehouse_fk, :email, :phone_number, :login, :password, :deleted)
"""

# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

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
                'role_fk': random.randint(1, 7),
                'company_fk': random.randint(1, 50000),
                'warehouse_fk': random.randint(1, 50000),
                'email': email,
                'phone_number': phone_number,
                'login': login,
                'password': fake.password(),
                'deleted': random.randint(0, 1)
            })

        connection.commit()  # Commit after all inserts

print("Operation completed!")

exit(0)

# Roles to seed
roles_to_seed = ["accountant", "admin", "customer", "sales representative", "warehouseman", "warehouse manager", "tech support"]

# Seed the Roles table
role_insert_query = """
    INSERT INTO Roles (id, name)
    VALUES (role_seq.nextval, :name)
"""
for role_name in roles_to_seed:
    cursor.execute(role_insert_query, {'name': role_name})

# Seed the Companies table
company_insert_query = """
    INSERT INTO Companies (id, name, address, business_number, regon, krs, account_number)
    VALUES (company_seq.nextval, :name, :address, :business_number, :regon, :krs, :account_number)
"""
for _ in range(50000):
    insert_data("Companies", company_insert_query, {
        'name': fake.company(),
        'address': fake.address(),
        'business_number': fake.random_int(min=1000000000, max=9999999999),
        'regon': fake.random_int(min=100000000, max=999999999),
        'krs': fake.random_int(min=100000000, max=999999999),
        'account_number': fake.iban()
    })

# Seed the Warehouses table
warehouse_insert_query = """
    INSERT INTO Warehouses (id, name, address, companies_fk)
    VALUES (warehouse_seq.nextval, :name, :address, :companies_fk)
"""
for _ in range(50000):
    insert_data("Warehouses", warehouse_insert_query, {
        'name': fake.company_suffix(),
        'address': fake.address(),
        'companies_fk': random.randint(1, 50000) #50 tys? nie wiem
    })

# Seed the Products table
product_insert_query = """
    INSERT INTO Products (id, name, product_weight, product_height, product_width, product_length, specification, contractor_fk)
    VALUES (product_seq.nextval, :name, :product_weight, :product_height, :product_width, :product_length, :specification, :contractor_fk)
"""
for _ in range(100000):
    insert_data("Products", product_insert_query, {
        'name': fake.catch_phrase(),
        'product_weight': round(random.uniform(0.01, 1000), 2),
        'product_height': round(random.uniform(0.01, 1000), 2),
        'product_width': round(random.uniform(0.01, 1000), 2),
        'product_length': round(random.uniform(0.01, 1000), 2),
        'specification': fake.text(max_nb_chars=200),
        'contractor_fk': random.randint(1, 50000) 
    })

# Seed the Price_lists table
price_list_insert_query = """
    INSERT INTO Price_lists (id, products_fk, purchase, netto, brutto, sale)
    VALUES (price_list_seq.nextval, :products_fk, :purchase, :netto, :brutto, :sale)
"""
for _ in range(100000):
    insert_data("Price_lists", price_list_insert_query, {
        'products_fk': random.randint(1, 100000),
        'purchase': round(random.uniform(1, 1000), 2),
        'netto': round(random.uniform(1, 1000), 2),
        'brutto': round(random.uniform(1, 1000), 2),
        'sale': round(random.uniform(1, 1000), 2)
    })

# Seed the Documents table
document_insert_query = """
    INSERT INTO Documents (id, document_number, document_type_fk, document_date, contractor_fk, client_fk, 
    created_by_fk, created, modified_by_fk, last_modification, deleted, deleted_by_fk, document_value)
    VALUES (document_seq.nextval, :document_number, :document_type_fk, :document_date, :contractor_fk, :client_fk, 
    :created_by_fk, TO_TIMESTAMP(:created, 'YYYY-MM-DD HH24:MI:SS.FF'), :modified_by_fk, 
    TO_TIMESTAMP(:last_modification, 'YYYY-MM-DD HH24:MI:SS.FF'), :deleted, :deleted_by_fk, :document_value)
"""
for _ in range(100000):
    insert_data("Documents", document_insert_query, {
        'document_number': fake.random_int(min=1, max=10000),
        'document_type_fk': random.randint(1, 10),
        'document_date': fake.date_time_between(start_date='-2y', end_date='now', tzinfo=None),
        'contractor_fk': random.randint(1, 50000),
        'client_fk': random.randint(1, 50000),
        'created_by_fk': random.randint(1, 50000),
        'created': fake.date_time_between(start_date='-2y', end_date='now', tzinfo=None).strftime('%Y-%m-%d %H:%M:%S.%f'),
        'modified_by_fk': random.randint(1, 50000),
        'last_modification': fake.date_time_between(start_date='-2y', end_date='now', tzinfo=None).strftime('%Y-%m-%d %H:%M:%S.%f'),
        'deleted': random.randint(0, 1),
        'deleted_by_fk': random.randint(1, 50000),
        'document_value': round(random.uniform(10, 1000), 2)
    })

# Seed the Product_documents table
product_document_insert_query = """
    INSERT INTO Product_documents (document_fk, product_fk, amount, product_value)
    VALUES (:document_fk, :product_fk, :amount, :product_value)
"""
for _ in range(100000):
    insert_data("Product_documents", product_document_insert_query, {
        'document_fk': random.randint(1, 100000),
        'product_fk': random.randint(1, 100000),
        'amount': round(random.uniform(0.01, 1000), 2),
        'product_value': round(random.uniform(0.01, 1000), 2)
    })

# Seed the Contractors table
contractor_insert_query = """
    INSERT INTO Contractors (id, address, country, name, business_number, account_number)
    VALUES (contractor_seq.nextval, :address, :country, :name, :business_number, :account_number)
"""
for _ in range(50000):
    insert_data("Contractors", contractor_insert_query, {
        'address': fake.address(),
        'country': fake.country_code(representation="alpha-2"),
        'name': fake.company(),
        'business_number': fake.random_int(min=1000000000, max=9999999999),
        'account_number': fake.iban()
    })

# Seed the Document_types table
document_types_to_seed = [
    ("Zamówienie", "zam"),
    ("Faktura", "fak"),
    ("Raport serwisowy", "rser"),
    ("Reklamacja", "rek"),
    ("List przewozowy", "lprz"),
    ("Dokument magazynowy", "dmag"),
    ("Dokument celny", "dcel"),
    ("Przetarg", "prze"),
    ("Audyt", "adt"),
    ("Umowa z kontrahentem", "uzk")
]

document_type_insert_query = """
    INSERT INTO document_types (name, abbreviation) VALUES (:name, :abbreviation)
"""

for document_type in document_types_to_seed:
    cursor.execute(document_type_insert_query, {
        'name': document_type[0],
        'abbreviation': document_type[1]
    })


# # Seed the Document_extension_types table
# document_extension_type_insert_query = """
#     INSERT INTO Document_extension_types (id, document_type_fk)
#     VALUES (doc_ext_type_seq.nextval, :document_type_fk)
# """
# for _ in range(10000):
#     insert_data("Document_extension_types", document_extension_type_insert_query, {
#         'document_type_fk': random.randint(1, 10)
#     })

# # Seed the Document_extensions table
# document_extension_insert_query = """
#     INSERT INTO Document_extensions (id, document_extension_type_fk, document_fk)
#     VALUES (doc_ext_seq.nextval, :document_extension_type_fk, :document_fk)
# """
# for _ in range(10000):
#     insert_data("Document_extensions", document_extension_insert_query, {
#         'document_extension_type_fk': random.randint(1, 2),
#         'document_fk': random.randint(1, 100000)
#     })

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
