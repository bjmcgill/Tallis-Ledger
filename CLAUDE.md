# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

Tallis Ledger is a Tkinter-based accounting application that provides a spreadsheet-like interface for managing financial transactions. The application uses SQLite as its database and the tksheet library for the interactive data grid.

### Core Architecture

The application follows a class-based architecture with separation of concerns:

- **DatabaseManager**: Handles all SQLite database operations and queries
- **ChartSelector**: Manages the account dropdown selection widget
- **EditModeManager**: Controls the edit mode UI state and buttons
- **LedgerSheet**: Wraps the tksheet widget and handles data display
- **Application**: Main controller that coordinates all components

### Database Schema

The application uses a double-entry accounting system with these key tables:

- **Transactions**: Main transaction records with date, description, and posting status
- **Split**: Individual accounting entries that implement double-entry bookkeeping
- **Chart**: Chart of accounts (assets, liabilities, income, expenses)
- **Fund**: Fund accounting for tracking restricted/unrestricted funds

## Common Development Commands

### Running the Application
```bash
python main.py
```

### Setting Up the Database
```bash
sqlite3 your_ledger.db < createtables.sql
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

### Database Operations
- All database interactions go through the `DatabaseManager` class
- The application maintains foreign key constraints
- Use parameterized queries to prevent SQL injection
- The database file is `your_ledger.db` by default

### UI Components
- The main data grid uses tksheet - refer to `tksheet_reference.md` for detailed API
- The application has two modes: "initial" (read-only) and "edit" (editable)
- Edit mode is triggered by clicking on a cell and shows action buttons
- The chart selector filters the ledger display by account

### Data Flow
1. User selects an account from the dropdown
2. `fetch_ledger_data()` retrieves transactions for that account
3. Data is displayed in the tksheet grid
4. User can enter edit mode to modify transaction data
5. Changes are validated and saved back to the database

### Event Handling
- Cell selection triggers edit mode entry
- Edit mode shows Cancel/Save/Delete buttons
- The application tracks the selected row for edit operations
- Readonly spans prevent editing of non-selected rows

## Code Patterns

### Adding New Database Queries
```python
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
# Update sheet data
self.sheet.set_sheet_data(data_list)

# Handle cell selection
def on_cell_click(self, event):
    selected_row = self.sheet.get_currently_selected()[0]
    # Process selection
```

### Managing Edit Mode
```python
# Enter edit mode
self.mode = "edit"
self.ledger_sheet.set_row_readonly(start, end)
self.edit_mode_manager.show_edit_buttons()

# Exit edit mode
self.mode = "initial"
self.ledger_sheet.set_all_readonly(False)
self.edit_mode_manager.hide_edit_buttons()
```

## Important Notes

- The application uses integer amounts (likely in cents) for financial calculations
- Foreign key constraints are enabled in SQLite
- The UI prevents editing multiple rows simultaneously
- Posted transactions may have different business rules than unposted ones
- The application includes sample data for testing and development