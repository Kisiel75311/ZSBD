create table COMPANIES
(
    ID              NUMBER(10)    not null
        primary key,
    NAME            VARCHAR2(30)  not null,
    ADDRESS         VARCHAR2(300) not null,
    BUSINESS_NUMBER CHAR(10)
        check (REGEXP_LIKE(business_number, '^[0-9]*$')),
    REGON           CHAR(9)
        check (REGEXP_LIKE(regon, '^[0-9]*$')),
    KRS             CHAR(9)
        check (REGEXP_LIKE(krs, '^[0-9]*$')),
    ACCOUNT_NUMBER  CHAR(35)      not null,
    constraint UNIQUE_COMPANY_INFO
        unique (NAME, ACCOUNT_NUMBER)
)
/

