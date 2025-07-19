# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

Tallis Ledger is a Tkinter-based accounting application that provides a spreadsheet-like interface for managing financial transactions. The application uses SQLite as its database and the tksheet library for the interactive data grid.

### Core Architecture

The application follows a modular architecture with clear separation of concerns:

**Module Structure:**
- **`main.py`**: Application entry point
- **`application.py`**: Main Application class coordinating all components
- **`database.py`**: DatabaseManager class for all SQLite operations
- **`ui_components.py`**: ChartSelector and EditModeManager classes
- **`ledger_sheet.py`**: LedgerSheet class wrapping tksheet widget

**Key Classes:**
- **DatabaseManager**: Handles all SQLite database operations and queries
- **ChartSelector**: Manages the account dropdown selection widget
- **EditModeManager**: Controls the edit mode UI state and buttons
- **LedgerSheet**: Wraps the tksheet widget and handles data display
- **Application**: Main controller that coordinates all components

### Database Schema

The application uses a double-entry accounting system with these key tables:

- **Transactions**: Main transaction records with date, description, and posting status
- **Split**: Individual accounting entries that implement double-entry bookkeeping
- **Account**: Chart of accounts with Id, Name, and Type fields (assets, liabilities, income, expenses)
- **Fund**: Fund accounting with Id, Name, and Type fields for tracking different fund types

**Default Records:**
- Account table includes a default "No Account" entry (ID=0, Type="Default") for unassigned transactions
- Fund table includes a default "No Fund" entry (ID=0, Type="Default") for unassigned funds

**Performance Indexes:**
- `idx_split_tran_id` on Split.Tran_id for efficient transaction joins
- `idx_transactions_userdate` on Transactions.UserDate for date-based queries

## Common Development Commands

### Running the Application
```bash
python main.py
```

### Setting Up the Database
```bash
# Create tables
sqlite3 your_ledger.db < createtables.sql

# Insert sample data
sqlite3 your_ledger.db < insertdata.sql
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Key Dependencies

- **tksheet**: Spreadsheet widget for data display and editing
- **pandas**: Data manipulation and SQL query results
- **sqlite3**: Database operations (built-in)
- **tkinter**: GUI framework (built-in)

## Working with the Code

### Modular Structure
- Each module has a single responsibility and clear interfaces
- Import modules using `from module_name import ClassName`
- The Application class in `application.py` coordinates all components
- Database operations are isolated in `database.py` for easy testing

### Database Operations
- All database interactions go through the `DatabaseManager` class in `database.py`
- The application maintains foreign key constraints
- Use parameterized queries to prevent SQL injection
- The database file is `your_ledger.db` by default

### UI Components
- UI widgets are organized in `ui_components.py` and `ledger_sheet.py`
- The main data grid uses tksheet - refer to `tksheet_reference.md` for detailed API
- The application has two modes: "initial" (read-only) and "edit" (editable)
- Edit mode is triggered by clicking on a cell and shows action buttons
- The account selector filters the ledger display by account
- All columns from database queries are displayed dynamically (no hardcoded column filtering)

### Display Modes
**Initial Mode:**
- Shows all transaction data with a calculated Balance column (cumulative sum of amounts)
- All rows are readonly and highlighted in white
- Account dropdown selector is enabled

**Edit Mode:**
- Removes the Balance column to focus on editable data
- Selected transaction splits are highlighted in red and made editable
- Account dropdown is disabled during editing
- AccountChoice column features dropdown selection for account assignment
- FundChoice column features dropdown selection for fund assignment
- Both dropdowns are initialized with current values and ordered by ID
- Save and Cancel buttons are available for transaction management
- All other rows remain readonly

### Data Flow
1. User selects an account from the dropdown
2. `fetch_ledger_data()` retrieves transactions for that account
3. Data is displayed in the tksheet grid with Balance column added
4. User clicks on a transaction row to enter edit mode
5. System fetches all splits for that transaction using `fetch_transaction_data()`
6. Edit mode displays transaction splits with account and fund dropdowns, removes Balance column
7. User can modify transaction data, account assignments, and fund assignments
8. User clicks Save to persist changes or Cancel to discard changes
9. On save, data is validated and written to database using `save_transaction()`
10. On cancel/save completion, Balance column is restored and normal view is resumed

### Event Handling
- Cell selection triggers edit mode entry
- Edit mode shows Cancel/Save/Delete buttons
- The application tracks the selected row and transaction ID for edit operations
- Readonly spans prevent editing of non-selected rows
- Account and fund dropdown functionality is dynamically applied to editable rows
- Dropdowns are initialized with current values from database
- Red highlighting indicates editable transaction splits
- Save button persists changes to database with full transaction replacement
- Cancel button discards changes and restores original view

## Code Patterns

### Adding New Database Queries
```python
# In database.py - DatabaseManager class
def fetch_new_data(self, param):
    query = """
        SELECT column1, column2
        FROM table_name
        WHERE condition = ?
    """
    return pd.read_sql_query(query, self.conn, params=[param])
