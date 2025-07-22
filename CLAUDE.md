# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

Tallis Ledger is a comprehensive Tkinter-based accounting application that provides a professional spreadsheet-like interface for managing financial transactions. The application implements double-entry bookkeeping principles with modern UI components and robust data validation.

### Core Architecture

The application follows a modular architecture with clear separation of concerns and professional cross-platform styling:

**Module Structure:**
- **`main.py`**: Application entry point
- **`application.py`**: Main Application class with comprehensive mode management (initial, edit, add)
- **`database.py`**: DatabaseManager class with flexible database selection and CRUD operations
- **`ui_components.py`**: Professional UI components using TTK widgets with dynamic button management
- **`ledger_sheet.py`**: LedgerSheet class with configurable column widths and tksheet integration

**Key Classes:**
- **DatabaseManager**: Handles SQLite operations with file selection dialog and performance indexes
- **AccountSelector**: TTK combobox for account selection with "Id:Name" format
- **FundSelector**: TTK combobox for fund selection with "Id:Name" format  
- **EditModeManager**: Dynamic button management for different application modes
- **LedgerSheet**: Advanced tksheet wrapper with decimal formatting and configurable column widths
- **Application**: Central coordinator with three distinct modes and comprehensive transaction management

### Database Schema

The application implements a complete double-entry accounting system:

**Core Tables:**
- **Transactions**: Main transaction records with soft delete capability
  - `Id` (PRIMARY KEY), `UserDate`, `Description` (100 chars max), `Created_at`, `Deleted`, `Deleted_at`
- **Split**: Individual accounting entries implementing double-entry bookkeeping
  - `Id` (PRIMARY KEY), `Tran_id` (FK), `Amount` (REAL), `FundId` (FK), `AccountId` (FK)
- **Account**: Chart of accounts with configurable types
  - `Id` (PRIMARY KEY), `Name` (50 chars), `Type` (25 chars)
- **Fund**: Fund accounting for different fund types
  - `Id` (PRIMARY KEY), `Name` (50 chars), `Type` (25 chars)

**Performance Features:**
- Comprehensive indexes on all major columns for optimal query performance
- Foreign key constraints enabled for data integrity
- Soft delete pattern preserves audit trails
- REAL data type for precise decimal calculations

**Default Records:**
- Default "No Account" (ID=0) and "No Fund" (ID=0) entries for system flexibility

## Application Modes

### Initial Mode (View Mode)
- **Display**: All transactions with calculated Balance column (cumulative sum)
- **Interaction**: Read-only display, single-click row selection enters edit mode
- **UI Elements**: Account/Fund selectors enabled, "Add Transaction" button visible
- **Database Selection**: Shows file dialog when `_DEBUG=False`, uses default when `_DEBUG=True`

### Edit Mode (Transaction Editing)
- **Trigger**: Single-click on any row in initial mode
- **Display**: Transaction splits highlighted in red, balance column removed
- **Features**: 
  - Edit transaction date, description, amounts, fund/account assignments
  - Automatic synchronization of date/description across all splits
  - Input validation for dates and amounts
  - Readonly protection for ID columns (SplitId, TransactionsId)
- **Buttons**: Cancel, Save Transaction, Add Split, Delete Split, Balance Split, Delete Transaction
- **Validation**: Transaction must balance (sum to zero) before saving

### Add Mode (New Transaction Creation)
- **Trigger**: Click "Add Transaction" button in initial mode
- **Display**: Two new editable rows appended to bottom, balance column removed
- **Features**: 
  - Default current date and empty description
  - Uses current fund/account selector values as defaults
  - Same editing capabilities as edit mode
  - Focus automatically set to Description column
- **Buttons**: Cancel, Save Transaction, Add Split, Delete Split, Balance Split
- **Validation**: Same balance requirements as edit mode

## Key Features

### Database Management
```python
# Database initialization with file selection
def _initialize_database(self):
    if _DEBUG:
        return DatabaseManager("your_ledger.db")  # Auto-load for development
    else:
        # Show file dialog for production use
        db_path = filedialog.askopenfilename(
            title="Select Database File",
            filetypes=[("SQLite Database", "*.db"), ("SQLite Database", "*.sqlite")]
        )
        return DatabaseManager(db_path)
```

### Column Width Configuration
```python
# Easily customizable column widths
def set_column_widths(self):
    column_widths = {
        'SplitId': 50,           # Narrow ID columns
        'TransactionsId': 50,
        'UserDate': 150,
        'Description': 800,      # Wide for readability
        'FundChoice': 150,
        'AccountChoice': 150,
        'Amount': 150,
        'Balance': 150
    }
    # Applied automatically when headers are updated
```

### Transaction Management
```python
# Complete transaction lifecycle
def enter_edit_mode(self, event=None):
    # Store transaction metadata on entry
    self.selected_tran_id = selected_row_data[1]
    self.selected_user_date = selected_row_data[2]
    self.selected_description = selected_row_data[3]
    
    # Set focus to appropriate column
    self.ledger_sheet.sheet.set_currently_selected(self.start_idx, 4)  # FundChoice

def save_edit_mode(self):
    # Validate balance before saving
    if not self._validate_transaction_balance(current_data):
        messagebox.showwarning("Transaction Not Balanced", "...")
        return
    
    # Use stored metadata for consistency
    success = self.db_manager.save_transaction(
        self.selected_tran_id, self.selected_user_date, 
        self.selected_description, splits_data
    )
```

### Input Validation and Synchronization
```python
def after_cell_edit(self, event):
    """Real-time validation and synchronization"""
    if event.column == 2:  # UserDate
        if not self._is_valid_date(edited_value):
            return old_value  # Reject invalid dates
        # Sync date across all transaction splits
        for i in range(self.start_idx, self.end_idx):
            if i != event.row:
                self.sheet.set_cell_data(i, 2, edited_value)
    elif event.column == 6:  # Amount
        if not self._is_valid_amount(edited_value):
            return old_value  # Reject non-numeric amounts
```

