-- Insert sample data for a small charity - "Hope Community Center"
-- All transactions follow double-entry bookkeeping (debits = credits for each transaction)

-- Insert realistic Fund data
INSERT INTO Fund (Id, Name, Type) VALUES
(1, "General Operating Fund", "Unrestricted"),
(2, "Building Maintenance Fund", "Restricted"),
(3, "Youth Programs Fund", "Restricted"),
(4, "Emergency Relief Fund", "Restricted"),
(5, "Equipment Replacement Fund", "Restricted");

-- Insert comprehensive Account chart for a charity
INSERT INTO Account (Id, Name, Type) VALUES
-- Assets (1000s)
(1001, "Checking Account", "Current Asset"),
(1002, "Savings Account", "Current Asset"),
(1003, "Petty Cash", "Current Asset"),
(1004, "Accounts Receivable", "Current Asset"),
(1005, "Office Equipment", "Fixed Asset"),
(1006, "Computer Equipment", "Fixed Asset"),
(1007, "Building Improvements", "Fixed Asset"),
(1008, "Vehicles", "Fixed Asset"),

-- Liabilities (2000s)
(2001, "Accounts Payable", "Current Liability"),
(2002, "Credit Card Payable", "Current Liability"),
(2003, "Mortgage Payable", "Long-term Liability"),

-- Income (4000s)
(4001, "Individual Donations", "Income"),
(4002, "Corporate Donations", "Income"),
(4003, "Grant Income", "Income"),
(4004, "Fundraising Events", "Income"),
(4005, "Program Fees", "Income"),
(4006, "Investment Income", "Income"),
(4007, "In-Kind Donations", "Income"),

-- Expenses (5000s)
(5001, "Salaries and Wages", "Expense"),
(5002, "Employee Benefits", "Expense"),
(5003, "Office Rent", "Expense"),
(5004, "Utilities", "Expense"),
(5005, "Office Supplies", "Expense"),
(5006, "Program Supplies", "Expense"),
(5007, "Insurance", "Expense"),
(5008, "Professional Services", "Expense"),
(5009, "Marketing and Outreach", "Expense"),
(5010, "Travel and Transportation", "Expense"),
(5011, "Training and Development", "Expense"),
(5012, "Equipment Maintenance", "Expense"),
(5013, "Fundraising Expenses", "Expense"),
(5014, "Bank Fees", "Expense"),
(5015, "Depreciation", "Expense");

-- Insert realistic transactions with proper double-entry bookkeeping
INSERT INTO Transactions (UserDate, Description) VALUES
-- January 2025
("2025-01-01", "Opening balance transfer from savings"),
("2025-01-03", "Monthly donation - Johnson Family"),
("2025-01-05", "City grant received for youth programs"),
("2025-01-07", "Office rent payment - January"),
("2025-01-10", "Utility bills - electricity and heating"),
("2025-01-12", "Annual fundraising gala proceeds"),
("2025-01-15", "Staff salaries - January first half"),
("2025-01-18", "Office supplies purchase"),
("2025-01-20", "Corporate donation - Local Bank"),
("2025-01-22", "Program supplies for youth center"),
("2025-01-25", "Computer equipment purchase"),
("2025-01-28", "Insurance premium payment"),
("2025-01-30", "Staff salaries - January second half"),

-- February 2025
("2025-02-01", "Emergency relief donation from community"),
("2025-02-03", "Office rent payment - February"),
("2025-02-05", "Valentine's fundraising event"),
("2025-02-07", "Professional services - accounting"),
("2025-02-10", "Utility bills - February"),
("2025-02-12", "Major donor contribution - Smith Foundation"),
("2025-02-15", "Staff salaries - February first half"),
("2025-02-18", "Vehicle maintenance and repairs"),
("2025-02-20", "Marketing materials for spring campaign"),
("2025-02-22", "Training workshop for staff"),
("2025-02-25", "Program fees collected from participants"),
("2025-02-28", "Staff salaries - February second half"),

