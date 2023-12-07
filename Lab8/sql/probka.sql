ALTER SYSTEM FLUSH SHARED_POOL;

DELETE
FROM 'C##ZSBD'."PRODUCT" C##ZSBD "." DOCUMENTS "" PC
WHERE PRODUCT_FK IN (
    SELECT P.ID
    FROM 'C##ZSBD'."PRODUCTS" P
    JOIN 'C##ZSBD'."CONTRACTORS" C ON P.CONTRACTOR_FK = C.ID
    WHERE P.NAME LIKE '%a%'
    )
  AND DOCUMENT_FK IN (
    SELECT D.ID
    FROM 'C##ZSBD'."DOCUMENTS" D
    WHERE D.DOCUMENT_DATE <= TO_DATE('2022-12-31'
    , 'YYYY-MM-DD')
    );



SELECT /*+ NO_RESULT_CACHE */ U.ID, U.NAME, U.SURNAME, COUNT(DISTINCT D.ID) AS DOCUMENT_COUNT
FROM 'C##ZSBD'."USERS" U
    JOIN 'C##ZSBD'."DOCUMENTS" D
ON U.ID = D.CLIENT_FK
    JOIN 'C##ZSBD'."DOCUMENT_TYPES" DT ON D.DOCUMENT_TYPE_FK = DT.ID
    JOIN 'C##ZSBD'."WAREHOUSES" W ON U.WAREHOUSE_FK = W.ID
    JOIN 'C##ZSBD'."PRODUCTS" P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
    JOIN 'C##ZSBD'."PRICE_LISTS" PL ON P.ID = PL.'C##ZSBD'."PRODUCTS"_FK
    AND P.PRODUCT_LENGTH < 60
    AND PL.SALE > 150
    AND U.ID IN (SELECT DISTINCT U1.ID
    FROM 'C##ZSBD'."USERS" U1
    JOIN 'C##ZSBD'."DOCUMENTS" D1 ON U1.ID = D1.CLIENT_FK
    WHERE TO_NUMBER(TO_CHAR(D1.DOCUMENT_DATE, 'YYYY')) >= 2022
    AND D1.DOCUMENT_TYPE_FK = 3)
GROUP BY U.ID, U.NAME, U.SURNAME
HAVING COUNT(DISTINCT D.ID) > 5;


SELECT /*+ NO_RESULT_CACHE */ C.ID, C.BUSINESS_NUMBER, C.COUNTRY
FROM 'C##ZSBD'."CONTRACTORS" C
WHERE C.ID IN (SELECT Subquery.CONTRACTOR_FK
               FROM (SELECT DISTINCT D.CONTRACTOR_FK
                     FROM 'C##ZSBD'."DOCUMENTS" D
                              JOIN 'C##ZSBD'."USERS" U ON D.CLIENT_FK = U.ID
                              JOIN 'C##ZSBD'."DOCUMENT_TYPES" DT ON D.DOCUMENT_TYPE_FK = DT.ID
                              JOIN 'C##ZSBD'."WAREHOUSES" W ON U.WAREHOUSE_FK = W.ID
                              JOIN 'C##ZSBD'."PRODUCTS" P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
                              JOIN 'C##ZSBD'."PRICE_LISTS" PL ON P.ID = PL.'C##ZSBD'."PRODUCTS"_FK
                     WHERE D.DOCUMENT_DATE >= SYSDATE - 180
                       AND DT.ABBREVIATION in ('zam'
                         , 'dmag'
                         , 'prze')
                       AND P.PRODUCT_LENGTH
                         < 50
                       AND PL.SALE
                         > 100
                       AND D.ID IN (SELECT PD.DOCUMENT_FK
                         FROM 'C##ZSBD'."PRODUCT_" C##ZSBD "." DOCUMENTS "" PD
                         JOIN 'C##ZSBD'."DOCUMENTS" D2 ON PD.DOCUMENT_FK = D2.ID
                         WHERE D2.DOCUMENT_DATE BETWEEN SYSDATE - 365
                       AND SYSDATE
                       AND PD.AMOUNT
                         > (SELECT AVG(PD2.AMOUNT)
                         FROM 'C##ZSBD'."PRODUCT_" C##ZSBD "." DOCUMENTS "" PD2
                         JOIN 'C##ZSBD'."DOCUMENTS" D3 ON PD2.DOCUMENT_FK = D3.ID
                         WHERE D3.DOCUMENT_DATE BETWEEN SYSDATE - 365
                       AND SYSDATE))
                     GROUP BY D.CONTRACTOR_FK
                     HAVING COUNT(D.ID) > 3) Subquery
               WHERE C.ID = Subquery.CONTRACTOR_FK)
