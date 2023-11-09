UPDATE PRODUCTS P
SET P.PRODUCT_WEIGHT = CASE
                           WHEN P.PRODUCT_WEIGHT > 1.3 * (SELECT AVG(P2.PRODUCT_WEIGHT) FROM PRODUCTS P2)
                               THEN CASE
                                        WHEN P.PRODUCT_WEIGHT * 1.3 > (SELECT AVG(P2.PRODUCT_WEIGHT) FROM PRODUCTS P2)
                                            THEN P.PRODUCT_WEIGHT + (SELECT STDDEV(P2.PRODUCT_WEIGHT) FROM PRODUCTS P2)
                                        ELSE P.PRODUCT_WEIGHT * 1.3
                               END
                           ELSE P.PRODUCT_WEIGHT
    END
WHERE P.ID IN (SELECT PL.PRODUCTS_FK
               FROM PRICE_LISTS PL
               WHERE PL.VALID_DATE BETWEEN SYSDATE - INTERVAL '2' YEAR AND SYSDATE
               GROUP BY PL.PRODUCTS_FK
               HAVING AVG(PL.SALE) > (SELECT AVG(PL2.SALE)
                                      FROM PRICE_LISTS PL2
                                      WHERE PL2.VALID_DATE BETWEEN SYSDATE - INTERVAL '2' YEAR AND SYSDATE));