-- March 2025
("2025-03-01", "Spring fundraising campaign launch"),
("2025-03-03", "Office rent payment - March"),
("2025-03-05", "Building maintenance - HVAC repair"),
("2025-03-07", "Corporate sponsorship - Tech Company"),
("2025-03-10", "Utility bills - March"),
("2025-03-12", "Equipment donation valuation"),
("2025-03-15", "Staff salaries - March first half"),
("2025-03-17", "Travel expenses for conference"),
("2025-03-20", "Office furniture purchase"),
("2025-03-22", "Emergency relief distribution"),
("2025-03-25", "Investment income from endowment"),
("2025-03-28", "Bank fees and service charges"),
("2025-03-30", "Staff salaries - March second half");

-- Insert corresponding Split entries (all transactions balance to zero)

-- Transaction 1: Opening balance transfer ($15,000 from savings to checking)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(1, 15000.00, 1, 1001),    -- Debit Checking Account
(1, -15000.00, 1, 1002);   -- Credit Savings Account

-- Transaction 2: Johnson Family monthly donation ($500)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(2, 500.00, 1, 1001),      -- Debit Checking Account
(2, -500.00, 1, 4001);     -- Credit Individual Donations

-- Transaction 3: City grant for youth programs ($8,000)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(3, 8000.00, 3, 1001),     -- Debit Checking Account (Youth Programs Fund)
(3, -8000.00, 3, 4003);    -- Credit Grant Income

