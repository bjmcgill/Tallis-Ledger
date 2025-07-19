"""
Main application module for Tallis Ledger.
Contains the main Application class that coordinates all components.
"""

import tkinter as tk
from database import DatabaseManager
from ui_components import AccountSelector, FundSelector, EditModeManager
from ledger_sheet import LedgerSheet


_DEBUG = True


class Application:
    """Main controller that coordinates all components."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Split Entry Form")
        
        self.mode = "initial"
        self.selected_row = None
        self.selected_tran_id = None
        self.current_filter_type = "account"  # 'account' or 'fund'
        
        # Create main layout frames
        self.selector_frame = tk.Frame(root)
        self.selector_frame.pack(pady=10)
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)
        
        self.sheet_frame = tk.Frame(root)
        self.sheet_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Initialize components
        self.db_manager = DatabaseManager()
        
        # Add labels for selectors
        fund_label = tk.Label(self.selector_frame, text="Fund:")
        fund_label.pack(side="left", padx=(0, 5))
        
        self.fund_selector = FundSelector(self.selector_frame, self.db_manager, self.update_table_with_fund)
        
        account_label = tk.Label(self.selector_frame, text="Account:")
        account_label.pack(side="left", padx=(10, 5))
        
        self.account_selector = AccountSelector(self.selector_frame, self.db_manager, self.update_table_with_account)
        self.edit_mode_manager = EditModeManager(self.button_frame, self.cancel_edit_mode, self.save_edit_mode)
        self.ledger_sheet = LedgerSheet(self.sheet_frame, self.db_manager, self.enter_edit_mode)
        
        self.update_table_with_account(self.account_selector.initial_option)
        self.ledger_sheet.set_all_readonly(True)
    
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
            
            # Get current data to extract Tran_id
            current_data = self.ledger_sheet.get_current_data()
            if self.selected_row < len(current_data):
                # TransactionsId is at index 1 in the display columns
                self.selected_tran_id = current_data[self.selected_row][1]
                
                # Get data without balance column for edit mode
                if self.current_filter_type == "account":
                    filter_id = self.account_selector.get_selected_account_id()
                else:
                    filter_id = self.fund_selector.get_selected_fund_id()
                ledger_df = self.db_manager.fetch_ledger_data(filter_id, self.current_filter_type)
                current_data_no_balance = ledger_df.values.tolist()
                
                # Fetch all splits for this transaction
                transaction_df = self.db_manager.fetch_transaction_data(self.selected_tran_id)
                transaction_data = transaction_df.values.tolist()
                
                # Combine data: before selected row + transaction data + after selected row
                if _DEBUG:
                    print("Head :", current_data_no_balance[:self.selected_row])
                    print("Transaction data :", transaction_data)
                    print("Tail :", current_data_no_balance[self.selected_row + 1:])

                new_data = (current_data_no_balance[:self.selected_row] + 
                           transaction_data + 
                           current_data_no_balance[self.selected_row + 1:])
                
                # Update headers without balance column
                self.ledger_sheet.sheet.headers(list(transaction_df.columns))
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
            
            # Extract transaction details
            user_date, description = self._extract_transaction_details(current_data)
            
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
    
    def _extract_transaction_details(self, current_data):
        """Extract transaction date and description from the first split row."""
        first_row = current_data[self.start_idx]
        user_date = first_row[2]  # UserDate column
        description = first_row[3]  # Description column
        return user_date, description
    
    def _collect_splits_data(self, current_data):
        """Collect splits data from the edited rows."""
        splits_data = []
        for i in range(self.start_idx, self.end_idx):
            row = current_data[i]
            amount = row[4]  # Amount column
            fund_choice = row[5]  # FundChoice column
            account_choice = row[6]  # AccountChoice column
            
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
            self.edit_mode_manager.hide_edit_buttons()
            self.ledger_sheet.set_all_readonly(True)