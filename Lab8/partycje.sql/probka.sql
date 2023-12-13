-- 1.sql
ALTER TABLE products
    MODIFY
        PARTITION BY RANGE (contractor_fk) (
        PARTITION p1 VALUES LESS THAN (100),
        PARTITION p2 VALUES LESS THAN (200),
        PARTITION p3 VALUES LESS THAN (MAXVALUE)
        );
ALTER TABLE documents
    MODIFY
        PARTITION BY RANGE (document_date) (
        PARTITION docs_before_2020 VALUES LESS THAN (DATE '2020-01-01'),
        PARTITION docs_2020 VALUES LESS THAN (DATE '2021-01-01'),
        PARTITION docs_after_2020 VALUES LESS THAN (MAXVALUE)
        );

ALTER TABLE product_documents
    MODIFY
        PARTITION BY RANGE (document_fk) (
        PARTITION docs_low VALUES LESS THAN (1000),
        PARTITION docs_mid VALUES LESS THAN (2000),
        PARTITION docs_high VALUES LESS THAN (MAXVALUE)
        ) SUBPARTITION BY LIST (product_fk)
                               (
    SUBPARTITION prod_low VALUES (1, 2, 3),
    SUBPARTITION prod_high VALUES (DEFAULT)
);

-- 2.sql
