create table DOCUMENT_EXTENSION_TYPES
(
    ID               NUMBER(10) not null
        primary key,
    DOCUMENT_TYPE_FK NUMBER(10) not null
        references DOCUMENT_TYPES
)
/

