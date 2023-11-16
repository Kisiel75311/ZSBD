DELETE
FROM DOCUMENTS D
WHERE D.DOCUMENT_DATE >= TO_DATE('2020-01-01', 'YYYY-MM-DD')
  AND D.DOCUMENT_DATE <= TO_DATE('2022-12-31', 'YYYY-MM-DD')
  AND D.DOCUMENT_TYPE_FK IN (SELECT DT.ID
                             FROM DOCUMENT_TYPES DT
                             WHERE DT.ABBREVIATION IN ('Type1', 'Type2', 'Type3'))
  AND D.CONTRACTOR_FK IN (SELECT DISTINCT P.CONTRACTOR_FK
                          FROM PRODUCTS P
                                   JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
                          WHERE PL.PURCHASE < 50)
  AND EXISTS (SELECT 1
              FROM USERS U
                       JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
              WHERE W.NAME = '%a%');