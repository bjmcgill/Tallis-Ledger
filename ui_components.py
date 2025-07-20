"""
UI components module for Tallis Ledger.
Contains reusable UI components like selectors and managers.
"""

import tkinter as tk
from tkinter import ttk


class AccountSelector:
    """Manages the account dropdown selection widget."""
    
    def __init__(self, parent_frame, db_manager, on_change_callback):
        self.parent_frame = parent_frame
        self.db_manager = db_manager
        self.on_change_callback = on_change_callback
        
        self.account_options = self.db_manager.fetch_chart_options()
        self.dropdown_options = [f"{row['Id']}:{row['Name']}" for _, row in self.account_options.iterrows()]
        self.initial_option = next(option for option in self.dropdown_options if option.startswith("0:"))
        
        self.selected_account = tk.StringVar()
        self.selected_account.set(self.initial_option)
        
        # Use ttk.Combobox instead of OptionMenu for better styling
        self.dropdown = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.selected_account,
            values=self.dropdown_options,
            state="readonly",
            width=25
        )
        self.dropdown.pack(side="left", padx=(0, 10))
        self.dropdown.bind('<<ComboboxSelected>>', self._on_selection_changed)
    
    def _on_selection_changed(self, event=None):
        """Handle combobox selection change."""
        if self.on_change_callback:
            self.on_change_callback(self.selected_account.get())
    
    def get_selected_account_id(self):
        """Extract the account ID from the selected dropdown option."""
        return int(self.selected_account.get().split(":")[0])
    
    def set_enabled(self, enabled):
        """Enable or disable the dropdown."""
        self.dropdown.config(state="readonly" if enabled else "disabled")


class FundSelector:
    """Manages the fund dropdown selection widget."""
    
    def __init__(self, parent_frame, db_manager, on_change_callback):
        self.parent_frame = parent_frame
        self.db_manager = db_manager
        self.on_change_callback = on_change_callback
        
        self.fund_options = self.db_manager.fetch_fund_options()
        self.dropdown_options = [f"{row['Id']}:{row['Name']}" for _, row in self.fund_options.iterrows()]
        self.initial_option = next(option for option in self.dropdown_options if option.startswith("0:"))
        
        self.selected_fund = tk.StringVar()
        self.selected_fund.set(self.initial_option)
        
        # Use ttk.Combobox instead of OptionMenu for better styling
        self.dropdown = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.selected_fund,
            values=self.dropdown_options,
            state="readonly",
            width=25
        )
        self.dropdown.pack(side="left", padx=(0, 10))
        self.dropdown.bind('<<ComboboxSelected>>', self._on_selection_changed)
    
    def _on_selection_changed(self, event=None):
        """Handle combobox selection change."""
        if self.on_change_callback:
            self.on_change_callback(self.selected_fund.get())
    
    def get_selected_fund_id(self):
        """Extract the fund ID from the selected dropdown option."""
        return int(self.selected_fund.get().split(":")[0])
    
    def set_enabled(self, enabled):
        """Enable or disable the dropdown."""
        self.dropdown.config(state="readonly" if enabled else "disabled")


class EditModeManager:
    """Controls the edit mode UI state and buttons."""
    
    def __init__(self, button_frame, on_exit_callback, on_save_callback=None, application=None):
        self.button_frame = button_frame
        self.on_exit_callback = on_exit_callback
        self.on_save_callback = on_save_callback
        self.application = application
        self.buttons = []
    
    def show_edit_buttons(self):
        """Show the edit mode action buttons with professional styling."""
        # Create a centered container for buttons
        button_container = ttk.Frame(self.button_frame)
        button_container.pack(expand=True)
        
        # Primary action buttons (left side)
        self.cancel_button = ttk.Button(button_container, text="Cancel", command=self.on_exit_callback)
        self.cancel_button.pack(side="left", padx=3, pady=8)
        
        self.save_button = ttk.Button(button_container, text="Save Transaction", 
                                     command=self.on_save_callback, style="Accent.TButton")
        self.save_button.pack(side="left", padx=3, pady=8)
        
        # Split management buttons (middle)
        self.add_split_button = ttk.Button(button_container, text="Add Split", command=self._placeholder_add_split)
        self.add_split_button.pack(side="left", padx=3, pady=8)
        
        self.delete_split_button = ttk.Button(button_container, text="Delete Split", command=self._placeholder_delete_split)
        self.delete_split_button.pack(side="left", padx=3, pady=8)
        
        self.balance_split_button = ttk.Button(button_container, text="Balance Split", command=self._placeholder_balance_split)
        self.balance_split_button.pack(side="left", padx=3, pady=8)
        
        # Transaction management button (right side)
        self.delete_transaction_button = ttk.Button(button_container, text="Delete Transaction", command=self._placeholder_delete_transaction)
        self.delete_transaction_button.pack(side="left", padx=3, pady=8)
        
        self.buttons = [button_container, self.cancel_button, self.save_button, self.add_split_button, 
                       self.delete_split_button, self.balance_split_button, self.delete_transaction_button]
    
    def hide_edit_buttons(self):
        """Hide the edit mode action buttons."""
        for button in self.buttons:
            button.destroy()
        self.buttons = []
    
    def _placeholder_add_split(self):
        """Add a new split row to the current transaction."""
        if self.application and hasattr(self.application, 'add_split_row'):
            self.application.add_split_row()
        else:
            print("Add Split clicked - application reference not available")
    
    def _placeholder_delete_split(self):
        """Delete the currently selected split row."""
        if self.application and hasattr(self.application, 'delete_split_row'):
            self.application.delete_split_row()
        else:
            print("Delete Split clicked - application reference not available")
    
    def _placeholder_balance_split(self):
        """Balance the currently selected split to ensure transaction sums to zero."""
        if self.application and hasattr(self.application, 'balance_split_row'):
            self.application.balance_split_row()
        else:
            print("Balance Split clicked - application reference not available")
    
    def _placeholder_delete_transaction(self):
        """Placeholder for delete transaction functionality."""
        print("Delete Transaction clicked - functionality not implemented yet")