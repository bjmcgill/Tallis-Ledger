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
(7, "Program Income", "Income"),
(8, "Savings Account", "Asset"),
(9, "Equipment", "Asset"),
(10, "Marketing Expense", "Expense"),
(11, "Travel Expense", "Expense"),
(12, "Insurance Expense", "Expense"),
(13, "Professional Services", "Expense"),
(14, "Interest Income", "Income"),
(15, "Grant Income", "Income"),
(16, "Accounts Payable", "Liability"),
(17, "Accounts Receivable", "Asset"),
(18, "Petty Cash", "Asset"),
(19, "Conference Fees", "Expense"),
(20, "Training Expense", "Expense");

-- Insert sample data into Transaction table (50+ transactions for scroll testing)
INSERT INTO Transactions (UserDate, Description) VALUES
("2025-01-01", "Opening balance - Cash"),
("2025-01-02", "January donation - Smith family"),
("2025-01-03", "Office rent payment"),
("2025-01-04", "Equipment purchase"),
("2025-01-05", "Utility bill - electricity"),
("2025-01-06", "Cash donation - community event"),
("2025-01-07", "Office supplies restock"),
("2025-01-08", "Marketing materials"),
("2025-01-09", "Professional consulting"),
("2025-01-10", "Travel reimbursement"),
("2025-01-15", "Large donor contribution"),
("2025-01-16", "Insurance premium payment"),
("2025-01-17", "Training workshop fees"),
("2025-01-18", "Conference registration"),
("2025-01-19", "Petty cash replenishment"),
("2025-01-20", "Grant award received"),
("2025-01-22", "Equipment maintenance"),
("2025-01-23", "Marketing campaign"),
("2025-01-24", "Office supplies"),
("2025-01-25", "Utility bill - water"),
("2025-02-01", "February donation drive"),
("2025-02-02", "Rent payment"),
("2025-02-03", "New equipment"),
("2025-02-04", "Staff training"),
("2025-02-05", "Conference expenses"),
("2025-02-06", "Donation from local business"),
("2025-02-07", "Office equipment repair"),
("2025-02-08", "Marketing materials"),
("2025-02-09", "Professional fees"),
("2025-02-10", "Travel expenses"),
("2025-02-12", "Building fund donation"),
("2025-02-13", "Scholarship payment"),
("2025-02-14", "Valentine's fundraiser"),
("2025-02-15", "Utility payment"),
("2025-02-16", "Office supplies"),
("2025-02-18", "Equipment upgrade"),
("2025-02-19", "Training materials"),
("2025-02-20", "Conference booth"),
("2025-02-21", "Petty cash expense"),
("2025-02-22", "Interest income"),
("2025-03-01", "March campaign kickoff"),
("2025-03-02", "Office rent"),
("2025-03-03", "New computer equipment"),
("2025-03-04", "Staff development"),
("2025-03-05", "Annual conference"),
("2025-03-06", "Major donor gift"),
("2025-03-07", "Equipment lease payment"),
("2025-03-08", "Marketing campaign"),
("2025-03-09", "Consulting services"),
("2025-03-10", "Business travel"),
("2025-03-12", "Building maintenance"),
("2025-03-13", "Scholarship distribution"),
("2025-03-14", "Fundraising event"),
("2025-03-15", "Utility bills"),
("2025-03-16", "Office supplies bulk"),
("2025-03-18", "Technology upgrade"),
("2025-03-19", "Professional development"),
("2025-03-20", "Conference sponsorship"),
("2025-03-21", "Cash management"),
("2025-03-22", "Investment income");

-- Insert comprehensive Split data (proper double-entry bookkeeping)
-- Each transaction will have at least one split involving Cash (Account 1) for scroll testing

-- Transaction 1: Opening balance
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(1, 5000.00, 1, 1),   -- Debit Cash $5000
(1, -5000.00, 1, 8);  -- Credit Savings Account $5000

-- Transaction 2: Smith family donation
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(2, 1500.75, 1, 1),   -- Debit Cash $1500.75
(2, -1500.75, 1, 2);  -- Credit Donations $1500.75

-- Transaction 3: Office rent payment
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(3, -1200.00, 1, 1),  -- Credit Cash $1200
(3, 1200.00, 1, 3);   -- Debit Rent Expense $1200

-- Transaction 4: Equipment purchase
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(4, -800.50, 1, 1),   -- Credit Cash $800.50
(4, 800.50, 1, 9);    -- Debit Equipment $800.50

-- Transaction 5: Utility bill
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(5, -150.25, 1, 1),   -- Credit Cash $150.25
(5, 150.25, 1, 6);    -- Debit Utilities $150.25

-- Transaction 6: Community event donation
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(6, 750.00, 1, 1),    -- Debit Cash $750
(6, -750.00, 1, 2);   -- Credit Donations $750

-- Transaction 7: Office supplies
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(7, -125.80, 1, 1),   -- Credit Cash $125.80
(7, 125.80, 1, 5);    -- Debit Office Supplies $125.80

