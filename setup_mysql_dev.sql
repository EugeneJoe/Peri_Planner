-- Creates a MySQL server with:
--   Database hbnb_dxev_db.
--   User peri_dev with password peri_dev_pwd in localhost
--   Grants all privileges for peri_dev on peri_dev_db
--   Grants SELECT privilege for peri_dev on performance_schema

CREATE DATABASE IF NOT EXISTS peri_dev_db;

-- Create the user
CREATE USER IF NOT EXISTS 'peri_dev'@'localhost' IDENTIFIED BY 'peri_dev_pwd';

GRANT ALL PRIVILEGES ON peri_dev_db.* TO 'peri_dev'@'localhost';

GRANT SELECT ON performance_schema.* TO 'peri_dev'@'localhost';

FLUSH PRIVILEGES;
