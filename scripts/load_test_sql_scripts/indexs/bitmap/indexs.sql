-- Indeksy bitmapowe na PRODUCTS
-- Indeks bitmapowy na nazwę produktu
CREATE BITMAP INDEX bmp_idx_products_name ON PRODUCTS (NAME) LOCAL
-- Indeks bitmapowy na klucz obcy CONTRACTOR_FK
CREATE BITMAP INDEX bmp_idx_products_contractor_fk ON PRODUCTS (CONTRACTOR_FK) LOCAL
-- Indeks bitmapowy na długość specyfikacji (jeśli zastosowanie funkcji jest możliwe w indeksie bitmapowym)
CREATE BITMAP INDEX bmp_idx_products_spec_length ON PRODUCTS (LENGTH(SPECIFICATION)) LOCAL

-- Indeksy bitmapowe na DOCUMENTS
-- Indeks bitmapowy na datę dokumentu
CREATE BITMAP INDEX bmp_idx_documents_date ON DOCUMENTS (DOCUMENT_DATE) LOCAL
-- Indeks bitmapowy na klucz obcy CONTRACTOR_FK
CREATE BITMAP INDEX bmp_idx_documents_contractor_fk ON DOCUMENTS (CONTRACTOR_FK) LOCAL
-- Indeks bitmapowy na klucz obcy CLIENT_FK
CREATE BITMAP INDEX bmp_idx_documents_client_fk ON DOCUMENTS (CLIENT_FK) LOCAL
-- Indeks bitmapowy na klucz obcy DOCUMENT_TYPE_FK
CREATE BITMAP INDEX bmp_idx_documents_type_fk ON DOCUMENTS (DOCUMENT_TYPE_FK) LOCAL

-- Indeksy bitmapowe na USERS
-- Indeks bitmapowy na klucz obcy WAREHOUSE_FK
CREATE BITMAP INDEX bmp_idx_users_warehouse_fk ON USERS (WAREHOUSE_FK) LOCAL

-- Indeksy bitmapowe na PRICE_LISTS
-- Indeks bitmapowy na datę ważności cennika
CREATE BITMAP INDEX bmp_idx_price_lists_valid_date ON PRICE_LISTS (VALID_DATE) LOCAL

-- Dodatkowe indeksy bitmapowe
-- Złożony indeks bitmapowy na CLIENT_FK i DOCUMENT_DATE w DOCUMENTS
CREATE BITMAP INDEX bmp_idx_documents_client_fk_date ON DOCUMENTS (CLIENT_FK, DOCUMENT_DATE) LOCAL
-- Indeks bitmapowy na DOCUMENT_TYPES.ABBREVIATION i DOCUMENT_TYPES.ID (jeśli zastosowanie indeksu złożonego jest możliwe w indeksie bitmapowym)
CREATE BITMAP INDEX bmp_idx_document_types_abbreviation_id ON DOCUMENT_TYPES (ABBREVIATION, ID)
-- Indeks bitmapowy na PRODUCTS.CONTRACTOR_FK i PRODUCTS.PRODUCT_LENGTH (jeśli zastosowanie indeksu złożonego jest możliwe w indeksie bitmapowym)
CREATE BITMAP INDEX bmp_idx_products_contractor_fk_length ON PRODUCTS (CONTRACTOR_FK, PRODUCT_LENGTH) LOCAL
-- Indeks bitmapowy na PRICE_LISTS.PRODUCTS_FK i PRICE_LISTS.SALE (jeśli zastosowanie indeksu złożonego jest możliwe w indeksie bitmapowym)
CREATE BITMAP INDEX bmp_idx_price_lists_product_fk_sale ON PRICE_LISTS (PRODUCTS_FK, SALE) LOCAL
-- Indeks bitmapowy na PRODUCT_DOCUMENTS.DOCUMENT_FK i PRODUCT_DOCUMENTS.AMOUNT (jeśli zastosowanie indeksu złożonego jest możliwe w indeksie bitmapowym)
CREATE BITMAP INDEX bmp_idx_product_documents_doc_fk_amount ON PRODUCT_DOCUMENTS (DOCUMENT_FK, AMOUNT) LOCAL

-- Indeks bitmapowy na PRODUCTS.NAME dla porównań z LIKE '%a%'
CREATE BITMAP INDEX bmp_idx_func_products_name ON PRODUCTS (LOWER(NAME)) LOCAL

-- Indeks bitmapowy na rok z DOCUMENTS.DOCUMENT_DATE
CREATE BITMAP INDEX bmp_idx_func_documents_year ON DOCUMENTS (EXTRACT(YEAR FROM DOCUMENT_DATE)) LOCAL

-- Indeks bitmapowy na stosunek PRODUCT_WEIGHT do średniej wagi z tabeli PRODUCTS
-- Uwaga: Oracle może nie zezwolić na tworzenie indeksu bitmapowego z subzapytaniem.
-- CREATE BITMAP INDEX bmp_idx_func_products_weight_avg ON PRODUCTS (PRODUCT_WEIGHT / (SELECT AVG(PRODUCT_WEIGHT) FROM PRODUCTS))

-- Indeks bitmapowy na DOCUMENT_DATE w zakresie dat
-- Uwaga: Oracle może nie zezwolić na tworzenie indeksu bitmapowego z tego rodzaju wyrażeniem.
CREATE BITMAP INDEX bmp_idx_func_documents_date_range ON DOCUMENTS (CASE WHEN DOCUMENT_DATE BETWEEN TO_DATE('2020-01-01', 'YYYY-MM-DD') AND TO_DATE('2022-12-31', 'YYYY-MM-DD') THEN 1 ELSE 0 END) LOCAL

-- Indeks bitmapowy na PRODUCT_LENGTH i SALE w PRODUCTS i PRICE_LISTS
-- Uwaga: Oracle może nie zezwolić na tworzenie indeksu bitmapowego z subzapytaniem.
-- CREATE BITMAP INDEX bmp_idx_func_product_length_sale ON PRODUCTS (PRODUCT_LENGTH, (SELECT SALE FROM PRICE_LISTS WHERE PRODUCTS_FK = PRODUCTS.ID))
