-- 3.partycje.sql
SELECT C.ID, C.BUSINESS_NUMBER, C.COUNTRY
FROM CONTRACTORS C
WHERE C.ID IN (SELECT Subquery.CONTRACTOR_FK
               FROM (SELECT DISTINCT D.CONTRACTOR_FK
                     FROM DOCUMENTS D
                              JOIN USERS U ON D.CLIENT_FK = U.ID
                              JOIN DOCUMENT_TYPES DT ON D.DOCUMENT_TYPE_FK = DT.ID
                              JOIN WAREHOUSES W ON U.WAREHOUSE_FK = W.ID
                              JOIN PRODUCTS P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
                              JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
                     WHERE D.DOCUMENT_DATE >= SYSDATE - 180
                       AND DT.ABBREVIATION in ('zam', 'dmag', 'prze')
                       AND P.PRODUCT_LENGTH < 50
                       AND PL.SALE > 100
                       AND D.ID IN (SELECT PD.DOCUMENT_FK
                                    FROM PRODUCT_DOCUMENTS PD
                                             JOIN DOCUMENTS D2 ON PD.DOCUMENT_FK = D2.ID
                                    WHERE D2.DOCUMENT_DATE BETWEEN SYSDATE - 365 AND SYSDATE
                                      AND PD.AMOUNT > (SELECT AVG(PD2.AMOUNT)
                                                       FROM PRODUCT_DOCUMENTS PD2
                                                                JOIN DOCUMENTS D3 ON PD2.DOCUMENT_FK = D3.ID
                                                       WHERE D3.DOCUMENT_DATE BETWEEN SYSDATE - 365 AND SYSDATE))
                     GROUP BY D.CONTRACTOR_FK
                     HAVING COUNT(D.ID) > 3) Subquery
               WHERE C.ID = Subquery.CONTRACTOR_FK)
  AND C.COUNTRY = 'VN'
  AND C.BUSINESS_NUMBER NOT IN (SELECT BUSINESS_NUMBER
                                FROM CONTRACTORS
                                WHERE COUNTRY <> 'VN')
ORDER BY (SELECT COUNT(*)
          FROM DOCUMENTS D
          WHERE D.CONTRACTOR_FK = C.ID
            AND D.DOCUMENT_DATE > SYSDATE - 90) DESC;