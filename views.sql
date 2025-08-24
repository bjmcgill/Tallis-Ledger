-- Drop existing views if they exist
DROP VIEW IF EXISTS LedgerView;
DROP VIEW IF EXISTS LedgerViewWithFundBalance;
DROP VIEW IF EXISTS LedgerViewWithFundBalance2;
DROP VIEW IF EXISTS LedgerViewWithAccountBalance;
DROP VIEW IF EXISTS LedgerViewWithAccountBalance2;
DROP VIEW IF EXISTS AccountSummaryView;
DROP VIEW IF EXISTS FundSummaryView;
DROP VIEW IF EXISTS AccountTypeSummaryView;

-- Create a comprehensive view for ledger data with formatted choice fields
CREATE VIEW LedgerView AS
SELECT
    Split.Id AS SplitId,
    Transactions.Id AS TransactionsId,
    Transactions.UserDate AS UserDate,
    Transactions.Description AS Description,
    Fund.Id AS FundId,
    Fund.Name AS FundName,
    Fund.Type AS FundType,
    Account.Id AS AccountId,
    Account.Name AS AccountName,
    Account.Type AS AccountType,
    Split.Amount AS Amount
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
    ) AS UFBalance
FROM LedgerView 
ORDER BY FundId, UserDate, TransactionsId, SplitId;

CREATE VIEW LedgerViewWithFundBalance2 AS
SELECT
    SplitId,
    TransactionsId,
    UserDate,
    Description,
    FundId,
    FundName,
    FundType,
    AccountId,
    AccountName,
    AccountType,
    FORMAT("%.2f",Amount) as FAmount,
    FORMAT("%.2f", UFBalance) as Balance
FROM LedgerViewWithFundBalance;

CREATE VIEW LedgerViewWithAccountBalance AS
SELECT 
    *,
    SUM(Amount) OVER (
        PARTITION BY AccountId 
        ORDER BY UserDate, TransactionsId, SplitId 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS UFBalance
FROM LedgerView 
ORDER BY AccountId, UserDate, TransactionsId, SplitId;

CREATE VIEW LedgerViewWithAccountBalance2 AS
SELECT
    SplitId,
    TransactionsId,
    UserDate,
    Description,
    FundId,
    FundName,
    FundType,
    AccountId,
    AccountName,
    AccountType,
    FORMAT("%.2f",Amount) as FAmount,
    FORMAT("%.2f", UFBalance) as Balance
FROM LedgerViewWithAccountBalance;

CREATE VIEW AccountSummaryView AS
SELECT 
    AccountId,
    AccountName,
    AccountType,
    FORMAT("%.2f",SUM(Amount)) AS TotalAmount
FROM LedgerView 
GROUP BY AccountId;

CREATE VIEW FundSummaryView AS
SELECT 
    FundId,
    FundName,
    FundType,
    FORMAT("%.2f",SUM(Amount)) AS TotalAmount
FROM LedgerView 
GROUP BY FundId;

CREATE VIEW AccountTypeSummaryView AS
SELECT 
    Account.Type AS AccountType,
    FORMAT("%.2f",SUM(Split.Amount)) AS TotalAmount
FROM Split
JOIN Transactions ON Split.Tran_id = Transactions.Id
LEFT JOIN Account ON Split.AccountId = Account.Id
WHERE Transactions.Deleted = 0
GROUP BY Account.Type;

