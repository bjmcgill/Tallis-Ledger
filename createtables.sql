-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Drop tables if they already exist
DROP TABLE IF EXISTS Split;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Fund;
DROP TABLE IF EXISTS Chart;

-- Create Transaction table
CREATE TABLE Transactions (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    UserDate DATE,
    Description TEXT CHECK(length(Description) <= 40),
    Posted BOOLEAN,
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Deleted BOOLEAN DEFAULT 0,
    Deleted_at DATETIME
);

-- Create Fund table
CREATE TABLE Fund (
    Id INTEGER PRIMARY KEY,
    Name TEXT CHECK(length(Name) <= 50),
    Restricted BOOLEAN DEFAULT 0
);

-- Create Chart table
CREATE TABLE Chart (
    Id INTEGER PRIMARY KEY,
    Name TEXT CHECK(length(Name) <= 50),
    ActyType TEXT CHECK(length(ActyType) <= 10)
);

-- Create Split table
CREATE TABLE Split (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Tran_id INTEGER,
    Amount INTEGER,
    FundId INTEGER,
    AccountId INTEGER,
    FOREIGN KEY (Tran_id) REFERENCES Transactions(Id),
    FOREIGN KEY (FundId) REFERENCES Fund(Id),
    FOREIGN KEY (AccountId) REFERENCES Chart(Id)
);

-- Insert sample data into Fund table
INSERT INTO Fund (Id, Name, Restricted) VALUES
(1, "General Fund", 0),
(2, "Building Fund", 1),
(3, "Scholarship Fund", 1);

-- Insert sample data into Chart table
INSERT INTO Chart (Id, Name, ActyType) VALUES
(1, "Cash", "Asset"),
(2, "Donations", "Income"),
(3, "Rent Expense", "Expense");

-- Insert sample data into Transaction table
INSERT INTO Transactions (UserDate, Description, Posted) VALUES
("2025-07-01", "Donation from Alice", 1),
("2025-07-02", "Rent Payment", 1),
("2025-07-03", "Tuition Assistance", 0);

-- Insert sample data into Split table
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(1, 5000, 1, 2),  -- Donation
(2, -1500, 1, 3), -- Rent
(3, 2000, 3, 2),  -- Scholarship donation (unposted)
(1, 3000, 2, 2),  -- Building fund donation
(2, -2000, 2, 3), -- Building fund expense
(3, 1000, 3, 2),  -- Scholarship fund donation
(1, 4000, 1, 2),  -- General fund donation
(2, -2500, 1, 3), -- General fund expense
(3, 1500, 3, 2),  -- Scholarship fund donation
(1, 6000, 2, 2),  -- Building fund donation
(2, -3000, 2, 3), -- Building fund expense
(3, 2500, 3, 2),  -- Scholarship fund donation
(1, 7000, 1, 2),  -- General fund donation
(2, -3500, 1, 3), -- General fund expense
(3, 3000, 3, 2),  -- Scholarship fund donation
(1, 8000, 2, 2),  -- Building fund donation
(2, -4000, 2, 3), -- Building fund expense
(3, 3500, 3, 2),  -- Scholarship fund donation
(1, 9000, 1, 2),  -- General fund donation
(2, -4500, 1, 3), -- General fund expense
(3, 4000, 3, 2),  -- Scholarship fund donation
(1, 10000, 2, 2), -- Building fund donation
(2, -5000, 2, 3), -- Building fund expense
(3, 4500, 3, 2),  -- Scholarship fund donation
(1, 11000, 1, 2), -- General fund donation
(2, -5500, 1, 3), -- General fund expense
(3, 5000, 3, 2),  -- Scholarship fund donation
(1, 12000, 2, 2), -- Building fund donation
(2, -6000, 2, 3), -- Building fund expense
(3, 5500, 3, 2),  -- Scholarship fund donation
(1, 13000, 1, 2), -- General fund donation
(2, -6500, 1, 3), -- General fund expense
(3, 6000, 3, 2),  -- Scholarship fund donation
(1, 14000, 2, 2), -- Building fund donation
(2, -7000, 2, 3), -- Building fund expense
(3, 6500, 3, 2),  -- Scholarship fund donation
(1, 15000, 1, 2), -- General fund donation
(2, -7500, 1, 3), -- General fund expense
(3, 7000, 3, 2),  -- Scholarship fund donation
(1, 16000, 2, 2), -- Building fund donation
(2, -8000, 2, 3), -- Building fund expense
(3, 7500, 3, 2),  -- Scholarship fund donation
(1, 17000, 1, 2), -- General fund donation
(2, -8500, 1, 3), -- General fund expense
(3, 8000, 3, 2);  -- Scholarship fund donation

-- Repeat similar patterns to reach approximately 100 rows
-- ...additional rows can be added similarly...
