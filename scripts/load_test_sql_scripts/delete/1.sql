DELETE FROM PRODUCT_DOCUMENTS PD
WHERE PD.PRODUCT_FK IN (
    SELECT DISTINCT P.ID
    FROM PRODUCTS P
    JOIN PRICE_LISTS PL ON P.ID = PL.PRODUCTS_FK
    WHERE P.PRODUCT_WEIGHT < 5 -- Weight constraint
    AND P.PRODUCT_LENGTH < 75 -- Length constraint
    AND P.PRODUCT_HEIGHT > 20 -- Height constraint
    AND PL.PURCHASE < 50 -- Purchase price constraint
    AND P.ID IN (
        SELECT DISTINCT P1.ID
        FROM PRODUCTS P1
        JOIN WAREHOUSES W ON P1.WAREHOUSE_FK = W.ID
        WHERE W.ADDRESS LIKE '%New York%' -- Warehouse location constraint
    )
    AND P.ID IN (
        SELECT DISTINCT P2.ID
        FROM PRODUCTS P2
        JOIN DOCUMENTS D ON P2.ID = D.CONTRACTOR_FK
        WHERE D.DOCUMENT_TYPE_FK IN (
            SELECT DISTINCT DOCUMENT_TYPE_ID
            FROM DOCUMENT_TYPES
            WHERE DOCUMENT_TYPE_NAME IN ('Zamówienie',     'Faktura',     'Raport') -- Subquery for document types
        )
    )
);