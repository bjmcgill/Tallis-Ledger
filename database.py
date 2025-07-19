"""
Database management module for Tallis Ledger.
Handles all SQLite database operations and queries.
"""

import sqlite3
import pandas as pd


class DatabaseManager:
    """Handles all SQLite database operations and queries."""
    
    def __init__(self, db_path="your_ledger.db"):
        """Initialize database connection with foreign key support."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
    
    # ========== LOOKUP QUERIES ==========
    
    def fetch_chart_options(self):
        """Fetch all account entries for dropdown selection."""
        query = "SELECT Id, Name FROM Account ORDER BY Id"
        return pd.read_sql_query(query, self.conn)
    
    def fetch_fund_options(self):
        """Fetch all fund entries for dropdown selection."""
        query = "SELECT Id, Name FROM Fund ORDER BY Id"
        return pd.read_sql_query(query, self.conn)
    
    # ========== TRANSACTION QUERIES ==========
    
    def fetch_ledger_data(self, filter_id, filter_type='account'):
        """Fetch ledger data filtered by account or fund with formatted choice fields."""
        if filter_type == 'account':
            filter_clause = "Account.Id = ?"
        elif filter_type == 'fund':
            filter_clause = "Fund.Id = ?"
        else:
            raise ValueError("filter_type must be 'account' or 'fund'")
            
        query = f"""
            SELECT
                Split.Id AS SplitId,
                Transactions.Id AS TransactionsId,
                Transactions.UserDate,
                Transactions.Description,
                Fund.Id || ':' || Fund.Name AS FundChoice,
                Account.Id || ':' || Account.Name AS AccountChoice,
                Split.Amount
            FROM Split
            JOIN Transactions ON Split.Tran_id = Transactions.Id
            LEFT JOIN Fund ON Split.FundId = Fund.Id
            LEFT JOIN Account ON Split.AccountId = Account.Id
            WHERE Transactions.Deleted = 0 AND {filter_clause}
            ORDER BY Transactions.UserDate, Transactions.Id, Split.Id
        """
        return pd.read_sql_query(query, self.conn, params=[filter_id])
    
    def fetch_transaction_data(self, tran_id):
        """Fetch all splits for a specific transaction with formatted choice fields."""
        query = """
            SELECT
                Split.Id AS SplitId,
                Transactions.Id AS TransactionsId,
                Transactions.UserDate,
                Transactions.Description,
                Fund.Id || ':' || Fund.Name AS FundChoice,
                Account.Id || ':' || Account.Name AS AccountChoice,
                Split.Amount
            FROM Split
            JOIN Transactions ON Split.Tran_id = Transactions.Id
            LEFT JOIN Fund ON Split.FundId = Fund.Id
            LEFT JOIN Account ON Split.AccountId = Account.Id
            WHERE Transactions.Deleted = 0 AND Split.Tran_id = ?
            ORDER BY Transactions.UserDate, Transactions.Id, Split.Id
        """
        return pd.read_sql_query(query, self.conn, params=[tran_id])
    
    # ========== TRANSACTION UPDATES ==========
    
    def save_transaction(self, tran_id, user_date, description, splits_data):
        """
        Save a transaction and its splits to the database.
        
        Args:
            tran_id: Transaction ID
            user_date: Transaction date
            description: Transaction description
            splits_data: List of dicts with keys: amount, fund_id, account_id
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Begin transaction
            self.conn.execute("BEGIN")
            
            # Delete existing data for this transaction
            self._delete_transaction_data(tran_id)
            
            # Insert new transaction
            new_tran_id = self._insert_transaction(user_date, description)
            
            # Insert new splits
            self._insert_splits(new_tran_id, splits_data)
            
            # Commit the transaction
            self.conn.commit()
            return True
            
        except Exception as e:
            # Rollback on error
            self.conn.rollback()
            print(f"Error saving transaction: {e}")
            return False
    
    def _delete_transaction_data(self, tran_id):
        """Mark transaction as deleted with soft deletion (leaves splits intact)."""
        self.cursor.execute("""
            UPDATE Transactions 
            SET Deleted = 1, Deleted_at = CURRENT_TIMESTAMP 
            WHERE Id = ?
        """, (tran_id,))
    
    def _insert_transaction(self, user_date, description):
        """Insert a new transaction record and return the new ID."""
        self.cursor.execute("""
            INSERT INTO Transactions (UserDate, Description, Created_at, Deleted) 
            VALUES (?, ?, CURRENT_TIMESTAMP, 0)
        """, (user_date, description))
        return self.cursor.lastrowid
    
    def _insert_splits(self, tran_id, splits_data):
        """Insert splits for the given transaction."""
        for split in splits_data:
            self.cursor.execute("""
                INSERT INTO Split (Tran_id, Amount, FundId, AccountId) 
                VALUES (?, ?, ?, ?)
            """, (tran_id, split['amount'], split['fund_id'], split['account_id']))
    
    # ========== CONNECTION MANAGEMENT ==========
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()