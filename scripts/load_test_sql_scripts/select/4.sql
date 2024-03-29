SELECT C.ID, C.BUSINESS_NUMBER, C.COUNTRY
FROM CONTRACTORS C
WHERE C.ID IN (SELECT Subquery.CONTRACTOR_FK
               FROM (SELECT SubSubquery.CONTRACTOR_FK
                     FROM (SELECT DISTINCT D.CONTRACTOR_FK
                           FROM DOCUMENTS D
                                    JOIN USERS U ON D.CLIENT_FK = U.ID
                                    JOIN DOCUMENT_TYPES DT ON D.DOCUMENT_TYPE_FK = DT.ID
                                    JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
                                    JOIN PRODUCTS P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
                                    JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
                           WHERE D.DOCUMENT_DATE >= SYSDATE - 180
                             AND DT.ABBREVIATION = 'zam'
                             AND P.PRODUCT_LENGTH < 50
                             AND PL.SALE > 100
                           GROUP BY D.CONTRACTOR_FK
                           HAVING COUNT(D.ID) > 3) SubSubquery) Subquery
               WHERE C.ID = Subquery.CONTRACTOR_FK)
  AND C.COUNTRY = 'PL';