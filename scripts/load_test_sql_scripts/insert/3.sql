INSERT INTO WAREHOUSE_COMPANY (WAREHOUSE_ID, COMPANY_ID)
SELECT w.ID AS WAREHOUSE_ID,
       c.ID AS COMPANY_ID
FROM (SELECT w.ID, w.TotalCurrentCompanies, n.TargetAverage
      FROM (SELECT w.ID, COUNT(wc.COMPANY_ID) AS TotalCurrentCompanies
            FROM WAREHOUSES w
                     LEFT JOIN WAREHOUSE_COMPANY wc ON w.ID = wc.WAREHOUSE_ID
            GROUP BY w.ID) w
               CROSS JOIN (SELECT (COUNT(*) / COUNT(DISTINCT WAREHOUSE_ID)) * 1.4 AS TargetAverage
                           FROM WAREHOUSE_COMPANY) n
      WHERE w.TotalCurrentCompanies < n.TargetAverage) w
         CROSS JOIN (SELECT ID
                     FROM COMPANIES
                     ORDER BY DBMS_RANDOM.VALUE) c
WHERE ROWNUM <= (SELECT CEIL(SUM(n.TargetAverage - w.TotalCurrentCompanies))
                 FROM (SELECT w.ID, COUNT(wc.COMPANY_ID) AS TotalCurrentCompanies
                       FROM WAREHOUSES w
                                LEFT JOIN WAREHOUSE_COMPANY wc ON w.ID = wc.WAREHOUSE_ID
                       GROUP BY w.ID) w
                          CROSS JOIN (SELECT (COUNT(*) / COUNT(DISTINCT WAREHOUSE_ID)) * 1.4 AS TargetAverage
                                      FROM WAREHOUSE_COMPANY) n
                 WHERE w.TotalCurrentCompanies < n.TargetAverage);