AND C.COUNTRY = 'VN'
AND C.BUSINESS_NUMBER NOT IN (SELECT BUSINESS_NUMBER
                                FROM 'C##ZSBD'."CONTRACTORS"
                                WHERE COUNTRY <> 'VN')
ORDER BY (SELECT COUNT(*)
          FROM 'C##ZSBD'."DOCUMENTS" D
          WHERE D.CONTRACTOR_FK = C.ID
            AND D.DOCUMENT_DATE > SYSDATE - 90) DESC;


SELECT /*+ NO_RESULT_CACHE */ C.ID, C.BUSINESS_NUMBER, C.COUNTRY
FROM 'C##ZSBD'."CONTRACTORS" C
WHERE C.ID IN (SELECT Subquery.CONTRACTOR_FK
               FROM (SELECT SubSubquery.CONTRACTOR_FK
                     FROM (SELECT DISTINCT D.CONTRACTOR_FK
                           FROM 'C##ZSBD'."DOCUMENTS" D
                                    JOIN 'C##ZSBD'."USERS" U ON D.CLIENT_FK = U.ID
                                    JOIN 'C##ZSBD'."DOCUMENT_TYPES" DT ON D.DOCUMENT_TYPE_FK = DT.ID
                                    JOIN 'C##ZSBD'."WAREHOUSES" W ON U.WAREHOUSE_FK = W.ID
                                    JOIN 'C##ZSBD'."PRODUCTS" P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
                                    JOIN 'C##ZSBD'."PRICE_LISTS" PL ON P.ID = PL.'C##ZSBD'."PRODUCTS"_FK
                           WHERE D.DOCUMENT_DATE >= SYSDATE - 180
                             AND DT.ABBREVIATION = 'zam'
                             AND P.PRODUCT_LENGTH
                               < 50
                             AND PL.SALE
                               > 100
                           GROUP BY D.CONTRACTOR_FK
                           HAVING COUNT(D.ID) > 3) SubSubquery) Subquery
               WHERE C.ID = Subquery.CONTRACTOR_FK)
AND C.COUNTRY = 'PL';


UPDATE
'C##ZSBD'."PRODUCTS" P
SET P.PRODUCT_WEIGHT = CASE
    WHEN P.PRODUCT_WEIGHT > 1.3 * (SELECT AVG(P2.PRODUCT_WEIGHT) FROM 'C##ZSBD'."PRODUCTS" P2)
    THEN CASE
    WHEN P.PRODUCT_WEIGHT * 1.3 >
    (SELECT AVG(P2.PRODUCT_WEIGHT) FROM 'C##ZSBD'."PRODUCTS" P2)
    THEN P.PRODUCT_WEIGHT +
    (SELECT STDDEV(P2.PRODUCT_WEIGHT) FROM 'C##ZSBD'."PRODUCTS" P2)
    ELSE P.PRODUCT_WEIGHT * 1.3
    END
    ELSE P.PRODUCT_WEIGHT
    END
    WHERE P.ID IN (SELECT PL.'C##ZSBD'."PRODUCTS"_FK
    FROM 'C##ZSBD'."PRICE_LISTS" PL
    WHERE PL.VALID_DATE BETWEEN SYSDATE - INTERVAL '2' YEAR AND SYSDATE
    GROUP BY PL.'C##ZSBD'."PRODUCTS"_FK
    HAVING AVG(PL.SALE)
    > (SELECT AVG(PL2.SALE)
    FROM 'C##ZSBD'."PRICE_LISTS" PL2
    WHERE PL2.VALID_DATE BETWEEN SYSDATE - INTERVAL '2' YEAR
    AND SYSDATE));



UPDATE
'C##ZSBD'."PRICE_LISTS"
SET SALE = SALE * 1.1,
    PURCHASE = (SELECT AVG(PURCHASE) FROM 'C##ZSBD'."PRICE_LISTS")
    WHERE ID IN (SELECT PL.ID
    FROM 'C##ZSBD'."PRICE_LISTS" PL
    INNER JOIN 'C##ZSBD'."PRODUCTS" P ON P.ID = PL.'C##ZSBD'."PRODUCTS"_FK
    WHERE P.PRODUCT_LENGTH
    > 100
    AND LENGTH(P.SPECIFICATION)
    < 500);



