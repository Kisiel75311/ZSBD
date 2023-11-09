INSERT INTO PRODUCTS (NAME, PRODUCT_WEIGHT, PRODUCT_LENGTH, PRODUCT_HEIGHT, PRODUCT_WIDTH, SPECIFICATION, CONTRACTOR_FK)
SELECT 'New Product', AVG(P.PRODUCT_WEIGHT), 60.0, 30.0, 10.0, 'This is a new product description.', C.CONTRACTOR_ID
FROM (SELECT D.CONTRACTOR_FK AS CONTRACTOR_ID
      FROM DOCUMENTS D
      WHERE D.DOCUMENT_DATE >= SYSDATE - 180
      GROUP BY D.CONTRACTOR_FK
      HAVING COUNT(D.ID) > 3) C
WHERE C.CONTRACTOR_ID IN (SELECT DISTINCT P.CONTRACTOR_FK
                          FROM PRODUCTS P
                                   JOIN WAREHOUSES W ON P.WAREHOUSE_FK = W.ID
                          WHERE W.ADDRESS LIKE '%Lu%'
                            AND P.ID NOT IN (SELECT PD.PRODUCT_FK
                                             FROM PRODUCT_DOCUMENTS PD
                                                      JOIN DOCUMENTS D ON PD.DOCUMENT_FK = D.ID
                                             WHERE D.DOCUMENT_DATE < SYSDATE - 180));