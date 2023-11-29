CREATE INDEX idx_products_contractor_fk ON PRODUCTS (CONTRACTOR_FK)
CREATE INDEX idx_products_name ON PRODUCTS (NAME)
CREATE INDEX idx_products_spec_length ON PRODUCTS (LENGTH(SPECIFICATION))
CREATE INDEX idx_documents_contractor_fk ON DOCUMENTS (CONTRACTOR_FK)
CREATE INDEX idx_documents_client_fk ON DOCUMENTS (CLIENT_FK)
CREATE INDEX idx_documents_type_fk ON DOCUMENTS (DOCUMENT_TYPE_FK)
CREATE INDEX idx_documents_date ON DOCUMENTS (DOCUMENT_DATE)
CREATE INDEX idx_users_warehouse_fk ON USERS (WAREHOUSE_FK)
CREATE INDEX idx_price_lists_valid_date ON PRICE_LISTS (VALID_DATE)