-- Transaction 4: Office rent payment ($1,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(4, 1200.00, 1, 5003),     -- Debit Office Rent
(4, -1200.00, 1, 1001);    -- Credit Checking Account

-- Transaction 5: Utility bills ($385.50)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(5, 385.50, 1, 5004),      -- Debit Utilities
(5, -385.50, 1, 1001);     -- Credit Checking Account

-- Transaction 6: Annual fundraising gala proceeds ($12,500)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(6, 12500.00, 1, 1001),    -- Debit Checking Account
(6, -12000.00, 1, 4004),   -- Credit Fundraising Events
(6, -500.00, 1, 5013);     -- Credit Fundraising Expenses (net of direct costs)

-- Transaction 7: Staff salaries first half January ($3,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(7, 3200.00, 1, 5001),     -- Debit Salaries and Wages
(7, -3200.00, 1, 1001);    -- Credit Checking Account

-- Transaction 8: Office supplies ($175.80)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(8, 175.80, 1, 5005),      -- Debit Office Supplies
(8, -175.80, 1, 1001);     -- Credit Checking Account

-- Transaction 9: Corporate donation from Local Bank ($2,500)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(9, 2500.00, 1, 1001),     -- Debit Checking Account
(9, -2500.00, 1, 4002);    -- Credit Corporate Donations

-- Transaction 10: Program supplies for youth center ($650.25)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(10, 650.25, 3, 5006),     -- Debit Program Supplies (Youth Programs Fund)
(10, -650.25, 3, 1001);    -- Credit Checking Account

-- Transaction 11: Computer equipment purchase ($1,850.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(11, 1850.00, 1, 1006),    -- Debit Computer Equipment
(11, -1850.00, 1, 1001);   -- Credit Checking Account

-- Transaction 12: Insurance premium payment ($890.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(12, 890.00, 1, 5007),     -- Debit Insurance
(12, -890.00, 1, 1001);    -- Credit Checking Account

-- Transaction 13: Staff salaries second half January ($3,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(13, 3200.00, 1, 5001),    -- Debit Salaries and Wages
(13, -3200.00, 1, 1001);   -- Credit Checking Account

-- Transaction 14: Emergency relief donation ($5,000)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(14, 5000.00, 4, 1001),    -- Debit Checking Account (Emergency Relief Fund)
(14, -5000.00, 4, 4001);   -- Credit Individual Donations

-- Transaction 15: February office rent ($1,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(15, 1200.00, 1, 5003),    -- Debit Office Rent
(15, -1200.00, 1, 1001);   -- Credit Checking Account

-- Transaction 16: Valentine's fundraising event ($1,750)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(16, 1750.00, 1, 1001),    -- Debit Checking Account
(16, -1600.00, 1, 4004),   -- Credit Fundraising Events
(16, -150.00, 1, 5013);    -- Credit Fundraising Expenses (net of costs)

-- Transaction 17: Professional services - accounting ($450)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(17, 450.00, 1, 5008),     -- Debit Professional Services
(17, -450.00, 1, 1001);    -- Credit Checking Account

-- Transaction 18: February utility bills ($420.75)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(18, 420.75, 1, 5004),     -- Debit Utilities
(18, -420.75, 1, 1001);    -- Credit Checking Account

-- Transaction 19: Major donor - Smith Foundation ($15,000)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(19, 15000.00, 1, 1001),   -- Debit Checking Account
(19, -15000.00, 1, 4001);  -- Credit Individual Donations

-- Transaction 20: Staff salaries first half February ($3,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(20, 3200.00, 1, 5001),    -- Debit Salaries and Wages
(20, -3200.00, 1, 1001);   -- Credit Checking Account

-- Transaction 21: Vehicle maintenance and repairs ($680.50)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(21, 680.50, 1, 5012),     -- Debit Equipment Maintenance
(21, -680.50, 1, 1001);    -- Credit Checking Account

-- Transaction 22: Marketing materials ($325.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(22, 325.00, 1, 5009),     -- Debit Marketing and Outreach
(22, -325.00, 1, 1001);    -- Credit Checking Account

-- Transaction 23: Training workshop for staff ($275.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(23, 275.00, 1, 5011),     -- Debit Training and Development
(23, -275.00, 1, 1001);    -- Credit Checking Account

-- Transaction 24: Program fees collected ($850.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(24, 850.00, 1, 1001),     -- Debit Checking Account
(24, -850.00, 1, 4005);    -- Credit Program Fees

-- Transaction 25: Staff salaries second half February ($3,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(25, 3200.00, 1, 5001),    -- Debit Salaries and Wages
(25, -3200.00, 1, 1001);   -- Credit Checking Account

-- Transaction 26: Spring fundraising campaign launch ($950.00 expenses)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(26, 950.00, 1, 5013),     -- Debit Fundraising Expenses
(26, -950.00, 1, 1001);    -- Credit Checking Account

-- Transaction 27: March office rent ($1,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(27, 1200.00, 1, 5003),    -- Debit Office Rent
(27, -1200.00, 1, 1001);   -- Credit Checking Account

-- Transaction 28: Building maintenance - HVAC repair ($1,250.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(28, 1250.00, 2, 5012),    -- Debit Equipment Maintenance (Building Fund)
(28, -1250.00, 2, 1001);   -- Credit Checking Account

-- Transaction 29: Corporate sponsorship - Tech Company ($7,500)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(29, 7500.00, 1, 1001),    -- Debit Checking Account
(29, -7500.00, 1, 4002);   -- Credit Corporate Donations

-- Transaction 30: March utility bills ($395.25)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(30, 395.25, 1, 5004),     -- Debit Utilities
(30, -395.25, 1, 1001);    -- Credit Checking Account

-- Transaction 31: Equipment donation valuation ($2,800 in-kind)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(31, 2800.00, 1, 1005),    -- Debit Office Equipment
(31, -2800.00, 1, 4007);   -- Credit In-Kind Donations

-- Transaction 32: Staff salaries first half March ($3,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(32, 3200.00, 1, 5001),    -- Debit Salaries and Wages
(32, -3200.00, 1, 1001);   -- Credit Checking Account

-- Transaction 33: Travel expenses for conference ($785.60)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(33, 785.60, 1, 5010),     -- Debit Travel and Transportation
(33, -785.60, 1, 1001);    -- Credit Checking Account

-- Transaction 34: Office furniture purchase ($650.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(34, 650.00, 1, 1005),     -- Debit Office Equipment
(34, -650.00, 1, 1001);    -- Credit Checking Account

-- Transaction 35: Emergency relief distribution ($3,500)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(35, 3500.00, 4, 5006),    -- Debit Program Supplies (Emergency Relief Fund)
(35, -3500.00, 4, 1001);   -- Credit Checking Account

-- Transaction 36: Investment income from endowment ($125.75)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(36, 125.75, 1, 1001),     -- Debit Checking Account
(36, -125.75, 1, 4006);    -- Credit Investment Income

-- Transaction 37: Bank fees and service charges ($45.00)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(37, 45.00, 1, 5014),      -- Debit Bank Fees
(37, -45.00, 1, 1001);     -- Credit Checking Account

-- Transaction 38: Staff salaries second half March ($3,200)
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(38, 3200.00, 1, 5001),    -- Debit Salaries and Wages
(38, -3200.00, 1, 1001);   -- Credit Checking Account