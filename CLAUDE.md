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
3. **Edit Validation**: Automatic synchronization and input validation
   - User_date and description sync across all splits
   - Date format validation (supports multiple formats: YYYY-MM-DD, MM/DD/YYYY, etc.)
   - Amount validation (must be valid numbers, rejects invalid input)
4. **Edit Operations**: 
   - Modify amounts, fund choices, account choices in editable rows
   - Edit user_date or description → automatically updates all splits in transaction
   - Add Split: Inserts new row after last selected position with current dropdown values
   - Delete Split: Removes selected editable row (prevents deletion of last split)
   - Balance Split: Calculates and sets amount for selected row to make transaction sum to zero
   - Delete Transaction: Soft deletes entire transaction with confirmation dialog
5. **Save/Cancel**: 
   - Save validates transaction balance (must sum to zero) before database operations
   - Uses stored original transaction details for consistency
   - Shows warning message if transaction is unbalanced, prevents saving

### Event Handling
- Cell selection triggers edit mode entry and stores transaction metadata
- Edit mode shows comprehensive button set: Cancel, Save Transaction, Add Split, Delete Split, Balance Split, Delete Transaction
- **Edit validation with input checking**: Date and amount validation prevents invalid data entry
- **Automatic synchronization**: User_date and description sync across all splits when edited
- **Format support**: Accepts multiple date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, etc.)
- Application tracks selected row, transaction ID, user date, and description separately
- Add Split intelligently positions new rows after last selected row
- Delete Split validates selection and prevents deletion of last remaining split
- Balance Split ensures double-entry bookkeeping by making transaction amounts sum to zero
- Save Transaction validates balance before saving, shows warning if unbalanced
- Delete Transaction performs soft delete with confirmation, preserves audit trail
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
        # Set up edit validation for user_date and description synchronization
        self.ledger_sheet.sheet.edit_validation(self.after_cell_edit)

# Save edit mode - validate balance and use stored transaction details
def save_edit_mode(self):
    if self.mode == "edit":
        # Validate that transaction amounts sum to zero
        if not self._validate_transaction_balance(current_data):
            messagebox.showwarning(
                "Transaction Not Balanced",
                "The sum of all amounts in the current transaction should equal zero. "
                "Please use the balance split button to achieve this."
            )
            return
        # Use stored original transaction details, not current row data
        user_date = self.selected_user_date
        description = self.selected_description
        splits_data = self._collect_splits_data(current_data)
        success = self.db_manager.save_transaction(
            self.selected_tran_id, user_date, description, splits_data
        )

# Validate transaction balance - ensure double-entry bookkeeping compliance
def _validate_transaction_balance(self, current_data):
    total_amount = 0.0
    for i in range(self.start_idx, self.end_idx):
        try:
            amount = float(current_data[i][6])  # Amount column
            total_amount += amount
        except (ValueError, IndexError):
            continue  # Treat invalid amounts as 0 for validation
    # Check if sum is close to zero (accounting for floating point precision)
    return abs(total_amount) < 0.01

# Delete transaction - soft delete with confirmation
def delete_transaction(self):
    if self.mode == "edit" and self.selected_tran_id:
        # Ask for confirmation with transaction details
        result = messagebox.askyesno(
            "Delete Transaction",
            f"Are you sure you want to delete transaction {self.selected_tran_id}?\n\n"
            f"Date: {self.selected_user_date}\n"
            f"Description: {self.selected_description}\n\n"
            f"This action cannot be undone."
        )
        if result:
            # Perform soft delete in database (only affects Transactions table)
            success = self.db_manager.soft_delete_transaction(self.selected_tran_id)
            if success:
                self.cancel_edit_mode()  # Exit edit mode
                self.update_table_with_account()  # Refresh view
                messagebox.showinfo("Transaction Deleted", 
                                  f"Transaction {self.selected_tran_id} has been successfully deleted.")

# Database soft delete - preserves audit trail
def soft_delete_transaction(self, tran_id):
    try:
        # Update only Transactions table, leave Split table unchanged
        self.cursor.execute("""
            UPDATE Transactions 
            SET Deleted = 1, Deleted_at = CURRENT_TIMESTAMP 
            WHERE Id = ? AND Deleted = 0
        """, (tran_id,))
        return self.cursor.rowcount > 0  # True if row was updated
    except Exception as e:
        self.conn.rollback()
        return False

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

# Balance split - ensure transaction sums to zero
def balance_split_row(self):
    if self.mode == "edit":
        selected_cells = self.ledger_sheet.sheet.get_currently_selected()
        selected_row = selected_cells[0]
        # Validate selection is within editable range
        if self.start_idx <= selected_row < self.end_idx:
            # Calculate sum of all other amounts in transaction
            total_other_amounts = 0.0
            for i in range(self.start_idx, self.end_idx):
                if i != selected_row:
                    amount = float(current_data[i][6])  # Amount column
                    total_other_amounts += amount
            # Set balancing amount (negative of sum) to make total zero
            balancing_amount = -total_other_amounts
            formatted_amount = f"{balancing_amount:.2f}"
            self.ledger_sheet.sheet.set_cell_data(selected_row, 6, formatted_amount)

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

# Edit validation - input validation and synchronization
def after_cell_edit(self, event):
    if self.mode == "edit" and self.start_idx <= event.row < self.end_idx:
        edited_value = event.value
        current_data = self.ledger_sheet.get_current_data()
        old_value = current_data[event.row][event.column]
        
        if event.column == 2:  # UserDate column
            # Validate date format before accepting
            if not self._is_valid_date(edited_value):
                return old_value  # Reject invalid date, keep old value
            # Update user_date in all editable rows except current
            for i in range(self.start_idx, self.end_idx):
                if i != event.row:
                    self.ledger_sheet.sheet.set_cell_data(i, 2, edited_value)
            self.selected_user_date = edited_value
        elif event.column == 3:  # Description column
            # Update description in all editable rows except current
            for i in range(self.start_idx, self.end_idx):
                if i != event.row:
                    self.ledger_sheet.sheet.set_cell_data(i, 3, edited_value)
            self.selected_description = edited_value
        elif event.column == 6:  # Amount column
            # Validate amount is a valid number
            if not self._is_valid_amount(edited_value):
                return old_value  # Reject invalid amount, keep old value
    return event.value  # Return validated value to allow edit

# Date validation - supports multiple common formats
def _is_valid_date(self, date_string):
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y", "%d-%m-%Y"]
    for date_format in date_formats:
        try:
            datetime.strptime(date_string.strip(), date_format)
            return True
        except ValueError:
            continue
    return False

# Amount validation - ensures numeric input
def _is_valid_amount(self, amount_string):
    if not amount_string:  # Empty string allowed
        return True
    try:
        float(amount_string)
        return True
    except (ValueError, TypeError):
        return False

# Cancel edit mode - clear stored data and restore view
def cancel_edit_mode(self):
    if self.mode == "edit":
        self.mode = "initial"
        self.selected_tran_id = None
        self.selected_user_date = None
        self.selected_description = None
        # Clear edit validation
        self.ledger_sheet.sheet.edit_validation(None)
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