-- Transaction 8: Marketing materials
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(8, -300.00, 1, 1),   -- Credit Cash $300
(8, 300.00, 1, 10);   -- Debit Marketing Expense $300

-- Transaction 9: Professional consulting
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(9, -450.00, 1, 1),   -- Credit Cash $450
(9, 450.00, 1, 13);   -- Debit Professional Services $450

-- Transaction 10: Travel reimbursement
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(10, -275.50, 1, 1),  -- Credit Cash $275.50
(10, 275.50, 1, 11);  -- Debit Travel Expense $275.50

-- Transaction 11: Large donor contribution
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(11, 5000.00, 1, 1),  -- Debit Cash $5000
(11, -5000.00, 1, 2); -- Credit Donations $5000

-- Transaction 12: Insurance premium
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(12, -600.00, 1, 1),  -- Credit Cash $600
(12, 600.00, 1, 12);  -- Debit Insurance Expense $600

-- Transaction 13: Training workshop
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(13, -250.00, 1, 1),  -- Credit Cash $250
(13, 250.00, 1, 20);  -- Debit Training Expense $250

-- Transaction 14: Conference registration
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(14, -400.00, 1, 1),  -- Credit Cash $400
(14, 400.00, 1, 19);  -- Debit Conference Fees $400

-- Transaction 15: Petty cash replenishment
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(15, -100.00, 1, 1),  -- Credit Cash $100
(15, 100.00, 1, 18);  -- Debit Petty Cash $100

-- Transaction 16: Grant award received
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(16, 3000.00, 2, 1),  -- Debit Cash $3000 (Building Fund)
(16, -3000.00, 2, 15); -- Credit Grant Income $3000

-- Transaction 17: Equipment maintenance
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(17, -180.75, 1, 1),  -- Credit Cash $180.75
(17, 180.75, 1, 9);   -- Debit Equipment $180.75

-- Transaction 18: Marketing campaign
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(18, -650.00, 1, 1),  -- Credit Cash $650
(18, 650.00, 1, 10);  -- Debit Marketing Expense $650

-- Transaction 19: Office supplies
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(19, -85.20, 1, 1),   -- Credit Cash $85.20
(19, 85.20, 1, 5);    -- Debit Office Supplies $85.20

-- Transaction 20: Water utility
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(20, -75.60, 1, 1),   -- Credit Cash $75.60
(20, 75.60, 1, 6);    -- Debit Utilities $75.60

-- Transaction 21: February donation drive
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(21, 2200.00, 1, 1),  -- Debit Cash $2200
(21, -2200.00, 1, 2); -- Credit Donations $2200

-- Transaction 22: February rent
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(22, -1200.00, 1, 1), -- Credit Cash $1200
(22, 1200.00, 1, 3);  -- Debit Rent Expense $1200

-- Transaction 23: New equipment
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(23, -1500.00, 2, 1), -- Credit Cash $1500 (Building Fund)
(23, 1500.00, 2, 9);  -- Debit Equipment $1500

-- Transaction 24: Staff training
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(24, -350.00, 1, 1),  -- Credit Cash $350
(24, 350.00, 1, 20);  -- Debit Training Expense $350

-- Transaction 25: Conference expenses
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(25, -800.00, 1, 1),  -- Credit Cash $800
(25, 800.00, 1, 19);  -- Debit Conference Fees $800

-- Continue with remaining transactions (26-60) for extensive scroll testing
-- Transaction 26: Local business donation
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(26, 1800.00, 1, 1),  -- Debit Cash $1800
(26, -1800.00, 1, 2); -- Credit Donations $1800

-- Transaction 27: Equipment repair
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(27, -220.50, 1, 1),  -- Credit Cash $220.50
(27, 220.50, 1, 9);   -- Debit Equipment $220.50

-- Transaction 28: Marketing materials
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(28, -425.00, 1, 1),  -- Credit Cash $425
(28, 425.00, 1, 10);  -- Debit Marketing Expense $425

-- Transaction 29: Professional fees
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(29, -750.00, 1, 1),  -- Credit Cash $750
(29, 750.00, 1, 13);  -- Debit Professional Services $750

-- Transaction 30: Travel expenses
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(30, -320.80, 1, 1),  -- Credit Cash $320.80
(30, 320.80, 1, 11);  -- Debit Travel Expense $320.80

-- Transaction 31: Building fund donation
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(31, 4000.00, 2, 1),  -- Debit Cash $4000 (Building Fund)
(31, -4000.00, 2, 2); -- Credit Donations $4000

-- Transaction 32: Scholarship payment
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(32, -1200.00, 3, 1), -- Credit Cash $1200 (Scholarship Fund)
(32, 1200.00, 3, 20); -- Debit Training Expense $1200

-- Transaction 33: Valentine's fundraiser
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(33, 850.00, 1, 1),   -- Debit Cash $850
(33, -850.00, 1, 7);  -- Credit Program Income $850

-- Transaction 34: Utility payment
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(34, -195.40, 1, 1),  -- Credit Cash $195.40
(34, 195.40, 1, 6);   -- Debit Utilities $195.40

