create table USERS
(
    ID           NUMBER(10)   not null
        primary key,
    NAME         VARCHAR2(20) not null,
    SURNAME      VARCHAR2(50) not null,
    ROLE_FK      NUMBER(10)   not null,
    COMPANY_FK   NUMBER(10),
    WAREHOUSE_FK NUMBER(10),
    EMAIL        VARCHAR2(40)
        check (REGEXP_LIKE(email, '.*@.*')),
    PHONE_NUMBER VARCHAR2(15) not null
        check (REGEXP_LIKE(phone_number, '^[0-9]*$')),
    LOGIN        VARCHAR2(15) not null,
    PASSWORD     VARCHAR2(25) not null,
    DELETED      NUMBER(1)    not null,
    constraint UNIQUE_USER_INFO
        unique (LOGIN, EMAIL, PHONE_NUMBER)
)
/

