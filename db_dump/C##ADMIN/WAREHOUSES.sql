create table WAREHOUSES
(
    ID           NUMBER(10)    not null
        primary key,
    NAME         VARCHAR2(20)  not null,
    ADDRESS      VARCHAR2(300) not null,
    COMPANIES_FK NUMBER(10)    not null
        constraint COMPANIES_WAREHOUSE_CON
            references COMPANIES
)
/

