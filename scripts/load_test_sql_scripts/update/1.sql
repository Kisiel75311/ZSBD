UPDATE CONTRACTORS C
SET C.BUSINESS_NUMBER = '1234567890', -- Make sure this value is 10 characters or less
    C.COUNTRY         = 'PL'
WHERE C.ID IN (SELECT DISTINCT D.CONTRACTOR_FK
               FROM DOCUMENTS D
                        JOIN USERS U ON D.CLIENT_FK = U.ID
                        JOIN DOCUMENT_TYPES DT ON D.DOCUMENT_TYPE_FK = DT.ID
                        JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
                        JOIN PRODUCTS P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
                        JOIN PRODUCT_DOCUMENTS PD ON D.ID = PD.DOCUMENT_FK
                        JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
               WHERE D.DOCUMENT_DATE >= SYSDATE - 180
                 AND DT.ABBREVIATION IN ('dcel', 'prze', 'adt')
                 AND U.NAME LIKE 'Adam%'
                 AND P.PRODUCT_LENGTH > 50
                 AND PL.PURCHASE > 100
                 AND PD.AMOUNT > 5
               GROUP BY D.CONTRACTOR_FK
               HAVING COUNT(D.ID) > 3);