```

### Working with tksheet
```python
# In ledger_sheet.py - LedgerSheet class
# Update sheet data with dynamic headers
def update_data(self, account_id, include_balance=True):
    full_df = self.db_manager.fetch_ledger_data(account_id)
    if include_balance:
        full_df['Balance'] = full_df['Amount'].cumsum()
    self.sheet.headers(list(full_df.columns))
    self.sheet.set_sheet_data(full_df.values.tolist())

# Setup dropdowns for editable rows
def setup_dropdowns(self, start_row, end_row):
    self.setup_account_dropdown(start_row, end_row)
    self.setup_fund_dropdown(start_row, end_row)

def setup_account_dropdown(self, start_row, end_row):
    account_options = self.db_manager.fetch_chart_options()
    dropdown_values = [f"{row['Id']}:{row['Name']}" for _, row in account_options.iterrows()]
    headers = self.sheet.headers()
    account_col_idx = headers.index('AccountChoice')
    for row in range(start_row, end_row):
        current_value = self.sheet[row, account_col_idx].data
        self.sheet[row, account_col_idx].dropdown(
            values=dropdown_values,
            set_value=current_value
        )
```

### Managing Edit Mode
```python
# In application.py - Application class
# Enter edit mode - fetch transaction data and setup editing
def enter_edit_mode(self, event=None):
    if self.mode == "initial":
        self.selected_tran_id = current_data[self.selected_row][1]
        # Get data without balance column for edit mode
        ledger_df = self.db_manager.fetch_ledger_data(account_id)
        transaction_df = self.db_manager.fetch_transaction_data(self.selected_tran_id)
        # Combine data and setup edit environment
        self.ledger_sheet.set_all_readonly(True)
        self.ledger_sheet.set_row_readonly(start_idx, end_idx, False)
        self.ledger_sheet.setup_dropdowns(start_idx, end_idx)

# Save edit mode - persist changes to database
def save_edit_mode(self):
    if self.mode == "edit":
        current_data = self.ledger_sheet.get_current_data()
        user_date, description = self._extract_transaction_details(current_data)
        splits_data = self._collect_splits_data(current_data)
        success = self.db_manager.save_transaction(
            self.selected_tran_id, user_date, description, splits_data
        )
        if success:
            self.cancel_edit_mode()

# Cancel edit mode - restore balance column and normal view
def cancel_edit_mode(self):
    if self.mode == "edit":
        self.ledger_sheet.update_data(account_id, include_balance=True)
        self.mode = "initial"
```

### Module Imports
```python
# Import specific classes from modules
from database import DatabaseManager
from ui_components import ChartSelector, EditModeManager
from ledger_sheet import LedgerSheet
```

## Important Notes

### Database and Schema
- The application uses integer amounts (likely in cents) for financial calculations
- Foreign key constraints are enabled in SQLite
- Double-entry bookkeeping is enforced with transaction splits that sum to zero
- Account and Fund tables use Type fields (25 characters) for categorization
- Default "No Account" and "No Fund" entries (ID=0) provide fallback options
- Database indexes improve performance for common queries

### User Interface
- The UI prevents editing multiple rows simultaneously except for transaction splits
- The Balance column is calculated dynamically and not stored in the database
- Account and fund dropdown functionality is applied dynamically to editable rows
- All database columns are displayed automatically without hardcoded filtering
- Dropdowns are ordered by ID and initialized with current values

### Data Management
- Save operations perform complete transaction replacement (delete + insert)
- Database transactions ensure atomicity of save operations
- Cancel operations discard changes and restore original view
- The application includes sample data for testing and development