UPDATE
'C##ZSBD'."CONTRACTORS" C
SET C.BUSINESS_NUMBER = '1234567890', -- Make sure this value is 10 characters or less
C.COUNTRY         = 'PL'
WHERE C.ID IN (SELECT DISTINCT D.CONTRACTOR_FK
               FROM 'C##ZSBD'."DOCUMENTS" D
                        JOIN 'C##ZSBD'."USERS" U ON D.CLIENT_FK = U.ID
                        JOIN 'C##ZSBD'."DOCUMENT_TYPES" DT ON D.DOCUMENT_TYPE_FK = DT.ID
                        JOIN 'C##ZSBD'."WAREHOUSES" W ON U.WAREHOUSE_FK = W.ID
                        JOIN 'C##ZSBD'."PRODUCTS" P ON D.CONTRACTOR_FK = P.CONTRACTOR_FK
                        JOIN 'C##ZSBD'."PRODUCT_" C##ZSBD "." DOCUMENTS "" PD
               ON D.ID = PD.DOCUMENT_FK
                   JOIN 'C##ZSBD'."PRICE_LISTS" PL ON P.ID = PL.'C##ZSBD'."PRODUCTS"_FK
               WHERE D.DOCUMENT_DATE >= SYSDATE - 180
                 AND DT.ABBREVIATION IN ('dcel'
                   , 'prze'
                   , 'adt')
                 AND U.NAME LIKE 'Adam%'
                 AND P.PRODUCT_LENGTH
                   > 50
                 AND PL.PURCHASE
                   > 100
                 AND PD.AMOUNT
                   > 5
               GROUP BY D.CONTRACTOR_FK
               HAVING COUNT(D.ID) > 3);


INSERT INTO 'C##ZSBD'."WAREHOUSE_COMPANY" (WAREHOUSE_ID, COMPANY_ID)
SELECT w.ID AS WAREHOUSE_ID,
       c.ID AS COMPANY_ID
FROM (SELECT w.ID, w.TotalCurrentCompanies, n.TargetAverage
      FROM (SELECT w.ID, COUNT(wc.COMPANY_ID) AS TotalCurrentCompanies
            FROM 'C##ZSBD'."WAREHOUSES" w
                LEFT JOIN 'C##ZSBD'."WAREHOUSE_COMPANY" wc
            ON w.ID = wc.WAREHOUSE_ID
            GROUP BY w.ID) w
               CROSS JOIN (SELECT (COUNT(*) / COUNT(DISTINCT WAREHOUSE_ID)) * 1.4 AS TargetAverage
                           FROM 'C##ZSBD'."WAREHOUSE_COMPANY") n
      WHERE w.TotalCurrentCompanies < n.TargetAverage) w
         CROSS JOIN (SELECT ID
                     FROM COMPANIES
                     ORDER BY DBMS_RANDOM.VALUE) c
WHERE ROWNUM <= (SELECT CEIL(SUM(n.TargetAverage - w.TotalCurrentCompanies))
                 FROM (SELECT w.ID, COUNT(wc.COMPANY_ID) AS TotalCurrentCompanies
                       FROM 'C##ZSBD'."WAREHOUSES" w
                           LEFT JOIN 'C##ZSBD'."WAREHOUSE_COMPANY" wc
                       ON w.ID = wc.WAREHOUSE_ID
                       GROUP BY w.ID) w
                          CROSS JOIN (SELECT (COUNT(*) / COUNT(DISTINCT WAREHOUSE_ID)) * 1.4 AS TargetAverage
                                      FROM 'C##ZSBD'."WAREHOUSE_COMPANY") n
                 WHERE w.TotalCurrentCompanies < n.TargetAverage);



DELETE
FROM 'C##ZSBD'."DOCUMENTS" D
WHERE D.DOCUMENT_DATE >= TO_DATE('2020-01-01'
    , 'YYYY-MM-DD')
  AND D.DOCUMENT_DATE <= TO_DATE('2022-12-31'
    , 'YYYY-MM-DD')
  AND D.DOCUMENT_TYPE_FK IN (SELECT DT.ID
    FROM 'C##ZSBD'."DOCUMENT_TYPES" DT
    WHERE DT.ABBREVIATION IN ('Type1'
    , 'Type2'
    , 'Type3'))
  AND D.CONTRACTOR_FK IN (SELECT DISTINCT P.CONTRACTOR_FK
    FROM 'C##ZSBD'."PRODUCTS" P
    JOIN 'C##ZSBD'."PRICE_LISTS" PL ON P.ID = PL.'C##ZSBD'."PRODUCTS"_FK
    WHERE PL.PURCHASE
    < 50)
  AND EXISTS (SELECT 1
    FROM 'C##ZSBD'."USERS" U
    JOIN 'C##ZSBD'."WAREHOUSES" W ON U.WAREHOUSE_FK = W.ID
    WHERE W.NAME = '%a%');
