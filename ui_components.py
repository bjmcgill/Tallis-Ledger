"""
UI components module for Tallis Ledger.
Contains reusable UI components like selectors and managers.
"""

import tkinter as tk


class AccountSelector:
    """Manages the account dropdown selection widget."""
    
    def __init__(self, parent_frame, db_manager, on_change_callback):
        self.parent_frame = parent_frame
        self.db_manager = db_manager
        self.on_change_callback = on_change_callback
        
        self.account_options = self.db_manager.fetch_chart_options()
        self.dropdown_options = [f"{row['Id']} - {row['Name']}" for _, row in self.account_options.iterrows()]
        self.initial_option = next(option for option in self.dropdown_options if option.startswith("0 -"))
        
        self.selected_account = tk.StringVar()
        self.selected_account.set(self.initial_option)
        self.dropdown = tk.OptionMenu(self.parent_frame, self.selected_account, *self.dropdown_options, command=self.on_change_callback)
        self.dropdown.pack(side="left", padx=5, pady=5)
    
    def get_selected_account_id(self):
        """Extract the account ID from the selected dropdown option."""
        return int(self.selected_account.get().split(" - ")[0])
    
    def set_enabled(self, enabled):
        """Enable or disable the dropdown."""
        self.dropdown.config(state="normal" if enabled else "disabled")


class FundSelector:
    """Manages the fund dropdown selection widget."""
    
    def __init__(self, parent_frame, db_manager, on_change_callback):
        self.parent_frame = parent_frame
        self.db_manager = db_manager
        self.on_change_callback = on_change_callback
        
        self.fund_options = self.db_manager.fetch_fund_options()
        self.dropdown_options = [f"{row['Id']} - {row['Name']}" for _, row in self.fund_options.iterrows()]
        self.initial_option = next(option for option in self.dropdown_options if option.startswith("0 -"))
        
        self.selected_fund = tk.StringVar()
        self.selected_fund.set(self.initial_option)
        self.dropdown = tk.OptionMenu(self.parent_frame, self.selected_fund, *self.dropdown_options, command=self.on_change_callback)
        self.dropdown.pack(side="left", padx=5, pady=5)
    
    def get_selected_fund_id(self):
        """Extract the fund ID from the selected dropdown option."""
        return int(self.selected_fund.get().split(" - ")[0])
    
    def set_enabled(self, enabled):
        """Enable or disable the dropdown."""
        self.dropdown.config(state="normal" if enabled else "disabled")


class EditModeManager:
    """Controls the edit mode UI state and buttons."""
    
    def __init__(self, button_frame, on_exit_callback, on_save_callback=None):
        self.button_frame = button_frame
        self.on_exit_callback = on_exit_callback
        self.on_save_callback = on_save_callback
        self.buttons = []
    
    def show_edit_buttons(self):
        """Show the edit mode action buttons."""
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.on_exit_callback)
        self.cancel_button.pack(side="left", padx=5, pady=5)
        
        self.save_button = tk.Button(self.button_frame, text="Save Transaction", command=self.on_save_callback)
        self.save_button.pack(side="left", padx=5, pady=5)
        
        self.delete_split_button = tk.Button(self.button_frame, text="Delete Split")
        self.delete_split_button.pack(side="left", padx=5, pady=5)
        
        self.delete_transaction_button = tk.Button(self.button_frame, text="Delete Transaction")
        self.delete_transaction_button.pack(side="left", padx=5, pady=5)
        
        self.buttons = [self.cancel_button, self.save_button, self.delete_split_button, self.delete_transaction_button]
    
    def hide_edit_buttons(self):
        """Hide the edit mode action buttons."""
        for button in self.buttons:
            button.destroy()
        self.buttons = []