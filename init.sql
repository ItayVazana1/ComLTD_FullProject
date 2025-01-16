CREATE DATABASE IF NOT EXISTS com_ltd_protected;
CREATE DATABASE IF NOT EXISTS com_ltd_vulnerable;

CREATE USER IF NOT EXISTS 'backendU_p'@'%' IDENTIFIED BY 'admin';
CREATE USER IF NOT EXISTS 'backendU_v'@'%' IDENTIFIED BY 'admin';

GRANT ALL PRIVILEGES ON com_ltd_protected.* TO 'backendU_p'@'%';
GRANT ALL PRIVILEGES ON com_ltd_vulnerable.* TO 'backendU_v'@'%';

FLUSH PRIVILEGES;
