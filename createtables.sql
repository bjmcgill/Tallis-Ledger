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
    Description TEXT CHECK(length(Description) <= 100),
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
-- Transactions table indexes (excluding primary key Id)
CREATE INDEX idx_transactions_userdate ON Transactions(UserDate);
CREATE INDEX idx_transactions_description ON Transactions(Description);
CREATE INDEX idx_transactions_created_at ON Transactions(Created_at);
CREATE INDEX idx_transactions_deleted ON Transactions(Deleted);
CREATE INDEX idx_transactions_deleted_at ON Transactions(Deleted_at);

-- Split table indexes (excluding primary key Id)
CREATE INDEX idx_split_tran_id ON Split(Tran_id);
CREATE INDEX idx_split_amount ON Split(Amount);
CREATE INDEX idx_split_fund_id ON Split(FundId);
CREATE INDEX idx_split_account_id ON Split(AccountId);

-- Insert default "No Fund" entry
INSERT INTO Fund (Id, Name, Type) VALUES
(0, "No Fund", "SPECIAL");

-- Insert default "No Account" entry
INSERT INTO Account (Id, Name, Type) VALUES
(0, "No Account", "SPECIAL");