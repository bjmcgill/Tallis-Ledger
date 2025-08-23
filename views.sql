-- Drop existing views if they exist
DROP VIEW IF EXISTS LedgerView;
DROP VIEW IF EXISTS LedgerViewWithFundBalance;
DROP VIEW IF EXISTS LedgerViewWithAccountBalance;
DROP VIEW IF EXISTS AccountSummaryView;
DROP VIEW IF EXISTS FundSummaryView;
DROP VIEW IF EXISTS AccountTypeSummaryView;

-- Create a comprehensive view for ledger data with formatted choice fields
CREATE VIEW LedgerView AS
SELECT
    Split.Id AS SplitId,
    Transactions.Id AS TransactionsId,
    Transactions.UserDate,
    Transactions.Description,
    Fund.Id || ':' || Fund.Name AS FundChoice,
    Account.Id || ':' || Account.Name AS AccountChoice,
    Split.Amount,
    Fund.Id AS FundId,
    Account.Id AS AccountId
FROM Split
JOIN Transactions ON Split.Tran_id = Transactions.Id
LEFT JOIN Fund ON Split.FundId = Fund.Id
LEFT JOIN Account ON Split.AccountId = Account.Id
WHERE Transactions.Deleted = 0
ORDER BY Transactions.UserDate, Transactions.Id, Split.Id;

CREATE VIEW LedgerViewWithFundBalance AS
SELECT 
    *,
    SUM(Amount) OVER (
        PARTITION BY FundId 
        ORDER BY UserDate, TransactionsId, SplitId 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS Balance
FROM LedgerView 
ORDER BY FundId, UserDate, TransactionsId, SplitId;

CREATE VIEW LedgerViewWithAccountBalance AS
SELECT 
    *,
    SUM(Amount) OVER (
        PARTITION BY AccountId 
        ORDER BY UserDate, TransactionsId, SplitId 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS Balance
FROM LedgerView 
ORDER BY AccountId, UserDate, TransactionsId, SplitId;

CREATE VIEW AccountSummaryView AS
SELECT 
    AccountChoice,
    SUM(Amount) AS TotalAmount
FROM LedgerView 
GROUP BY AccountChoice;

CREATE VIEW FundSummaryView AS
SELECT 
    FundChoice,
    SUM(Amount) AS TotalAmount
FROM LedgerView 
GROUP BY FundChoice;

CREATE VIEW AccountTypeSummaryView AS
SELECT 
    Account.Type AS AccountType,
    SUM(Split.Amount) AS TotalAmount
FROM Split
JOIN Transactions ON Split.Tran_id = Transactions.Id
LEFT JOIN Account ON Split.AccountId = Account.Id
WHERE Transactions.Deleted = 0
GROUP BY Account.Type;

