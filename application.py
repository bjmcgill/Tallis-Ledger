"""
Main application module for Tallis Ledger.
Contains the main Application class that coordinates all components.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from database import DatabaseManager
from ui_components import AccountSelector, FundSelector, EditModeManager
from ledger_sheet import LedgerSheet


_DEBUG = False  # Set to True for debugging output


class Application:
    """Main controller that coordinates all components."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tallis Ledger - Accounting Application")

        # Configure ttk style for professional appearance
        self.style = ttk.Style()

        # Try to use a native theme for better cross-platform appearance
        available_themes = self.style.theme_names()
        if 'aqua' in available_themes:  # macOS
            self.style.theme_use('aqua')
        elif 'vista' in available_themes:  # Windows Vista/7+
            self.style.theme_use('vista')
        elif 'xpnative' in available_themes:  # Windows XP
            self.style.theme_use('xpnative')
        elif 'clam' in available_themes:  # Cross-platform modern theme
            self.style.theme_use('clam')

        # Configure custom styles
        self._configure_styles()

        # Maximize window on startup
        self.root.resizable(True, True)

        # Cross-platform window maximization
        try:
            # Try different methods depending on the platform
            if self.root.tk.call('tk', 'windowingsystem') == 'win32':
                self.root.state('zoomed')
            elif self.root.tk.call('tk', 'windowingsystem') == 'x11':
                self.root.attributes('-zoomed', True)
            else:  # macOS and others
                # Get screen dimensions and set window to nearly full screen
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.root.geometry(f"{screen_width}x{screen_height-100}+0+0")
        except Exception:
            # Fallback: try to maximize using geometry
            try:
                self.root.state('zoomed')
            except Exception:
                # Final fallback: set large window size
                self.root.geometry("1400x900+50+50")
        
        # Initialize instance variables
        self.mode = "initial"  # "initial", "edit", or "add"
        self.selected_row = None
        self.selected_tran_id = None
        self.selected_user_date = None
        self.selected_description = None
        self.current_filter_type = "account"  # 'account' or 'fund'
        self.start_idx = None
        self.end_idx = None
        
        # Create main layout frames using ttk
        self.main_container = ttk.Frame(root, style='Main.TFrame')
        self.main_container.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Selector frame with professional styling
        self.selector_frame = ttk.Frame(self.main_container, style='Selector.TFrame')
        self.selector_frame.pack(side="top", pady=(0, 10), fill="x")
        
        # Button frame (initially empty, shown in edit mode)
        self.button_frame = ttk.Frame(self.main_container, style='Button.TFrame')
        self.button_frame.pack(side="top", pady=(0, 5), fill="x")
        
        # Create a container frame for the sheet with professional border
        self.sheet_container = ttk.Frame(
            self.main_container,
            style='SheetContainer.TFrame',
            relief="sunken",
            borderwidth=1
        )
        self.sheet_container.pack(expand=True, fill="both")
        
        # Create the sheet frame inside the container
        # Keep as tk.Frame for tksheet compatibility
        self.sheet_frame = tk.Frame(self.sheet_container)
        self.sheet_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Initialize components
        self.db_manager = self._initialize_database()
        
        # Create a centered container for the selectors
        selector_container = ttk.Frame(self.selector_frame)
        selector_container.pack(expand=True, pady=5)
        
        # Add labels and selectors using ttk in centered container
        fund_label = ttk.Label(selector_container, text="Fund:", style='SelectorLabel.TLabel')
        fund_label.pack(side="left", padx=(0, 5))
        
        self.fund_selector = FundSelector(selector_container, self.db_manager, self.update_table_with_fund)
        
        account_label = ttk.Label(selector_container, text="Account:", style='SelectorLabel.TLabel')
        account_label.pack(side="left", padx=(20, 5))
        
        self.account_selector = AccountSelector(
            selector_container, self.db_manager, self.update_table_with_account
        )
        self.edit_mode_manager = EditModeManager(
            self.button_frame, self.cancel_edit_mode, self.save_edit_mode, self
        )
        self.ledger_sheet = LedgerSheet(
            self.sheet_frame, self.db_manager, self.enter_edit_mode
        )
        
        self.update_table_with_account(self.account_selector.initial_option)
        self.ledger_sheet.set_all_readonly(True)
        
        # Show Add Transaction button on startup
        self.edit_mode_manager.show_add_transaction_button()
    
    def _configure_styles(self):
        """Configure custom ttk styles for professional appearance."""
        # Main container style
        self.style.configure('Main.TFrame', background='#f0f0f0')
        
        # Selector frame style with subtle background
        self.style.configure('Selector.TFrame', 
                           background='#f8f8f8',
                           relief='solid',
                           borderwidth=1)
        
        # Button frame style
        self.style.configure('Button.TFrame', background='#f0f0f0')
        
        # Sheet container style
        self.style.configure('SheetContainer.TFrame',
                           background='#ffffff',
                           relief='sunken',
                           borderwidth=2)
        
        # Selector label style with cross-platform fonts
        platform_font = self._get_platform_font()
        self.style.configure('SelectorLabel.TLabel',
                           background='#f8f8f8',
                           foreground='#333333',
                           font=(platform_font, 10, 'bold'))
        
        # Enhanced button styles
        self.style.configure('Accent.TButton',
                           foreground='white',
                           background='#0078d4')
        
        self.style.map('Accent.TButton',
                      background=[('active', '#106ebe'),
                                ('pressed', '#005a9e')])
    
    def _get_platform_font(self):
        """Get the appropriate font for the current platform."""
        windowing_system = self.root.tk.call('tk', 'windowingsystem')
        if windowing_system == 'win32':
            return 'Segoe UI'
        elif windowing_system == 'aqua':  # macOS
            return 'SF Pro Display'
        else:  # Linux/X11
            return 'Liberation Sans'
    
    def _initialize_database(self):
        """
        Initialize the database connection based on DEBUG mode.
        
        When _DEBUG is True: Uses 'your_ledger.db' automatically
        When _DEBUG is False: Shows file dialog to select .db file
        
        Returns:
            DatabaseManager instance or None if connection fails
        """
        if _DEBUG:
            # Debug mode: Use default database file
            db_path = "your_ledger.db"
            print(f"Debug mode: Using default database: {db_path}")
        else:
            # Production mode: Show file dialog to select database
            db_path = filedialog.askopenfilename(
                title="Select Database File",
                filetypes=[
                    ("SQLite Database", "*.db"),
                    ("SQLite Database", "*.sqlite"),
                    ("All Files", "*.*")
                ],
                initialdir="."
            )
            
            # If user cancelled the dialog, fallback to default database
            if not db_path:
                db_path = "your_ledger.db"
                messagebox.showinfo(
                    "Default Database",
                    f"No database selected. Using default: {db_path}"
                )
        
        try:
            from database import DatabaseManager
            return DatabaseManager(db_path)
        except Exception as e:
            # If database connection fails, show error and exit gracefully
            messagebox.showerror(
                "Database Error",
                f"Failed to open database: {db_path}\nError: {str(e)}"
            )
            self.root.quit()
            return None
    
    def update_table_with_account(self, _selected_option=None):
        """Update the ledger display when a different account is selected."""
        self.current_filter_type = "account"
        account_id = self.account_selector.get_selected_account_id()
        self.ledger_sheet.update_data(account_id, filter_type="account")

    def update_table_with_fund(self, _selected_option=None):
        """Update the ledger display when a different fund is selected."""
        self.current_filter_type = "fund"
        fund_id = self.fund_selector.get_selected_fund_id()
        self.ledger_sheet.update_data(fund_id, filter_type="fund")

    def enter_edit_mode(self, _event=None):
        """Enter edit mode for the selected transaction."""
        if self.mode == "initial":
            self.selected_row = self.ledger_sheet.get_selected_row()
            
            # Check if a valid row is selected
            if self.selected_row is None:
                if _DEBUG:
                    print("No row selected, cannot enter edit mode")
                return
            
            # Get current data to extract transaction details
            current_data = self.ledger_sheet.get_current_data()
            if self.selected_row < len(current_data):
                # Store transaction details from the selected row
                selected_row_data = current_data[self.selected_row]
                self.selected_tran_id = selected_row_data[1]      # TransactionsId at index 1
                self.selected_user_date = selected_row_data[2]    # UserDate at index 2
                self.selected_description = selected_row_data[3]  # Description at index 3
                
                # Get data without balance column for edit mode
                if self.current_filter_type == "account":
                    filter_id = self.account_selector.get_selected_account_id()
                else:
                    filter_id = self.fund_selector.get_selected_fund_id()
                ledger_df = self.db_manager.fetch_ledger_data(
                    filter_id, self.current_filter_type
                )
                
                # Format the ledger data (without balance column)
                formatted_ledger_df = self.ledger_sheet.format_decimal_columns(
                    ledger_df, include_balance=False
                )
                current_data_no_balance = formatted_ledger_df.values.tolist()

                # Fetch all splits for this transaction
                transaction_df = self.db_manager.fetch_transaction_data(
                    self.selected_tran_id
                )

                # Format the transaction data
                formatted_transaction_df = self.ledger_sheet.format_decimal_columns(
                    transaction_df, include_balance=False
                )
                transaction_data = formatted_transaction_df.values.tolist()
                
                # Combine data: before selected row + transaction data + after selected row
                if _DEBUG:
                    print("Head :", current_data_no_balance[:self.selected_row])
                    print("Transaction data :", transaction_data)
                    print("Tail :", current_data_no_balance[self.selected_row + 1:])

                new_data = (
                    current_data_no_balance[:self.selected_row] +
                    transaction_data +
                    current_data_no_balance[self.selected_row + 1:]
                )
                
                # Update headers without balance column
                self.ledger_sheet.sheet.headers(list(formatted_transaction_df.columns))
                self.ledger_sheet.sheet.set_sheet_data(new_data)
                self.ledger_sheet.set_column_widths()
                
                # Highlight transaction rows in red with white text
                self.start_idx = self.selected_row
                self.end_idx = self.start_idx + len(transaction_data)
                
                # Setup account and fund dropdowns for the editable rows
                self.ledger_sheet.setup_dropdowns(self.start_idx, self.end_idx)

                if _DEBUG:
                    print("start_idx:", self.start_idx, "end_idx:", self.end_idx)
                
                for i in range(0,self.start_idx):
                    self.ledger_sheet.highlight_row(i, bg="white", fg="black")
                for i in range(self.start_idx, self.end_idx):
                    self.ledger_sheet.highlight_row(i, bg="red", fg="white")
                for i in range(self.end_idx, len(new_data)):
                    self.ledger_sheet.highlight_row(i, bg="white", fg="black")
                
                self.mode = "edit"
                self.account_selector.set_enabled(False)
                self.fund_selector.set_enabled(False)
                self.ledger_sheet.set_all_readonly(True)
                
                # Make the highlighted red rows editable
                self.ledger_sheet.set_row_readonly(
                    self.start_idx, self.end_idx, False
                )

                # Make ID columns (SplitId and TransactionsId) readonly in editable rows
                for row in range(self.start_idx, self.end_idx):
                    self.ledger_sheet.sheet.readonly(row, 0, readonly=True)  # SplitId column
                    self.ledger_sheet.sheet.readonly(row, 1, readonly=True)  # TransactionsId column

                # Set up edit validation to synchronize user_date and description
                self.ledger_sheet.sheet.edit_validation(self.after_cell_edit)
                
                # Set focus to FundChoice column (column 4) of the first editable row
                self.ledger_sheet.sheet.set_currently_selected(self.start_idx, 4)
                
                # Hide Add Transaction button and show edit buttons
                self.edit_mode_manager.hide_edit_buttons()
                self.edit_mode_manager.show_edit_buttons()
    
    def enter_add_mode(self):
        """Enter add mode to create a new transaction."""
        if self.mode == "initial":
            # Get current selections from dropdowns for default values
            current_fund_selection = self.fund_selector.selected_fund.get()
            current_account_selection = self.account_selector.selected_account.get()
            
            # Initialize new transaction details with defaults
            from datetime import date
            self.selected_tran_id = None  # Will be set when saved
            self.selected_user_date = date.today().strftime("%Y-%m-%d")
            self.selected_description = ""
            
            # Get data without balance column for add mode
            if self.current_filter_type == "account":
                filter_id = self.account_selector.get_selected_account_id()
            else:
                filter_id = self.fund_selector.get_selected_fund_id()
            ledger_df = self.db_manager.fetch_ledger_data(
                filter_id, self.current_filter_type
            )
            
            # Format the ledger data (without balance column)
            formatted_ledger_df = self.ledger_sheet.format_decimal_columns(
                ledger_df, include_balance=False
            )
            current_data_no_balance = formatted_ledger_df.values.tolist()
            
            # Create two empty rows for the new transaction
            new_row_1 = [
                0,  # SplitId (will be set when saved)
                0,  # TransactionsId (will be set when saved)
                self.selected_user_date,  # UserDate
                self.selected_description,  # Description
                current_fund_selection,  # FundChoice
                current_account_selection,  # AccountChoice
                "0.00"  # Amount
            ]
            
            new_row_2 = [
                0,  # SplitId (will be set when saved)
                0,  # TransactionsId (will be set when saved)
                self.selected_user_date,  # UserDate
                self.selected_description,  # Description
                current_fund_selection,  # FundChoice
                current_account_selection,  # AccountChoice
                "0.00"  # Amount
            ]
            
            # Add the new rows to the bottom of the sheet (without balance column)
            new_data = current_data_no_balance + [new_row_1, new_row_2]
            
            # Update headers without balance column
            self.ledger_sheet.sheet.headers(list(formatted_ledger_df.columns))
            self.ledger_sheet.sheet.set_sheet_data(new_data)
            self.ledger_sheet.set_column_widths()
            
            # Set up the editable range (last two rows)
            self.start_idx = len(current_data_no_balance)
            self.end_idx = len(new_data)
            
            # Setup account and fund dropdowns for the editable rows
            self.ledger_sheet.setup_dropdowns(self.start_idx, self.end_idx)
            
            # Highlight the new transaction rows in red with white text
            for i in range(len(current_data_no_balance)):
                self.ledger_sheet.highlight_row(i, bg="white", fg="black")
            for i in range(self.start_idx, self.end_idx):
                self.ledger_sheet.highlight_row(i, bg="red", fg="white")
            
            self.mode = "add"
            self.account_selector.set_enabled(False)
            self.fund_selector.set_enabled(False)
            self.ledger_sheet.set_all_readonly(True)
            
            # Make the highlighted red rows editable
            self.ledger_sheet.set_row_readonly(
                self.start_idx, self.end_idx, False
            )
            
            # Make ID columns (SplitId and TransactionsId) readonly in editable rows
            for row in range(self.start_idx, self.end_idx):
                self.ledger_sheet.sheet.readonly(row, 0, readonly=True)  # SplitId column
                self.ledger_sheet.sheet.readonly(row, 1, readonly=True)  # TransactionsId column
            
            # Set up edit validation to synchronize user_date and description
            self.ledger_sheet.sheet.edit_validation(self.after_cell_edit)
            
            # Set focus to Description column (column 3) of the first editable row
            self.ledger_sheet.sheet.set_currently_selected(self.start_idx, 3)
            
            # Hide Add Transaction button and show add mode buttons
            self.edit_mode_manager.hide_edit_buttons()
            self.edit_mode_manager.show_add_mode_buttons()
            
            if _DEBUG:
                print(f"Entered add mode: start_idx={self.start_idx}, end_idx={self.end_idx}")
    
    def after_cell_edit(self, event):
        """Handle cell edit events with validation and sync across editable rows."""
        if self.mode in ["edit", "add"] and self.start_idx <= event.row < self.end_idx:
            # Get the edited value from the event
            edited_value = event.value
            
            # Get current data to access old value if needed
            current_data = self.ledger_sheet.get_current_data()
            old_value = current_data[event.row][event.column]

            # Check if user_date (column 2) was edited
            if event.column == 2:  # UserDate column
                # Validate date format
                if not self._is_valid_date(edited_value):
                    if _DEBUG:
                        print(f"Invalid date format: {edited_value}, keeping old value: {old_value}")
                    return old_value
                
                # Update user_date in all editable rows
                for i in range(self.start_idx, self.end_idx):
                    if i != event.row:  # Don't overwrite the cell being edited
                        self.ledger_sheet.sheet.set_cell_data(i, 2, edited_value)
                # Update stored user_date
                self.selected_user_date = edited_value
                if _DEBUG:
                    print(f"Updated user_date in all editable rows to: {edited_value}")

            elif event.column == 3:  # Description column
                # Update description in all editable rows
                for i in range(self.start_idx, self.end_idx):
                    if i != event.row:  # Don't overwrite the cell being edited
                        self.ledger_sheet.sheet.set_cell_data(i, 3, edited_value)
                # Update stored description
                self.selected_description = edited_value
                if _DEBUG:
                    print(f"Updated description in all editable rows to: {edited_value}")
            
            elif event.column == 6:  # Amount column
                # Validate that amount is a valid number
                if not self._is_valid_amount(edited_value):
                    if _DEBUG:
                        print(f"Invalid amount format: {edited_value}, keeping old value: {old_value}")
                    return old_value

        # Return the edited value to allow the edit to proceed normally
        return event.value
    
    def _is_valid_date(self, date_string):
        """Validate that the date string is in a valid format."""
        if not date_string or not isinstance(date_string, str):
            return False
        
        # Common date formats to try
        date_formats = [
            "%Y-%m-%d",      # 2025-07-20
            "%Y/%m/%d",      # 2025/07/20
            "%m/%d/%Y",      # 07/20/2025
            "%m-%d-%Y",      # 07-20-2025
            "%d/%m/%Y",      # 20/07/2025
            "%d-%m-%Y",      # 20-07-2025
        ]
        
        for date_format in date_formats:
            try:
                datetime.strptime(date_string.strip(), date_format)
                return True
            except ValueError:
                continue
        
        return False
    
    def _is_valid_amount(self, amount_string):
        """Validate that the amount string is a valid number."""
        if not amount_string:
            return True  # Empty string is allowed (will be treated as 0)
        
        try:
            # Try to convert to float
            float(amount_string)
            return True
        except (ValueError, TypeError):
            return False
    
    def save_edit_mode(self):
        """Save the edited or new transaction data to the database."""
        if self.mode in ["edit", "add"]:
            current_data = self.ledger_sheet.get_current_data()
            
            # Validate that transaction amounts sum to zero
            if not self._validate_transaction_balance(current_data):
                messagebox.showwarning(
                    "Transaction Not Balanced",
                    "The sum of all amounts in the current transaction should equal zero. "
                    "Please use the balance split button to achieve this."
                )
                return
            
            # Use stored transaction details
            user_date = self.selected_user_date
            description = self.selected_description
            
            # Collect splits data
            splits_data = self._collect_splits_data(current_data)
            
            # Save to database - different logic for edit vs add mode
            if self.mode == "edit":
                # Edit mode: update existing transaction (soft delete old, insert new)
                success = self.db_manager.save_transaction(
                    self.selected_tran_id, 
                    user_date, 
                    description, 
                    splits_data
                )
            else:  # add mode
                # Add mode: insert new transaction without deleting anything
                success = self.db_manager.add_new_transaction(
                    user_date, 
                    description, 
                    splits_data
                )
            
            if success:
                self.cancel_edit_mode()  # This will also handle add mode cleanup
            else:
                mode_name = "save" if self.mode == "edit" else "create"
                print(f"Failed to {mode_name} transaction")
    
    def _validate_transaction_balance(self, current_data):
        """Validate that the transaction amounts sum to zero."""
        total_amount = 0.0
        
        for i in range(self.start_idx, self.end_idx):
            try:
                amount_str = current_data[i][6]  # Amount column
                amount = float(amount_str)
                total_amount += amount
            except (ValueError, IndexError):
                if _DEBUG:
                    print(f"Could not parse amount in row {i}: {amount_str}")
                # For validation purposes, treat invalid amounts as 0
                continue
        
        # Check if the sum is close to zero (accounting for floating point precision)
        is_balanced = abs(total_amount) < 0.01
        
        if _DEBUG:
            print(f"Transaction balance validation: sum = {total_amount:.2f}, "
                  f"balanced = {is_balanced}")
        
        return is_balanced
    
    def _collect_splits_data(self, current_data):
        """Collect splits data from the edited rows."""
        splits_data = []
        for i in range(self.start_idx, self.end_idx):
            row = current_data[i]
            amount = float(row[6])  # Amount column - convert formatted string to float
            fund_choice = row[4]  # FundChoice column
            account_choice = row[5]  # AccountChoice column
            
            # Extract IDs from the choice strings
            fund_id = int(fund_choice.split(':')[0]) if fund_choice else 0
            account_id = int(account_choice.split(':')[0]) if account_choice else 0
            
            splits_data.append({
                'amount': amount,
                'fund_id': fund_id,
                'account_id': account_id
            })
        return splits_data
    
    def cancel_edit_mode(self):
        """Cancel edit/add mode and restore the normal ledger view."""
        print(f"[DEBUG] cancel_edit_mode called, current mode: {self.mode}")
        if self.mode in ["edit", "add"]:
            # Restore original ledger view with balance column
            if self.current_filter_type == "account":
                filter_id = self.account_selector.get_selected_account_id()
            else:
                filter_id = self.fund_selector.get_selected_fund_id()
            self.ledger_sheet.update_data(filter_id, filter_type=self.current_filter_type, include_balance=True)
            
            # Reset all rows to white background and black foreground
            current_data = self.ledger_sheet.get_current_data()
            for i in range(len(current_data)):
                self.ledger_sheet.highlight_row(i, bg="white", fg="black")
            
            self.mode = "initial"
            self.account_selector.set_enabled(True)
            self.fund_selector.set_enabled(True)
            self.selected_row = None
            self.selected_tran_id = None
            self.selected_user_date = None
            self.selected_description = None
            # Clear edit validation
            try:
                self.ledger_sheet.sheet.edit_validation(lambda event: True)
            except:
                pass  # Ignore if edit_validation doesn't work with None
            
            # Hide edit mode buttons
            print("[DEBUG] About to hide edit buttons")
            self.edit_mode_manager.hide_edit_buttons()
            print("[DEBUG] Edit buttons hidden")
            self.ledger_sheet.set_all_readonly(True)
            
            # Show Add Transaction button when returning to initial mode
            print("[DEBUG] About to show Add Transaction button")
            self.edit_mode_manager.show_add_transaction_button()
            print("[DEBUG] Add Transaction button shown")
    
    def add_split_row(self):
        """Add a new split row to the current transaction in edit/add mode after the last selected row."""
        if self.mode in ["edit", "add"]:
            # Get current data
            current_data = self.ledger_sheet.get_current_data()
            
            # Get the currently selected row from the sheet
            selected_cells = self.ledger_sheet.sheet.get_currently_selected()
            if selected_cells:
                last_selected_row = selected_cells[0]  # Get the row index
            else:
                # No selection, default to end of editable rows
                last_selected_row = self.end_idx - 1
            
            # Determine insertion position
            if last_selected_row < self.start_idx:
                # Selected row is before editable rows, insert at start of editable rows
                insert_position = self.start_idx
            elif last_selected_row >= self.end_idx:
                # Selected row is after editable rows, insert at end of editable rows
                insert_position = self.end_idx
            else:
                # Selected row is within editable rows, insert after it
                insert_position = last_selected_row + 1
            
            # Create a new empty row with the same structure as transaction rows
            if self.start_idx < len(current_data):
                # Get current selections from dropdowns
                current_fund_selection = self.fund_selector.selected_fund.get()
                current_account_selection = self.account_selector.selected_account.get()
                
                new_row = [
                    0,  # SplitId (will be set when saved)
                    self.selected_tran_id if self.mode == "edit" else 0,  # TransactionsId
                    self.selected_user_date,  # UserDate (from stored transaction)
                    self.selected_description,  # Description (from stored transaction)
                    current_fund_selection,  # FundChoice (from current fund selector)
                    current_account_selection,  # AccountChoice (from current account selector)
                    "0.00"  # Amount (empty)
                ]
                
                # Insert the new row at the determined position
                new_data = current_data[:insert_position] + [new_row] + current_data[insert_position:]
                
                # Update the sheet with new data
                self.ledger_sheet.sheet.set_sheet_data(new_data)
                
                # Update end_idx to include the new row
                self.end_idx += 1
                
                # Re-setup dropdowns for all editable rows
                self.ledger_sheet.setup_dropdowns(self.start_idx, self.end_idx)
                
                # Re-highlight all rows to include the new row
                for i in range(0, self.start_idx):
                    self.ledger_sheet.highlight_row(i, bg="white", fg="black")
                for i in range(self.start_idx, self.end_idx):
                    self.ledger_sheet.highlight_row(i, bg="red", fg="white")
                for i in range(self.end_idx, len(new_data)):
                    self.ledger_sheet.highlight_row(i, bg="white", fg="black")
                
                # Make all transaction rows editable (including the new one)
                self.ledger_sheet.set_all_readonly(True)
                self.ledger_sheet.set_row_readonly(self.start_idx, self.end_idx, False)
                
                # Make ID columns readonly in all editable rows (including new one)
                for row in range(self.start_idx, self.end_idx):
                    self.ledger_sheet.sheet.readonly(row, 0, readonly=True)  # SplitId column
                    self.ledger_sheet.sheet.readonly(row, 1, readonly=True)  # TransactionsId column
                
                # Set focus to FundChoice column (column 4) of the new row
                self.ledger_sheet.sheet.set_currently_selected(insert_position, 4)
                
                if _DEBUG:
                    print(f"Added new split row at index {insert_position}, new end_idx: {self.end_idx}, last_selected_row: {last_selected_row}")
    
    def delete_split_row(self):
        """Delete the currently selected split row in edit/add mode."""
        if self.mode in ["edit", "add"]:
            # Get the currently selected row from the sheet
            selected_cells = self.ledger_sheet.sheet.get_currently_selected()
            if not selected_cells:
                if _DEBUG:
                    print("No row selected for deletion")
                return
            
            selected_row = selected_cells[0]  # Get the row index
            
            # Check if the selected row is within the editable transaction range
            if not (self.start_idx <= selected_row < self.end_idx):
                if _DEBUG:
                    print(f"Selected row {selected_row} is not in editable range ({self.start_idx}-{self.end_idx-1})")
                return
            
            # Check if this is the last remaining split
            if self.end_idx - self.start_idx <= 1:
                if _DEBUG:
                    print("Cannot delete the last remaining split in a transaction")
                return
            
            # Get current data
            current_data = self.ledger_sheet.get_current_data()
            
            # Remove the selected row
            new_data = current_data[:selected_row] + current_data[selected_row + 1:]
            
            # Update the sheet with new data
            self.ledger_sheet.sheet.set_sheet_data(new_data)
            
            # Update end_idx (one less row now)
            self.end_idx -= 1
            
            # Re-setup dropdowns for all remaining editable rows
            self.ledger_sheet.setup_dropdowns(self.start_idx, self.end_idx)
            
            # Re-highlight all rows
            for i in range(0, self.start_idx):
                self.ledger_sheet.highlight_row(i, bg="white", fg="black")
            for i in range(self.start_idx, self.end_idx):
                self.ledger_sheet.highlight_row(i, bg="red", fg="white")
            for i in range(self.end_idx, len(new_data)):
                self.ledger_sheet.highlight_row(i, bg="white", fg="black")
            
            # Make all transaction rows editable (excluding the deleted one)
            self.ledger_sheet.set_all_readonly(True)
            self.ledger_sheet.set_row_readonly(self.start_idx, self.end_idx, False)
            
            if _DEBUG:
                print(f"Deleted split row at index {selected_row}, "
                      f"new end_idx: {self.end_idx}")

    def balance_split_row(self):
        """Balance the currently selected split to make transaction sum to zero."""
        if self.mode in ["edit", "add"]:
            # Get the currently selected row from the sheet
            selected_cells = self.ledger_sheet.sheet.get_currently_selected()
            if not selected_cells:
                if _DEBUG:
                    print("No row selected for balancing")
                return

            selected_row = selected_cells[0]  # Get the row index

            # Check if the selected row is within the editable transaction range
            if not (self.start_idx <= selected_row < self.end_idx):
                if _DEBUG:
                    print(f"Selected row {selected_row} is not in editable range "
                          f"({self.start_idx}-{self.end_idx-1})")
                return

            # Get current data
            current_data = self.ledger_sheet.get_current_data()

            # Calculate the sum of all amounts except the selected row
            total_other_amounts = 0.0
            for i in range(self.start_idx, self.end_idx):
                if i != selected_row:
                    try:
                        amount_str = current_data[i][6]  # Amount column
                        amount = float(amount_str)
                        total_other_amounts += amount
                    except (ValueError, IndexError):
                        if _DEBUG:
                            print(f"Could not parse amount in row {i}: {amount_str}")
                        continue

            # Calculate the balancing amount (negative of the sum)
            balancing_amount = -total_other_amounts

            # Set the balancing amount in the selected row
            formatted_amount = f"{balancing_amount:.2f}"
            self.ledger_sheet.sheet.set_cell_data(selected_row, 6, formatted_amount)

            if _DEBUG:
                print(f"Balanced row {selected_row}: set amount to {formatted_amount} "
                      f"(sum of others: {total_other_amounts:.2f})")

    def delete_transaction(self):
        """Soft delete the current transaction being edited."""
        if self.mode == "edit" and self.selected_tran_id:
            # Ask for confirmation before deleting
            result = messagebox.askyesno(
                "Delete Transaction",
                f"Are you sure you want to delete transaction {self.selected_tran_id}?\n\n"
                f"Date: {self.selected_user_date}\n"
                f"Description: {self.selected_description}\n\n"
                f"This action cannot be undone."
            )
            
            if result:
                # Perform soft delete in database
                success = self.db_manager.soft_delete_transaction(self.selected_tran_id)
                
                if success:
                    if _DEBUG:
                        print(f"Successfully soft deleted transaction {self.selected_tran_id}")
                    
                    # Exit edit mode and refresh the view
                    self.cancel_edit_mode()
                    
                    # Refresh the current view to hide the deleted transaction
                    if self.current_filter_type == "account":
                        self.update_table_with_account()
                    else:
                        self.update_table_with_fund()
                        
                    # Show success message
                    messagebox.showinfo(
                        "Transaction Deleted",
                        f"Transaction {self.selected_tran_id} has been successfully deleted."
                    )
                else:
                    # Show error message
                    messagebox.showerror(
                        "Delete Failed",
                        f"Failed to delete transaction {self.selected_tran_id}. "
                        f"Please try again."
                    )
            else:
                if _DEBUG:
                    print("Transaction deletion cancelled by user")
    
    def _get_row_from_coordinates(self, y_coordinate):
        """Estimate row index from y coordinate."""
        try:
            # Try using tksheet's internal methods if available
            sheet = self.ledger_sheet.sheet
            # Approximate row height (this is a rough estimate)
            header_height = 25  # Approximate header height
            row_height = 20     # Approximate row height
            
            if y_coordinate > header_height:
                estimated_row = int((y_coordinate - header_height) / row_height)
                current_data = self.ledger_sheet.get_current_data()
                if 0 <= estimated_row < len(current_data):
                    return estimated_row
            return None
        except:
            return None
