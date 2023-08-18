CREATE TABLE IF NOT EXISTS otp (
    token varchar(254) NOT NULL,
    username varchar(254) NOT NULL PRIMARY KEY,
    timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);