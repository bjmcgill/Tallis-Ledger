# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

Tallis Ledger is a modern Tkinter-based accounting application that provides a professional spreadsheet-like interface for managing financial transactions. The application uses SQLite for data persistence and the tksheet library for the interactive data grid with comprehensive edit mode functionality.

### Core Architecture

The application follows a modular architecture with clear separation of concerns and professional cross-platform styling:

**Module Structure:**
- **`main.py`**: Application entry point
- **`application.py`**: Main Application class coordinating all components with TTK styling
- **`database.py`**: DatabaseManager class for all SQLite operations with REAL amount precision
- **`ui_components.py`**: AccountSelector, FundSelector, and EditModeManager classes using TTK widgets
- **`ledger_sheet.py`**: LedgerSheet class wrapping tksheet widget with decimal formatting

**Key Classes:**
- **DatabaseManager**: Handles all SQLite database operations with foreign key constraints
- **AccountSelector**: Manages the account dropdown selection with "Id:Name" format
- **FundSelector**: Manages the fund dropdown selection with "Id:Name" format  
- **EditModeManager**: Controls edit mode UI with comprehensive button set (Cancel, Save, Add Split, Delete Split, Balance Split, Delete Transaction)
- **LedgerSheet**: Wraps tksheet widget with decimal formatting and dropdown support
- **Application**: Main controller with cross-platform window management and TTK styling

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
1. User selects an account or fund from the dropdown selectors
2. `fetch_ledger_data()` retrieves transactions with formatted choice fields ("Id:Name")
3. Data is displayed in the tksheet grid with decimal formatting and Balance column
4. User clicks on any cell to enter edit mode for that transaction
5. System stores original transaction details (tran_id, user_date, description) from selected row
6. All splits for the transaction are fetched and displayed as editable rows
7. Edit mode removes Balance column and highlights transaction splits in red
8. User can add/delete splits, modify amounts, and change account/fund assignments
9. Save preserves stored original transaction details while updating split data
10. Cancel/save completion restores Balance column and normal view

### Edit Mode Workflow
1. **Enter Edit Mode**: Click on any cell → stores transaction details from selected row
2. **Display Splits**: All splits for transaction shown as red highlighted editable rows
3. **Edit Operations**: 
   - Modify amounts, fund choices, account choices in editable rows
   - Add Split: Inserts new row after last selected position with current dropdown values
   - Delete Split: Removes selected editable row (prevents deletion of last split)
4. **Save/Cancel**: Uses stored original transaction details for database operations

### Event Handling
- Cell selection triggers edit mode entry and stores transaction metadata
- Edit mode shows comprehensive button set: Cancel, Save Transaction, Add Split, Delete Split, Balance Split, Delete Transaction
- Application tracks selected row, transaction ID, user date, and description separately
- Add Split intelligently positions new rows after last selected row
- Delete Split validates selection and prevents deletion of last remaining split
- Readonly spans prevent editing of non-transaction rows
- Account and fund dropdowns use "Id:Name" format with no spaces
- Dropdowns are initialized with current database values ordered by ID
- Red highlighting with white text indicates editable transaction splits
- Save uses stored transaction details for consistency regardless of current row changes
- Cancel restores original view with balance calculations

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
# Update sheet data with dynamic headers and formatted amounts
def update_data(self, filter_id, filter_type='account', include_balance=True):
    full_df = self.db_manager.fetch_ledger_data(filter_id, filter_type)
    if include_balance:
        full_df['Balance'] = full_df['Amount'].cumsum()
    
    # Format Amount and Balance columns to 2 decimal places
    formatted_data = full_df.copy()
    formatted_data['Amount'] = formatted_data['Amount'].apply(lambda x: f"{float(x):.2f}")
    if include_balance:
        formatted_data['Balance'] = formatted_data['Balance'].apply(lambda x: f"{float(x):.2f}")
    
    self.sheet.headers(list(formatted_data.columns))
    self.sheet.set_sheet_data(formatted_data.values.tolist())

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

# Save edit mode - use stored transaction details for consistency
def save_edit_mode(self):
    if self.mode == "edit":
        # Use stored original transaction details, not current row data
        user_date = self.selected_user_date
        description = self.selected_description
        splits_data = self._collect_splits_data(current_data)
        success = self.db_manager.save_transaction(
            self.selected_tran_id, user_date, description, splits_data
        )

# Add split - insert new row after last selected position
def add_split_row(self):
    if self.mode == "edit":
        selected_cells = self.ledger_sheet.sheet.get_currently_selected()
        last_selected_row = selected_cells[0] if selected_cells else self.end_idx - 1
        # Smart positioning: after selected row or at start/end of editable range
        current_fund_selection = self.fund_selector.selected_fund.get()
        current_account_selection = self.account_selector.selected_account.get()
        # Use stored transaction details for new row
        new_row = [0, self.selected_tran_id, self.selected_user_date, 
                  self.selected_description, current_fund_selection, 
                  current_account_selection, "0.00"]

# Delete split - remove selected row with validation
def delete_split_row(self):
    if self.mode == "edit":
        selected_cells = self.ledger_sheet.sheet.get_currently_selected()
        if self.end_idx - self.start_idx <= 1:  # Prevent deletion of last split
            return
        # Validate selection is within editable range and remove row

# Collect splits data - convert formatted amounts back to float
def _collect_splits_data(self, current_data):
    splits_data = []
    for i in range(self.start_idx, self.end_idx):
        row = current_data[i]
        amount = float(row[6])  # Amount column - convert formatted string to float
        fund_choice = row[4]  # FundChoice column (format: "Id:Name")
        account_choice = row[5]  # AccountChoice column (format: "Id:Name")
        # Extract IDs from choice strings: split(':')[0]
        fund_id = int(fund_choice.split(':')[0]) if fund_choice else 0
        account_id = int(account_choice.split(':')[0]) if account_choice else 0
    return splits_data

# Cancel edit mode - clear stored data and restore view
def cancel_edit_mode(self):
    if self.mode == "edit":
        self.mode = "initial"
        self.selected_tran_id = None
        self.selected_user_date = None
        self.selected_description = None
```

### Module Imports
```python
# Import specific classes from modules
from database import DatabaseManager
from ui_components import AccountSelector, FundSelector, EditModeManager
from ledger_sheet import LedgerSheet
```

## Important Notes

### Database and Schema
- The application uses REAL (float) amounts for financial calculations with 2 decimal place precision
- All monetary amounts are stored as floating point numbers in the Split.Amount column
- Foreign key constraints are enabled in SQLite
- Double-entry bookkeeping is enforced with transaction splits that sum to zero
- Account and Fund tables use Type fields (25 characters) for categorization
- Default "No Account" and "No Fund" entries (ID=0) provide fallback options
- Database indexes improve performance for common queries

### User Interface
- The UI prevents editing multiple rows simultaneously except for transaction splits
- The Balance column is calculated dynamically and not stored in the database
- Amount and Balance columns are automatically formatted to 2 decimal places for display
- Account and fund dropdown functionality is applied dynamically to editable rows
- All database columns are displayed automatically without hardcoded filtering
- Dropdowns are ordered by ID and initialized with current values

### Data Management
- Save operations perform complete transaction replacement (delete + insert)
- Database transactions ensure atomicity of save operations
- Cancel operations discard changes and restore original view
- The application includes sample data for testing and development