-- Creation of users table
CREATE TABLE IF NOT EXISTS users (
  password varchar(254) NOT NULL,
  username varchar(254) NOT NULL PRIMARY KEY,
  name varchar(254) NOT NULL,
  surname varchar(254) NOT NULL,
  two_factors_login_enabled bool,
  CONSTRAINT 
    proper_email CHECK (username ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$')
);