### Smart Split Management
```python
def add_split_row(self):
    """Intelligent positioning and default values"""
    # Insert after last selected row or at appropriate position
    selected_cells = self.ledger_sheet.sheet.get_currently_selected()
    insert_position = self._calculate_insert_position(selected_cells)
    
    # Use current dropdown selections as defaults
    new_row = [
        0, self.selected_tran_id, self.selected_user_date,
        self.selected_description, current_fund_selection,
        current_account_selection, "0.00"
    ]

def balance_split_row(self):
    """Ensure double-entry bookkeeping compliance"""
    total_other_amounts = sum(amounts_except_selected_row)
    balancing_amount = -total_other_amounts
    self.sheet.set_cell_data(selected_row, 6, f"{balancing_amount:.2f}")
```

### Soft Delete with Audit Trail
```python
def delete_transaction(self):
    """Safe transaction deletion with confirmation"""
    result = messagebox.askyesno(
        "Delete Transaction",
        f"Delete transaction {self.selected_tran_id}?\n"
        f"Date: {self.selected_user_date}\n"
        f"Description: {self.selected_description}"
    )
    if result:
        self.db_manager.soft_delete_transaction(self.selected_tran_id)

def soft_delete_transaction(self, tran_id):
    """Preserve audit trail - only mark as deleted"""
    self.cursor.execute("""
        UPDATE Transactions 
        SET Deleted = 1, Deleted_at = CURRENT_TIMESTAMP 
        WHERE Id = ? AND Deleted = 0
    """, (tran_id,))
    # Split records remain unchanged for audit purposes
```

## Development Commands

### Application Startup
```bash
# Development mode (auto-loads your_ledger.db)
# Set _DEBUG = True in application.py
python main.py

# Production mode (shows database file dialog)
# Set _DEBUG = False in application.py  
python main.py
```

### Database Setup
```bash
# Create tables with performance indexes
sqlite3 your_ledger.db < createtables.sql

# Add sample data
sqlite3 your_ledger.db < insertdata.sql
```

### Dependencies
```bash
pip install tksheet pandas  # Core dependencies
# tkinter and sqlite3 are built-in to Python
```

## Code Patterns and Best Practices

### Mode-Aware Development
```python
# Always check current mode for appropriate behavior
if self.mode == "initial":
    # Handle view-only interactions
elif self.mode in ["edit", "add"]:
    # Handle editing operations
    if self.mode == "edit":
        # Edit-specific logic (existing transaction)
    else:  # add mode
        # Add-specific logic (new transaction)
```

### Database Query Patterns
```python
# Parameterized queries with proper formatting
def fetch_ledger_data(self, filter_id, filter_type='account'):
    query = f"""
        SELECT Split.Id AS SplitId, Transactions.Id AS TransactionsId,
               Transactions.UserDate, Transactions.Description,
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
```

### UI Component Management
```python
# Dynamic button management for different modes
def hide_edit_buttons(self):
    """Comprehensive cleanup of all UI elements"""
    for button in self.buttons:
        button.destroy()
    self.buttons = []
    # Also clear any orphaned widgets
    for widget in self.button_frame.winfo_children():
        widget.destroy()

def show_add_transaction_button(self):
    """Show single button for initial mode"""
    button_container = ttk.Frame(self.button_frame)
    self.add_transaction_button = ttk.Button(
        button_container, text="Add Transaction",
        command=self._on_add_transaction, style="Accent.TButton"
    )
```

### Error Handling and Validation
```python
# Robust error handling with user feedback
def _validate_transaction_balance(self, current_data):
    total_amount = 0.0
    for i in range(self.start_idx, self.end_idx):
        try:
            amount = float(current_data[i][6])
            total_amount += amount
        except (ValueError, IndexError):
            continue  # Skip invalid amounts
    return abs(total_amount) < 0.01  # Floating point precision tolerance

# Multi-format date validation
def _is_valid_date(self, date_string):
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%m-%d-%Y", "%d/%m/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            datetime.strptime(date_string.strip(), fmt)
            return True
        except ValueError:
            continue
    return False
```

## Important Implementation Notes

### Data Integrity
- **Double-Entry Bookkeeping**: All transactions must balance (sum to zero)
- **Foreign Key Constraints**: Enabled for referential integrity
- **Soft Delete Pattern**: Preserves audit trails for deleted transactions
- **Input Validation**: Real-time validation for dates and amounts
- **Transaction Atomicity**: Database transactions ensure consistency

### Performance Optimization
- **Comprehensive Indexes**: All major columns indexed for query performance
- **Efficient Data Loading**: Fetch only necessary columns with proper joins
- **Smart UI Updates**: Minimal redraws and targeted cell updates
- **Configurable Column Widths**: Optimized display without unnecessary scrolling

### User Experience
- **Single-Click Interaction**: Immediate mode transitions without double-clicking
- **Smart Focus Management**: Appropriate column focus for different modes
- **Visual Feedback**: Color-coded rows (white=readonly, red=editable)
- **Input Validation**: Immediate feedback for invalid data entry
- **Confirmation Dialogs**: Safety checks for destructive operations

### Cross-Platform Compatibility
- **TTK Styling**: Professional appearance across operating systems
- **Platform-Specific Fonts**: Automatic font selection (Segoe UI/SF Pro/Liberation Sans)
- **Window Management**: Proper maximization and sizing for different platforms
- **File Dialog Integration**: Native file selection dialogs

This documentation reflects the current comprehensive state of the Tallis Ledger application with its complete transaction management system, flexible database handling, and professional user interface.