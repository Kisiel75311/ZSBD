-- Indeksy na PRODUCTS
-- Indeks B-tree na nazwę produktu, optymalizacja zapytań z filtrowaniem po nazwie
CREATE INDEX idx_products_name ON PRODUCTS (NAME)
-- Indeks B-tree na klucz obcy CONTRACTOR_FK, optymalizacja zapytań łączących PRODUCTS z CONTRACTORS
CREATE INDEX idx_products_contractor_fk ON PRODUCTS (CONTRACTOR_FK)
-- Indeks funkcyjny na długość specyfikacji, użyteczny gdy filtrujemy produkty na podstawie długości specyfikacji
CREATE INDEX idx_products_spec_length ON PRODUCTS (LENGTH(SPECIFICATION))

-- Indeksy na DOCUMENTS
-- Indeks B-tree na datę dokumentu, optymalizacja zapytań z filtrowaniem po dacie
CREATE INDEX idx_documents_date ON DOCUMENTS (DOCUMENT_DATE)
-- Indeks B-tree na klucz obcy CONTRACTOR_FK, optymalizacja zapytań łączących DOCUMENTS z CONTRACTORS
CREATE INDEX idx_documents_contractor_fk ON DOCUMENTS (CONTRACTOR_FK)
-- Indeks B-tree na klucz obcy CLIENT_FK, optymalizacja zapytań łączących DOCUMENTS z USERS
CREATE INDEX idx_documents_client_fk ON DOCUMENTS (CLIENT_FK)
-- Indeks B-tree na klucz obcy DOCUMENT_TYPE_FK, optymalizacja zapytań łączących DOCUMENTS z DOCUMENT_TYPES
CREATE INDEX idx_documents_type_fk ON DOCUMENTS (DOCUMENT_TYPE_FK)

-- Indeksy na USERS
-- Indeks B-tree na klucz obcy WAREHOUSE_FK, optymalizacja zapytań łączących USERS z WAREHOUSES
CREATE INDEX idx_users_warehouse_fk ON USERS (WAREHOUSE_FK)

-- Indeksy na PRICE_LISTS
-- Indeks B-tree na datę ważności cennika, optymalizacja zapytań z filtrowaniem po dacie ważności
CREATE INDEX idx_price_lists_valid_date ON PRICE_LISTS (VALID_DATE)

-- Dodatkowe indeksy złożone
-- Złożony indeks B-tree na CLIENT_FK i DOCUMENT_DATE w DOCUMENTS
CREATE INDEX idx_documents_client_fk_date ON DOCUMENTS (CLIENT_FK, DOCUMENT_DATE)
-- Indeks B-tree na DOCUMENT_TYPES.ABBREVIATION i DOCUMENT_TYPES.ID
CREATE INDEX idx_document_types_abbreviation_id ON DOCUMENT_TYPES (ABBREVIATION, ID)
-- Złożony indeks B-tree na PRODUCTS.CONTRACTOR_FK i PRODUCTS.PRODUCT_LENGTH
CREATE INDEX idx_products_contractor_fk_length ON PRODUCTS (CONTRACTOR_FK, PRODUCT_LENGTH)
-- Indeks B-tree na PRICE_LISTS.PRODUCTS_FK i PRICE_LISTS.SALE
CREATE INDEX idx_price_lists_product_fk_sale ON PRICE_LISTS (PRODUCTS_FK, SALE)
-- Indeks B-tree na PRODUCT_DOCUMENTS.DOCUMENT_FK i PRODUCT_DOCUMENTS.AMOUNT
CREATE INDEX idx_product_documents_doc_fk_amount ON PRODUCT_DOCUMENTS (DOCUMENT_FK, AMOUNT)

-- Indeks funkcyjny na PRODUCTS.NAME dla porównań z LIKE '%a%'
CREATE INDEX idx_func_products_name ON PRODUCTS (LOWER(NAME))

-- Indeks funkcyjny na rok z DOCUMENTS.DOCUMENT_DATE
CREATE INDEX idx_func_documents_year ON DOCUMENTS (EXTRACT(YEAR FROM DOCUMENT_DATE))

-- Indeks funkcyjny na stosunek PRODUCT_WEIGHT do średniej wagi z tabeli PRODUCTS
-- CREATE INDEX idx_func_products_weight_avg ON PRODUCTS (PRODUCT_WEIGHT / (SELECT AVG(PRODUCT_WEIGHT) FROM PRODUCTS))

-- Indeks funkcyjny na DOCUMENT_DATE w zakresie dat
CREATE INDEX idx_func_documents_date_range ON DOCUMENTS (CASE WHEN DOCUMENT_DATE BETWEEN TO_DATE('2020-01-01', 'YYYY-MM-DD') AND TO_DATE('2022-12-31', 'YYYY-MM-DD') THEN 1 ELSE 0 END)

-- Indeks funkcyjny na PRODUCT_LENGTH i SALE w PRODUCTS i PRICE_LISTS
-- Uwaga: Ta komenda może nie działać w niektórych wersjach Oracle z powodu subzapytania w definicji indeksu.
-- CREATE INDEX idx_func_product_length_sale ON PRODUCTS (PRODUCT_LENGTH, (SELECT SALE FROM PRICE_LISTS WHERE PRODUCTS_FK = PRODUCTS.ID))
