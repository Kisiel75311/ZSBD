create table PRODUCTS
(
    ID             NUMBER(10)    not null
        primary key,
    NAME           VARCHAR2(100) not null,
    PRODUCT_WEIGHT NUMBER(10, 2)
        check (product_weight > 0),
    PRODUCT_HEIGHT NUMBER(10, 2)
        check (product_height > 0),
    PRODUCT_WIDTH  NUMBER(10, 2)
        check (product_width > 0),
    PRODUCT_LENGTH NUMBER(10, 2)
        check (product_length > 0),
    SPECIFICATION  CLOB,
    CONTRACTOR_FK  NUMBER(10)    not null
        constraint CONTRACTOR_PRODUCT_CON
            references CONTRACTORS
)
/

