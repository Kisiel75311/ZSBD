-- Usuń rekordy z PRODUCT_DOCUMENTS, których PRODUCT_FK jest powiązany z PRODUCTS, których nazwa zawiera 'a'
-- i które są powiązane z DOCUMENTS, których DOCUMENT_DATE jest przed lub równy '2022-12-31'
DELETE FROM PRODUCT_DOCUMENTS PC
WHERE PRODUCT_FK IN (
    SELECT P.ID
    FROM PRODUCTS P
    JOIN CONTRACTORS C ON P.CONTRACTOR_FK = C.ID
    WHERE P.NAME LIKE '%a%'
)
AND DOCUMENT_FK IN (
    SELECT D.ID
    FROM DOCUMENTS D
    WHERE D.DOCUMENT_DATE <= TO_DATE('2022-12-31', 'YYYY-MM-DD')
);