-- Transaction 35: Office supplies
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(35, -140.75, 1, 1),  -- Credit Cash $140.75
(35, 140.75, 1, 5);   -- Debit Office Supplies $140.75

-- Transaction 36: Equipment upgrade
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(36, -900.00, 2, 1),  -- Credit Cash $900 (Building Fund)
(36, 900.00, 2, 9);   -- Debit Equipment $900

-- Transaction 37: Training materials
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(37, -180.00, 1, 1),  -- Credit Cash $180
(37, 180.00, 1, 20);  -- Debit Training Expense $180

-- Transaction 38: Conference booth
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(38, -1200.00, 1, 1), -- Credit Cash $1200
(38, 1200.00, 1, 19); -- Debit Conference Fees $1200

-- Transaction 39: Petty cash expense
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(39, -50.00, 1, 18),  -- Credit Petty Cash $50
(39, 50.00, 1, 5);    -- Debit Office Supplies $50

-- Transaction 40: Interest income
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(40, 25.50, 1, 1),    -- Debit Cash $25.50
(40, -25.50, 1, 14);  -- Credit Interest Income $25.50

-- Continue with March transactions (41-60)
-- Transaction 41: March campaign kickoff
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(41, 3500.00, 1, 1),  -- Debit Cash $3500
(41, -3500.00, 1, 2); -- Credit Donations $3500

-- Transaction 42: March rent
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(42, -1200.00, 1, 1), -- Credit Cash $1200
(42, 1200.00, 1, 3);  -- Debit Rent Expense $1200

-- Transaction 43: Computer equipment
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(43, -2500.00, 2, 1), -- Credit Cash $2500 (Building Fund)
(43, 2500.00, 2, 9);  -- Debit Equipment $2500

-- Transaction 44: Staff development
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(44, -450.00, 1, 1),  -- Credit Cash $450
(44, 450.00, 1, 20);  -- Debit Training Expense $450

-- Transaction 45: Annual conference
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(45, -1500.00, 1, 1), -- Credit Cash $1500
(45, 1500.00, 1, 19); -- Debit Conference Fees $1500

-- Transaction 46: Major donor gift
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(46, 10000.00, 1, 1), -- Debit Cash $10000
(46, -10000.00, 1, 2); -- Credit Donations $10000

-- Transaction 47: Equipment lease
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(47, -600.00, 1, 1),  -- Credit Cash $600
(47, 600.00, 1, 9);   -- Debit Equipment $600

-- Transaction 48: Marketing campaign
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(48, -800.00, 1, 1),  -- Credit Cash $800
(48, 800.00, 1, 10);  -- Debit Marketing Expense $800

-- Transaction 49: Consulting services
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(49, -950.00, 1, 1),  -- Credit Cash $950
(49, 950.00, 1, 13);  -- Debit Professional Services $950

-- Transaction 50: Business travel
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(50, -485.75, 1, 1),  -- Credit Cash $485.75
(50, 485.75, 1, 11);  -- Debit Travel Expense $485.75

-- Transaction 51: Building maintenance
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(51, -350.00, 2, 1),  -- Credit Cash $350 (Building Fund)
(51, 350.00, 2, 3);   -- Debit Rent Expense $350

-- Transaction 52: Scholarship distribution
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(52, -1500.00, 3, 1), -- Credit Cash $1500 (Scholarship Fund)
(52, 1500.00, 3, 20); -- Debit Training Expense $1500

-- Transaction 53: Fundraising event
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(53, 2750.00, 1, 1),  -- Debit Cash $2750
(53, -2750.00, 1, 7); -- Credit Program Income $2750

-- Transaction 54: Utility bills
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(54, -280.90, 1, 1),  -- Credit Cash $280.90
(54, 280.90, 1, 6);   -- Debit Utilities $280.90

-- Transaction 55: Office supplies bulk
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(55, -450.00, 1, 1),  -- Credit Cash $450
(55, 450.00, 1, 5);   -- Debit Office Supplies $450

-- Transaction 56: Technology upgrade
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(56, -1800.00, 2, 1), -- Credit Cash $1800 (Building Fund)
(56, 1800.00, 2, 9);  -- Debit Equipment $1800

-- Transaction 57: Professional development
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(57, -320.00, 1, 1),  -- Credit Cash $320
(57, 320.00, 1, 20);  -- Debit Training Expense $320

-- Transaction 58: Conference sponsorship
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(58, -2000.00, 1, 1), -- Credit Cash $2000
(58, 2000.00, 1, 19); -- Debit Conference Fees $2000

-- Transaction 59: Cash management
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(59, -500.00, 1, 1),  -- Credit Cash $500
(59, 500.00, 1, 8);   -- Debit Savings Account $500

-- Transaction 60: Investment income
INSERT INTO Split (Tran_id, Amount, FundId, AccountId) VALUES
(60, 75.25, 1, 1),    -- Debit Cash $75.25
(60, -75.25, 1, 14);  -- Credit Interest Income $75.25