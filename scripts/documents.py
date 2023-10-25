import datetime

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


document_insert_query = """
    INSERT INTO Documents (id, document_number, document_type_fk, document_date, contractor_fk, client_fk, 
    created_by_fk, created, modified_by_fk, last_modification, deleted, deleted_by_fk, document_value)
    VALUES (document_seq.nextval, :document_number, :document_type_fk, :document_date, :contractor_fk, :client_fk, 
    :created_by_fk, TO_TIMESTAMP(:created, 'DD-MON-RR HH24.MI.SS.FF'), :modified_by_fk, 
    TO_TIMESTAMP(:last_modification, 'DD-MON-RR HH24.MI.SS.FF'), TO_TIMESTAMP(:deleted, 'DD-MON-RR HH24.MI.SS.FF'), :deleted_by_fk, :document_value)
"""

generated_document_number = set()

with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")

        # Fetch min and max IDs for relevant tables
        cursor.execute("SELECT MIN(id), MAX(id) FROM users")
        min_user_id, max_user_id = cursor.fetchone()

        cursor.execute("SELECT MIN(id), MAX(id) FROM contractors")
        min_contractor_id, max_contractor_id = cursor.fetchone()

        for _ in tqdm(range(100000)):
            # created_date = fake.date_time_this_decade() # ostatnia
            # last_modification_date = fake.date_time_between_dates(created_date, datetime.datetime.now())
            # deleted_date = fake.date_time_between_dates(last_modification_date, datetime.datetime.now())
            document_number = fake.unique.random_int(min=1, max=1000000)
            while document_number in generated_document_number:
                document_number = fake.unique.random_int(min=1, max=1000000)
            generated_document_number.add(document_number)

            created_date = fake.date_time_between(start_date="-10y", end_date="now")
            last_modification_date = fake.date_time_between_dates(
                datetime_start=created_date, datetime_end="now"
            )
            deleted_date = fake.date_time_between_dates(
                datetime_start=created_date, datetime_end=last_modification_date
            )

            # if last_modification_date > created_date and deleted_date < last_modification_date:
            #     break

            document_value = round(random.uniform(10, 1000), 2)
            #
            # if deleted_date <= created_date:
            #     continue  # Skip to next iteration, as this combination of dates violates a constraint
            #
            # if last_modification_date <= created_date or deleted_date <= last_modification_date:
            #     continue  # Skip to next iteration, as this combination of dates violates a constraint

            # Wybierz losowo, czy dokument ma być oznaczony jako usunięty (10% szans)
            is_deleted = random.random() < 0.10

            if is_deleted:
                deleted_date = fake.date_time_between_dates(
                    datetime_start=created_date, datetime_end=last_modification_date
                )
                deleted_by_fk = random.randint(min_user_id, max_user_id)
            else:
                deleted_date = None
                deleted_by_fk = None

            insert_data(cursor, "Documents", document_insert_query, {
                'document_number': document_number,
                'document_type_fk': random.randint(1, 10),
                'document_date': fake.date_this_decade(),
                'contractor_fk': random.randint(min_contractor_id, max_contractor_id + 1),
                'client_fk': random.randint(min_user_id, max_user_id + 1),
                'created_by_fk': random.randint(min_user_id, max_user_id +1),
                'created': created_date.strftime('%d-%B-%y %H.%M.%S.%f'),
                'modified_by_fk': random.randint(min_user_id, max_user_id + 1),
                'last_modification': last_modification_date.strftime('%d-%B-%y %H.%M.%S.%f'),
                'deleted': deleted_date.strftime('%d-%B-%y %H.%M.%S.%f') if deleted_date else None,
                'deleted_by_fk': deleted_by_fk,
                'document_value': document_value
            })

        connection.commit()

print("Operation completed!")

