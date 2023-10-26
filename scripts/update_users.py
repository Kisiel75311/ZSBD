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

roles_to_seed = [
    (1, "Accountant", 3),  # 3% - Firma
    (2, "ZSBD Specialist", 1),  # 1% - Może być w obu (Magazyn/Firma), ale zakładam tutaj Firma
    (3, "Customer", 5),  # 5% - Firma
    (4, "Sales Representative", 8),  # 8% - Firma
    (5, "Warehouse Operator", 25),  # 25% - Magazyn
    (6, "Warehouse Manager", 2),  # 2% - Magazyn
    (7, "Technical Support", 4),  # 4% - Firma
    (8, "Stock Coordinator", 4),  # 4% - Magazyn
    (9, "Forklift Operator", 10),  # 10% - Magazyn
    (10, "Warehouse SafetySpec", 2),  # 2% - Magazyn
    (11, "Warehouse Analyst", 3),  # 3% - Magazyn
    (12, "Customer ServiceSpec", 10),  # 10% - Firma
    (13, "Sales Director", 1),  # 1% - Firma
    (14, "Financial Analyst", 2),  # 2% - Firma
    (15, "Marketing Specialist", 20)  # 20% - Firma
]

# Funkcja do losowania roli na podstawie procentowych wartości
def choose_role():
    role_data = [(id, name, percentage) for id, name, percentage in roles_to_seed]
    role_ids, role_names, role_percentages = zip(*role_data)
    return random.choices(role_ids, weights=role_percentages)[0]

def insert_data(cursor, table_name, insert_query, data):
    try:
        cursor.execute(insert_query, data)  # Inserting the data once per call
    except cx_Oracle.Error as error:
        print(f"Error occurred when inserting into {table_name}:", error)

def get_existing_ids(cursor, table_name, column_name):
    """
    Pobiera istniejące ID z podanej tabeli i kolumny.
    """
    query = f"SELECT {column_name} FROM {table_name}"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

# Define the query for the Users table and the queries for fetching min and max ids
user_insert_query = """
    INSERT INTO Users (id, name, surname, role_fk, company_fk, warehouse_fk, email, phone_number, login, password, deleted)
    VALUES (user_seq.nextval, :name, :surname, :role_fk, :company_fk, :warehouse_fk, :email, :phone_number, :login, :password, :deleted)
"""

update_query = """
    UPDATE Users
    SET role_fk = :role_fk,
        company_fk = :company_fk,
        warehouse_fk = :warehouse_fk,
        deleted = :deleted
    WHERE id = :user_id
"""

role_query = "SELECT MIN(id), MAX(id) FROM Roles"
company_query = "SELECT MIN(id), MAX(id) FROM Companies"
warehouse_query = "SELECT MIN(id), MAX(id) FROM Warehouses"

# Connect to the database, fetch min-max values, and update data
# ... (kod wcześniejszy)

# Connect to the database, fetch min-max values, and update data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        # Pobierz istniejące ID dla roli, firmy i magazynu
        role_ids = get_existing_ids(cursor, "Roles", "id")
        company_ids = get_existing_ids(cursor, "Companies", "id")
        warehouse_ids = get_existing_ids(cursor, "Warehouses", "id")

        # Pobierz istniejące ID użytkowników, których chcesz zaktualizować
        user_ids = get_existing_ids(cursor, "Users", "id")

        for user_id in tqdm(user_ids):
            role_id = choose_role()
            company_id = None
            warehouse_id = None

            # Sprawdź, czy rola jest pracownikiem firmy lub magazynu
            if role_id in role_ids[:4]:  # Rola pracownika firmy
                company_id = random.choice(company_ids)
                warehouse_id = None
            elif role_id in role_ids[4:]:  # Rola pracownika magazynu
                warehouse_id = random.choice(warehouse_ids)
                company_id = None

            # Wybierz 15% użytkowników do usunięcia
            deleted = 1 if random.randint(1, 100) <= 15 else 0

            data = {
                "user_id": user_id,
                "role_fk": role_id,
                "company_fk": company_id,
                "warehouse_fk": warehouse_id,
                "deleted": deleted
            }

            # Aktualizuj dane użytkownika w tabeli USERS
            insert_data(cursor, "Users", update_query, data)

        # Zatwierdź transakcję
        connection.commit()
