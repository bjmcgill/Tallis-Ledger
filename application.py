"""
Main application module for Tallis Ledger.
Contains the main Application class that coordinates all components.
"""

import tkinter as tk
from tkinter import ttk
from database import DatabaseManager
from ui_components import AccountSelector, FundSelector, EditModeManager
from ledger_sheet import LedgerSheet


_DEBUG = True


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
        except:
            # Fallback: try to maximize using geometry
            try:
                self.root.state('zoomed')
            except:
                # Final fallback: set large window size
                self.root.geometry("1400x900+50+50")
        
        self.mode = "initial"
        self.selected_row = None
        self.selected_tran_id = None
        self.selected_user_date = None
        self.selected_description = None
        self.current_filter_type = "account"  # 'account' or 'fund'
        
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
        self.sheet_container = ttk.Frame(self.main_container, style='SheetContainer.TFrame', relief="sunken", borderwidth=1)
        self.sheet_container.pack(expand=True, fill="both")
        
        # Create the sheet frame inside the container
        self.sheet_frame = tk.Frame(self.sheet_container)  # Keep as tk.Frame for tksheet compatibility
        self.sheet_frame.pack(expand=True, fill="both", padx=2, pady=2)
        
        # Initialize components
        self.db_manager = DatabaseManager()
        
        # Create a centered container for the selectors
        selector_container = ttk.Frame(self.selector_frame)
        selector_container.pack(expand=True, pady=5)
        
        # Add labels and selectors using ttk in centered container
        fund_label = ttk.Label(selector_container, text="Fund:", style='SelectorLabel.TLabel')
        fund_label.pack(side="left", padx=(0, 5))
        
        self.fund_selector = FundSelector(selector_container, self.db_manager, self.update_table_with_fund)
        
        account_label = ttk.Label(selector_container, text="Account:", style='SelectorLabel.TLabel')
        account_label.pack(side="left", padx=(20, 5))
        
        self.account_selector = AccountSelector(selector_container, self.db_manager, self.update_table_with_account)
        self.edit_mode_manager = EditModeManager(self.button_frame, self.cancel_edit_mode, self.save_edit_mode, self)
        self.ledger_sheet = LedgerSheet(self.sheet_frame, self.db_manager, self.enter_edit_mode)
        
        self.update_table_with_account(self.account_selector.initial_option)
        self.ledger_sheet.set_all_readonly(True)
    
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
    
    def update_table_with_account(self, selected_option=None):
        """Update the ledger display when a different account is selected."""
        self.current_filter_type = "account"
        account_id = self.account_selector.get_selected_account_id()
        self.ledger_sheet.update_data(account_id, filter_type="account")
    
    def update_table_with_fund(self, selected_option=None):
        """Update the ledger display when a different fund is selected."""
        self.current_filter_type = "fund"
        fund_id = self.fund_selector.get_selected_fund_id()
        self.ledger_sheet.update_data(fund_id, filter_type="fund")
    
    def enter_edit_mode(self, event=None):
        """Enter edit mode for the selected transaction."""
        if self.mode == "initial":
            self.selected_row = self.ledger_sheet.get_selected_row()
            
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
                ledger_df = self.db_manager.fetch_ledger_data(filter_id, self.current_filter_type)
                
                # Format the ledger data (without balance column)
                formatted_ledger_df = self.ledger_sheet.format_decimal_columns(ledger_df, include_balance=False)
                current_data_no_balance = formatted_ledger_df.values.tolist()
                
                # Fetch all splits for this transaction
                transaction_df = self.db_manager.fetch_transaction_data(self.selected_tran_id)
                
                # Format the transaction data
                formatted_transaction_df = self.ledger_sheet.format_decimal_columns(transaction_df, include_balance=False)
                transaction_data = formatted_transaction_df.values.tolist()
                
                # Combine data: before selected row + transaction data + after selected row
                if _DEBUG:
                    print("Head :", current_data_no_balance[:self.selected_row])
                    print("Transaction data :", transaction_data)
                    print("Tail :", current_data_no_balance[self.selected_row + 1:])

                new_data = (current_data_no_balance[:self.selected_row] + 
                           transaction_data + 
                           current_data_no_balance[self.selected_row + 1:])
                
                # Update headers without balance column
                self.ledger_sheet.sheet.headers(list(formatted_transaction_df.columns))
                self.ledger_sheet.sheet.set_sheet_data(new_data)
                
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
                self.ledger_sheet.set_row_readonly(self.start_idx, self.end_idx, False)  # make transaction rows editable
                
                
                self.edit_mode_manager.show_edit_buttons()
    
    def save_edit_mode(self):
        """Save the edited transaction data to the database."""
        if self.mode == "edit":
            current_data = self.ledger_sheet.get_current_data()
            
            # Use stored transaction details from when edit mode was entered
            user_date = self.selected_user_date
            description = self.selected_description
            
            # Collect splits data
            splits_data = self._collect_splits_data(current_data)
            
            # Save to database
            success = self.db_manager.save_transaction(
                self.selected_tran_id, 
                user_date, 
                description, 
                splits_data
            )
            
            if success:
                self.cancel_edit_mode()
            else:
                print("Failed to save transaction")
    
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
        """Cancel edit mode and restore the normal ledger view."""
        if self.mode == "edit":
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
            self.edit_mode_manager.hide_edit_buttons()
            self.ledger_sheet.set_all_readonly(True)
    
    def add_split_row(self):
        """Add a new split row to the current transaction in edit mode after the last selected row."""
        if self.mode == "edit":
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
                    self.selected_tran_id,  # TransactionsId (from stored transaction)
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
                
                if _DEBUG:
                    print(f"Added new split row at index {insert_position}, new end_idx: {self.end_idx}, last_selected_row: {last_selected_row}")
    
    def delete_split_row(self):
        """Delete the currently selected split row in edit mode."""
        if self.mode == "edit":
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
            
            # Check if this is the last remaining split (don't allow deletion of the last split)
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
                print(f"Deleted split row at index {selected_row}, new end_idx: {self.end_idx}")