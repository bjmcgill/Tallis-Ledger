-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Drop tables if they already exist
DROP TABLE IF EXISTS Split;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Fund;
DROP TABLE IF EXISTS Account;

-- Create Transaction table
CREATE TABLE Transactions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserDate DATE,
    Description TEXT CHECK(length(Description) <= 40),
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Deleted BOOLEAN DEFAULT 0,
    Deleted_at DATETIME
);

-- Create Fund table
CREATE TABLE Fund (
    Id INTEGER PRIMARY KEY,
    Name TEXT CHECK(length(Name) <= 50),
    Type TEXT CHECK(length(Type) <= 25)
);

-- Create Account table
CREATE TABLE Account (
    Id INTEGER PRIMARY KEY,
    Name TEXT CHECK(length(Name) <= 50),
    Type TEXT CHECK(length(Type) <= 25)
);

-- Create Split table
CREATE TABLE Split (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Tran_id INTEGER,
    Amount REAL,
    FundId INTEGER,
    AccountId INTEGER,
    FOREIGN KEY (Tran_id) REFERENCES Transactions(Id),
    FOREIGN KEY (FundId) REFERENCES Fund(Id),
    FOREIGN KEY (AccountId) REFERENCES Account(Id)
);

-- Create indexes for performance
CREATE INDEX idx_split_tran_id ON Split(Tran_id);
CREATE INDEX idx_transactions_userdate ON Transactions(UserDate);

-- Insert default "No Fund" entry
INSERT INTO Fund (Id, Name, Type) VALUES
(0, "No Fund", "SPECIAL");

-- Insert default "No Account" entry
INSERT INTO Account (Id, Name, Type) VALUES
(0, "No Account", "SPECIAL");