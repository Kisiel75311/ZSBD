SELECT U.ID, U.NAME, U.SURNAME, COUNT(DISTINCT D.ID) AS DOCUMENT_COUNT
FROM USERS U
         JOIN DOCUMENTS D ON U.ID = D.CLIENT_FK
         JOIN DOCUMENT_TYPES DT ON D.DOCUMENT_TYPE_FK = DT.ID
         JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
         JOIN PRODUCTS P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
         JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
    AND P.PRODUCT_LENGTH < 60
    AND PL.SALE > 150
    AND U.ID IN (SELECT DISTINCT U1.ID
                 FROM USERS U1
                          JOIN DOCUMENTS D1 ON U1.ID = D1.CLIENT_FK
                 WHERE TO_NUMBER(TO_CHAR(D1.DOCUMENT_DATE, 'YYYY') >= 2022
                   AND D1.DOCUMENT_TYPE_FK = 3)
GROUP BY U.ID, U.NAME, U.SURNAME
HAVING COUNT(DISTINCT D.ID) > 5;