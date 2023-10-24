create table ROLES
(
    ID   NUMBER(10)   not null
        primary key,
    NAME VARCHAR2(20) not null
        constraint UNIQUE_ROLE_NAME
            unique
)
/

