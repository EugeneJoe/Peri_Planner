-- Prepares a MySQL test server for the project

-- Creates the database
CREATE DATABASE IF NOT EXISTS peri_dev_db;

CREATE USER IF NOT EXISTS 'peri_test'@'localhost' IDENTIFIED BY 'peri_test_pwd';

GRANT ALL PRIVILEGES ON peri_test_db.* TO 'peri_test'@'localhost';

GRANT SELECT ON performance_schema.* TO 'peri_test'@'localhost';

FLUSH PRIVILEGES;
