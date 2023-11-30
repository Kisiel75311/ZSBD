-- Usuwanie indeksów na PRODUCTS
DROP INDEX idx_products_name
DROP INDEX idx_products_contractor_fk
DROP INDEX idx_products_spec_length

-- Usuwanie indeksów na DOCUMENTS
DROP INDEX idx_documents_date
DROP INDEX idx_documents_contractor_fk
DROP INDEX idx_documents_client_fk
DROP INDEX idx_documents_type_fk

-- Usuwanie indeksów na USERS
DROP INDEX idx_users_warehouse_fk

-- Usuwanie indeksów na PRICE_LISTS
DROP INDEX idx_price_lists_valid_date

-- Usuwanie dodatkowych indeksów złożonych
DROP INDEX idx_documents_client_fk_date
DROP INDEX idx_document_types_abbreviation_id
DROP INDEX idx_products_contractor_fk_length
DROP INDEX idx_price_lists_product_fk_sale
DROP INDEX idx_product_documents_doc_fk_amount

-- Usuwanie indeksów funkcyjnych
DROP INDEX idx_func_products_name
DROP INDEX idx_func_documents_year
DROP INDEX idx_func_products_weight_avg
DROP INDEX idx_func_documents_date_range
DROP INDEX idx_func_product_length_sale

