create table PRICE_LISTS
(
    ID          NUMBER(10)    not null
        primary key,
    PRODUCTS_FK NUMBER(10)    not null
        constraint PRODUCTS_PRICE_LIST_CON
            references PRODUCTS,
    PURCHASE    NUMBER(10, 2) not null
        constraint CHK_PURCHASE_GT_0
            check (purchase > 0),
    NETTO       NUMBER(10, 2) not null
        constraint CHK_NETTO_GT_0
            check (netto > 0),
    BRUTTO      NUMBER(10, 2) not null,
    SALE        NUMBER(10, 2),
    constraint CHK_BRUTTO_GT_NETTO
        check (brutto > netto),
    constraint CHK_SALE_RANGE
        check (sale > 0 AND sale < brutto)
)
/

