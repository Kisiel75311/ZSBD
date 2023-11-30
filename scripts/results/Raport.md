# Dokumentacja Wolumetrii - Obieg Dokumentów Grupa 2 ZSBD
Data: 30.11.2023

## Skład Grupy
- Joanna Wdziękońska
- Ivan Tarasiuk
- Szymon Kisiela

## Laboratorium
Lab 7 – Indeksy (dev)

## Repozytorium
[GitHub - ZSBD](https://github.com/Kisiel75311/ZSBD)

## Propozycje indeksów wraz z krótim opisem

```sql
-- Indeksy na PRODUCTS

-- Indeks B-tree na nazwę produktu, optymalizuje zapytania z filtrowaniem po nazwie
CREATE INDEX idx_products_name ON PRODUCTS (NAME);

-- Indeks B-tree na klucz obcy CONTRACTOR_FK, optymalizuje zapytania łączące PRODUCTS z CONTRACTORS
CREATE INDEX idx_products_contractor_fk ON PRODUCTS (CONTRACTOR_FK);

-- Indeks funkcyjny na długość specyfikacji, użyteczny przy filtrowaniu produktów na podstawie długości specyfikacji
CREATE INDEX idx_products_spec_length ON PRODUCTS (LENGTH(SPECIFICATION));

-- Indeksy na DOCUMENTS

-- Indeks B-tree na datę dokumentu, optymalizuje zapytania z filtrowaniem po dacie
CREATE INDEX idx_documents_date ON DOCUMENTS (DOCUMENT_DATE);

-- Indeks B-tree na klucz obcy CONTRACTOR_FK, optymalizuje zapytania łączące DOCUMENTS z CONTRACTORS
CREATE INDEX idx_documents_contractor_fk ON DOCUMENTS (CONTRACTOR_FK);

-- Indeks B-tree na klucz obcy CLIENT_FK, optymalizuje zapytania łączące DOCUMENTS z USERS
CREATE INDEX idx_documents_client_fk ON DOCUMENTS (CLIENT_FK);

-- Indeks B-tree na klucz obcy DOCUMENT_TYPE_FK, optymalizuje zapytania łączące DOCUMENTS z DOCUMENT_TYPES
CREATE INDEX idx_documents_type_fk ON DOCUMENTS (DOCUMENT_TYPE_FK);

-- Indeksy na USERS

-- Indeks B-tree na klucz obcy WAREHOUSE_FK, optymalizuje zapytania łączące USERS z WAREHOUSES
CREATE INDEX idx_users_warehouse_fk ON USERS (WAREHOUSE_FK);

-- Indeksy na PRICE_LISTS

-- Indeks B-tree na datę ważności cennika, optymalizuje zapytania z filtrowaniem po dacie ważności
CREATE INDEX idx_price_lists_valid_date ON PRICE_LISTS (VALID_DATE);

-- Dodatkowe indeksy złożone

-- Złożony indeks B-tree na CLIENT_FK i DOCUMENT_DATE w DOCUMENTS, optymalizuje zapytania
CREATE INDEX idx_documents_client_fk_date ON DOCUMENTS (CLIENT_FK, DOCUMENT_DATE);

-- Indeks B-tree na DOCUMENT_TYPES.ABBREVIATION i DOCUMENT_TYPES.ID, optymalizuje zapytania
CREATE INDEX idx_document_types_abbreviation_id ON DOCUMENT_TYPES (ABBREVIATION, ID);

-- Złożony indeks B-tree na PRODUCTS.CONTRACTOR_FK i PRODUCTS.PRODUCT_LENGTH, optymalizuje zapytania
CREATE INDEX idx_products_contractor_fk_length ON PRODUCTS (CONTRACTOR_FK, PRODUCT_LENGTH);

-- Indeks B-tree na PRICE_LISTS.PRODUCTS_FK i PRICE_LISTS.SALE, optymalizuje zapytania
CREATE INDEX idx_price_lists_product_fk_sale ON PRICE_LISTS (PRODUCTS_FK, SALE);

-- Indeks B-tree na PRODUCT_DOCUMENTS.DOCUMENT_FK i PRODUCT_DOCUMENTS.AMOUNT, optymalizuje zapytania
CREATE INDEX idx_product_documents_doc_fk_amount ON PRODUCT_DOCUMENTS (DOCUMENT_FK, AMOUNT);

-- Indeks funkcyjny na PRODUCTS.NAME dla porównań z LIKE '%a%', optymalizuje zapytania
CREATE INDEX idx_func_products_name ON PRODUCTS (LOWER(NAME));

-- Indeks funkcyjny na rok z DOCUMENTS.DOCUMENT_DATE, optymalizuje zapytania
CREATE INDEX idx_func_documents_year ON DOCUMENTS (EXTRACT(YEAR FROM DOCUMENT_DATE));

-- Indeks funkcyjny na DOCUMENT_DATE w zakresie dat, optymalizuje zapytania
CREATE INDEX idx_func_documents_date_range ON DOCUMENTS (CASE
                                                             WHEN DOCUMENT_DATE BETWEEN TO_DATE('2020-01-01', 'YYYY-MM-DD') AND TO_DATE('2022-12-31', 'YYYY-MM-DD')
                                                                 THEN 1
                                                             ELSE 0 END);



```

## Porówanie z indeksami typu BITMAP
Każdy z powyższych indeksów został zaimplementowany również w wersji BITMAP. Poniżej przedstawiono wyniki pomiarów czasu wykonania zapytań dla obu typów indeksów.


## Wyniki pomiarów dla zapytań bez indeksów, z indeksami i z indeksami typu BITMAP

W tabelch przedstawione są wyniki pomiarów czasów oraz kosztów (tab1), a także różnica czasów i kosztów pomiędzy indeksami a brakiem indeksów oraz różnice pomiędzy danymi typami indeksów (tab2).
### Tabela 1
| Script   |   Min Time (ms) |   Max Time (ms) |   Avg Time (ms) |   INDEX Min Time (ms) |   INDEX Max Time (ms) |   INDEX Avg Time (ms) |   BITMAP INDEX Min Time (ms) |   BITMAP INDEX Max Time (ms) |   BITMAP INDEX Avg Time (ms) |   Cost (none) |   Cost (INDEX) |   Cost (BITMAP INDEX) |
|:---------|----------------:|----------------:|----------------:|----------------------:|----------------------:|----------------------:|-----------------------------:|-----------------------------:|-----------------------------:|--------------:|---------------:|----------------------:|
| 1.sql    |        11288.1  |        15838.3  |        12837.9  |               1515.1  |              13757    |             11817.6   |                      2026.28 |                     15859.8  |                    13121     |         14816 |          14816 |                 14816 |
| 2.sql    |         2005.95 |         3662.96 |         2436.26 |                227.94 |                731.75 |               370.143 |                       191.96 |                       249.76 |                      218.704 |         20918 |           4669 |                  5888 |
| 3.sql    |         1775.57 |         2170.26 |         1974.28 |                502.53 |                613.05 |               549.371 |                       569.78 |                       810.7  |                      699.093 |         22606 |           1724 |                  3181 |
| 4.sql    |         1539    |         1868.57 |         1682.84 |                 36.7  |                 71.52 |                52.082 |                        36.19 |                        79.69 |                       53.443 |         20125 |           1311 |                  1892 |
| 6.sql    |         4049.39 |         4387.52 |         4255.26 |               4221.64 |               5466.82 |              4681.95  |                      3697.35 |                      5825.16 |                     4344.41  |        236000 |         236000 |                236000 |
| 7.sql    |         9695.13 |        12114.2  |        10784.4  |                  6.84 |                 23.44 |                12.593 |                         7.81 |                        23.16 |                       11.895 |        117000 |          10355 |                 10629 |
| 8.sql    |         1950.32 |         2480.2  |         2139.91 |                272.53 |                418.62 |               351.268 |                       369.21 |                       557.27 |                      440.651 |         21914 |           3769 |                  4891 |
| 9.sql    |         1554.02 |         1760.48 |         1635.76 |               1663.75 |               2623.34 |              2073.66  |                      1633.59 |                      2559.05 |                     1871.73  |         11389 |          11389 |                 11389 |
| 91.sql   |           11.72 |           26.4  |           15.81 |                 18.59 |                 29.87 |                23.605 |                        17.58 |                        33.81 |                       24.584 |         16681 |           5372 |                  5146 |

### Tabela 2
| Script   |   Diff Avg Time (ms) (INDEX - Original) |   Diff Avg Time (ms) (BITMAP INDEX - Original) |   Diff Avg Time (ms) (BITMAP INDEX - INDEX) |   Diff Cost (INDEX - none) |   Diff Cost (BITMAP INDEX - none) |   Diff Cost (BITMAP INDEX - INDEX) |
|:---------|----------------------------------------:|-----------------------------------------------:|--------------------------------------------:|---------------------------:|----------------------------------:|-----------------------------------:|
| 1.sql    |                               -1020.33  |                                        283.094 |                                    1303.42  |                        0 |                                 0 |                                  0 |
| 2.sql    |                               -2066.12  |                                      -2217.56  |                                    -151.439 |                    -16249 |                            -15030 |                               1219 |
| 3.sql    |                               -1424.91  |                                      -1275.18  |                                     149.722 |                    -20882 |                            -19425 |                               1457 |
| 4.sql    |                               -1630.76  |                                      -1629.4   |                                       1.361 |                    -18814 |                            -18233 |                                581 |
| 6.sql    |                                 426.69  |                                         89.152 |                                    -337.538 |                        0 |                                 0 |                                  0 |
| 7.sql    |                              -10771.8   |                                     -10772.5   |                                      -0.698 |                   -106645 |                           -106371 |                                274 |
| 8.sql    |                               -1788.65  |                                      -1699.26  |                                      89.383 |                    -18145 |                            -17023 |                               1122 |
| 9.sql    |                                 437.897 |                                        235.971 |                                    -201.926 |                        0 |                                 0 |                                  0 |
| 91.sql   |                                   7.795 |                                          8.774 |                                       0.979 |                    -11309 |                            -11535 |                               -226 |


## Wnioski na podstawie tabel

- **Zastosowanie Indeksów:** Użycie indeksów w większości przypadków znacznie poprawia wydajność zapytań, co widać w zmniejszeniu średniego czasu wykonania. Widać to szczególnie w skryptach, gdzie czas wykonania z indeksami jest znacząco krótszy w porównaniu z czasem bez indeksów.

- **Porównanie Typów Indeksów:** Różnice w wydajności między indeksami typu B-tree a indeksami bitmapowymi są zróżnicowane. W niektórych przypadkach indeksy bitmapowe mają lepszy średni czas wykonania, ale nie zawsze są lepsze od indeksów B-tree. Wynika z tego, że wybór typu indeksu powinien być dokonywany indywidualnie dla każdego zapytania.

- **Koszt Optymalizacji:** Indeksy mogą znacząco obniżyć koszt wykonania zapytań, co widać w porównaniach kosztów. W niektórych przypadkach, koszty zostały zredukowane o ponad połowę dzięki zastosowaniu indeksów.

- **Wyjątki w Wynikach:** Zdarzają się przypadki, gdzie zastosowanie indeksów nie przynosi znaczącej poprawy lub nawet pogarsza wydajność (na przykład 6.sql i 9.sql). To podkreśla potrzebę indywidualnej analizy i testowania przed zastosowaniem indeksów.

## Wyniki porównań planów wykonania zapytań
Ze względu na duży rozmiar planów wykonania zapytań, zostały one umieszczone w .zip, który dołączony jest do raportu. Format plików pdf pozwala na łatwie przeglądanie.