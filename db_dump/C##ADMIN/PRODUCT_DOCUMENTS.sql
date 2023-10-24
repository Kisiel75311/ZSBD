create table PRODUCT_DOCUMENTS
(
    DOCUMENT_FK   NUMBER(10)    not null
        references DOCUMENTS,
    PRODUCT_FK    NUMBER(10)    not null
        references PRODUCTS,
    AMOUNT        NUMBER(10, 2) not null
        check (amount > 0),
    PRODUCT_VALUE NUMBER(10, 2) not null
        check (product_value > 0),
    primary key (DOCUMENT_FK, PRODUCT_FK)
)
/

