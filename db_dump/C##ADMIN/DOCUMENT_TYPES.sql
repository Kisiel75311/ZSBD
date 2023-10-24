create table DOCUMENT_TYPES
(
    ID           NUMBER(10)   not null
        primary key,
    NAME         VARCHAR2(30) not null,
    ABBREVIATION VARCHAR2(4)  not null,
    constraint UNIQUE_DOCUMENT_TYPE_INFO
        unique (NAME, ABBREVIATION)
)
/

