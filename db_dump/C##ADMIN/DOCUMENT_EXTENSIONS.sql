create table DOCUMENT_EXTENSIONS
(
    ID                         NUMBER(10) not null
        primary key,
    DOCUMENT_EXTENSION_TYPE_FK NUMBER(10) not null
        references DOCUMENT_EXTENSION_TYPES,
    DOCUMENT_FK                NUMBER(10) not null
)
/

