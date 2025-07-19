-- Insert sample data into Fund table
INSERT INTO Fund (Id, Name, Type) VALUES
(1, "General Fund", "Unrestricted"),
(2, "Building Fund", "Restricted"),
(3, "Scholarship Fund", "Restricted");

-- Insert sample data into Account table
INSERT INTO Account (Id, Name, Type) VALUES
(1, "Cash", "Asset"),
(2, "Donations", "Income"),
(3, "Rent Expense", "Expense"),
(4, "Checking Account", "Asset"),
(5, "Office Supplies", "Expense"),
(6, "Utilities", "Expense"),
(7, "Program Income", "Income");

-- Insert sample data into Transaction table
INSERT INTO Transactions (UserDate, Description) VALUES
("2025-07-01", "Cash donation from Alice"),
("2025-07-02", "Monthly rent payment"),
("2025-07-03", "Office supplies purchase"),
("2025-07-04", "Program fee collection"),
("2025-07-05", "Utility bill payment"),
("2025-07-06", "Building fund donation"),
("2025-07-07", "Scholarship payment");

-- Insert sample data into Split table (proper double-entry bookkeeping)
-- Transaction 1: Cash donation from Alice - $1000 to General Fund
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(1, 1000, 1, 1),   -- Debit Cash $1000
(1, -1000, 1, 2);  -- Credit Donations $1000

-- Transaction 2: Monthly rent payment - $800 from General Fund
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(2, -800, 1, 4),   -- Credit Checking Account $800
(2, 800, 1, 3);    -- Debit Rent Expense $800

-- Transaction 3: Office supplies purchase - $150 split between funds
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(3, -100, 1, 1),   -- Credit Cash $100 (General Fund portion)
(3, -50, 2, 1),    -- Credit Cash $50 (Building Fund portion)
(3, 150, 1, 5);    -- Debit Office Supplies $150

-- Transaction 4: Program fee collection - $500 to General Fund
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(4, 500, 1, 4),    -- Debit Checking Account $500
(4, -500, 1, 7);   -- Credit Program Income $500

-- Transaction 5: Utility bill payment - $200 from General Fund
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(5, -200, 1, 4),   -- Credit Checking Account $200
(5, 200, 1, 6);    -- Debit Utilities $200

-- Transaction 6: Building fund donation - $2000 cash
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(6, 2000, 2, 1),   -- Debit Cash $2000 (Building Fund)
(6, -2000, 2, 2);  -- Credit Donations $2000 (Building Fund)

-- Transaction 7: Scholarship payment - $750 from Scholarship Fund
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(7, -750, 3, 4),   -- Credit Checking Account $750
(7, 750, 3, 5);    -- Debit Office Supplies $750 (scholarship materials)