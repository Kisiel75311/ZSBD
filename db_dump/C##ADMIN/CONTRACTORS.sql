create table CONTRACTORS
(
    ID              NUMBER(10)    not null
        primary key,
    ADDRESS         VARCHAR2(300) not null,
    COUNTRY         VARCHAR2(100)
        check (REGEXP_LIKE(country, '^[A-Z]*$')),
    NAME            VARCHAR2(100) not null,
    BUSINESS_NUMBER CHAR(10)      not null
        check (REGEXP_LIKE(business_number, '^[0-9]*$')),
    ACCOUNT_NUMBER  CHAR(28)      not null
        constraint UNIQUE_ACCOUNT_NUMBER
            unique
)
/

