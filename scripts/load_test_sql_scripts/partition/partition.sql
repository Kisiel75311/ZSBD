-- Products Table
-- Partycjonowanie po zakresie na podstawie długości produktu.
-- Cel: Optymalizacja zapytań dotyczących różnych rozmiarów produktów.
ALTER TABLE products
    MODIFY
        PARTITION BY RANGE (product_length) (
        PARTITION pl_short VALUES LESS THAN (333),    -- Produkty o krótkiej długości
        PARTITION pl_medium VALUES LESS THAN (666),   -- Produkty o średniej długości
        PARTITION pl_long VALUES LESS THAN (MAXVALUE) -- Produkty o długiej długości
        );

-- Documents Table
-- Partycjonowanie po zakresie na podstawie daty dokumentu.
-- Cel: Ułatwienie zarządzania dokumentami i optymalizacja zapytań w oparciu o datę.
ALTER TABLE documents
    MODIFY
        PARTITION BY RANGE (document_date) (
        PARTITION docs_before_2020 VALUES LESS THAN (TO_DATE('2020-01-01', 'YYYY-MM-DD')), -- Dokumenty sprzed 2020 roku
        PARTITION docs_2020_2021 VALUES LESS THAN (TO_DATE('2022-01-01', 'YYYY-MM-DD')),   -- Dokumenty z lat 2020-2021
        PARTITION docs_after_2021 VALUES LESS THAN (MAXVALUE)                             -- Dokumenty po 2021 roku
        );

-- Price_Lists Table
-- Partycjonowanie po hash na podstawie klucza obcego products_fk.
-- Cel: Równomierny rozkład danych i optymalizacja zapytań.
ALTER TABLE price_lists
    MODIFY
        PARTITION BY HASH (products_fk) PARTITIONS 4; -- 4 partycje dla równomiernego rozkładu danych # Nie jestem pewny czy ta partycja nie pogarsza wyniku zapytania nymer 6, brakło czasu na weryfikację


-- Users Table
-- Partycjonowanie po liście na podstawie klucza obcego warehouse_fk.
-- Cel: Optymalizacja zapytań dotyczących użytkowników przypisanych do konkretnych magazynów.
ALTER TABLE users
    MODIFY
        PARTITION BY LIST (warehouse_fk) (
        PARTITION wh1 VALUES (541460),    -- Użytkownicy związani z magazynem o ID 541460
        PARTITION wh2 VALUES (547276),    -- Użytkownicy związani z magazynem o ID 547276
        PARTITION wh_others VALUES (DEFAULT) -- Pozostałe wartości (w tym NULL)
        );

-- Product_Documents Table
-- Partycjonowanie po zakresie i liście na podstawie kluczy obcych document_fk i product_fk.
-- Cel: Optymalizacja zapytań poprzez oddzielenie dokumentów produktów na podstawie ID dokumentu i ID produktu.
ALTER TABLE product_documents
    MODIFY
        PARTITION BY RANGE (document_fk) SUBPARTITION BY LIST (product_fk) (
        PARTITION docs_low VALUES LESS THAN (41000) (
            SUBPARTITION docs_low_prod_low VALUES (83346, 75240, 52929), -- Dokumenty o niskim ID z określonymi produktami
            SUBPARTITION docs_low_prod_high VALUES (DEFAULT)             -- Dokumenty o niskim ID z pozostałymi produktami
            ),
        PARTITION docs_mid VALUES LESS THAN (92000) (
            SUBPARTITION docs_mid_prod_low VALUES (83346,


-- Product_Documents Table
ALTER TABLE product_documents
    MODIFY
        PARTITION BY RANGE (document_fk) SUBPARTITION BY LIST (product_fk) (
        PARTITION docs_low VALUES LESS THAN (41000) (
            SUBPARTITION docs_low_prod_low VALUES (83346, 75240, 52929),
            SUBPARTITION docs_low_prod_high VALUES (DEFAULT)
            ),
        PARTITION docs_mid VALUES LESS THAN (92000) (
            SUBPARTITION docs_mid_prod_low VALUES (83346, 75240, 52929),
            SUBPARTITION docs_mid_prod_high VALUES (DEFAULT)
            ),
        PARTITION docs_high VALUES LESS THAN (MAXVALUE) (
            SUBPARTITION docs_high_prod_low VALUES (83346, 75240, 52929),
            SUBPARTITION docs_high_prod_high VALUES (DEFAULT)
            )
        );

