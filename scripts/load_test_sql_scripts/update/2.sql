DECLARE
    updated_user_count NUMBER;
BEGIN
    UPDATE DOCUMENTS D
    SET DOCUMENT_VALUE    = DOCUMENT_VALUE * 1.1,
        LAST_MODIFICATION = SYSTIMESTAMP
    WHERE D.DOCUMENT_DATE >= TO_DATE('2022-01-01', 'YYYY-MM-DD')
      AND D.DOCUMENT_DATE <= TO_DATE('2022-12-31', 'YYYY-MM-DD')
      AND D.DOCUMENT_TYPE_FK IN (2, 3)
      AND D.CONTRACTOR_FK IN (SELECT DISTINCT P.CONTRACTOR_FK
                              FROM PRODUCTS P
                                       JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
                              WHERE PL.SALE > 100)
      AND EXISTS (SELECT 1
                  FROM USERS U
                           JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
                  WHERE W.COUNTRY = 'PL');

    SELECT COUNT(DISTINCT U.ID)
    INTO updated_user_count
    FROM USERS U
             JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
    WHERE W.NAME = '%Sp.%';

    DBMS_OUTPUT.PUT_LINE('Updated user count: ' || TO_CHAR(updated_user_count));
END;

