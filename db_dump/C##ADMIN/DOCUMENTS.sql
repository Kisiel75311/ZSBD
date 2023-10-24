create table DOCUMENTS
(
    ID                NUMBER(10)                        not null
        primary key,
    DOCUMENT_NUMBER   NUMBER(10)                        not null
        constraint UNIQUE_DOCUMENT_NUMBER
            unique,
    DOCUMENT_TYPE_FK  NUMBER(10)                        not null
        references DOCUMENT_TYPES,
    DOCUMENT_DATE     DATE,
    CONTRACTOR_FK     NUMBER(10)
        references CONTRACTORS,
    CLIENT_FK         NUMBER(10)
        references USERS,
    CREATED_BY_FK     NUMBER(10)
        references USERS,
    CREATED           TIMESTAMP(6) default SYSTIMESTAMP not null,
    MODIFIED_BY_FK    NUMBER(10)
        references USERS,
    LAST_MODIFICATION TIMESTAMP(6),
    DELETED           TIMESTAMP(6),
    DELETED_BY_FK     NUMBER(10)
        references USERS,
    DOCUMENT_VALUE    NUMBER(10, 2)
        check (document_value > 0),
    constraint CHK_DATES1
        check (last_modification > created),
    constraint CHK_DATES2
        check (deleted > created),
    constraint CHK_LAST_MODIFICATION
        check (last_modification > created AND deleted < last_modification)
)
/

