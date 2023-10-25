import cx_Oracle

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
INSERT INTO document_types (id, name, abbreviation) VALUES (document_type_seq.nextval, :name, :abbreviation)
"""

# Connect to the database and insert data
with cx_Oracle.connect(username, password, dsn) as connection:
    with connection.cursor() as cursor:
        print("Connected successfully!")
        for document_type in document_types_to_seed:
            try:
                cursor.execute(document_type_insert_query, {
                    'name': document_type[0],
                    'abbreviation': document_type[1]
                })
            except cx_Oracle.Error as error:
                print("Error occurred when inserting document type:", error)
        connection.commit()  # Commit after all inserts

print("Operation completed!")
