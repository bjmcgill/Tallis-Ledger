import sqlite3
import pandas as pd
import tkinter as tk
from tksheet import Sheet

class DatabaseManager:
    def __init__(self, db_path="your_ledger.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
    
    def fetch_chart_options(self):
        query = "SELECT Id, Name FROM Chart"
        return pd.read_sql_query(query, self.conn)
    
    def fetch_ledger_data(self, account_id):
        query = f"""
            SELECT
                Split.Id AS SplitId,
                Transactions.Id AS TransactionsId,
                Transactions.UserDate,
                Transactions.Description,
                Transactions.Posted,
                Split.Amount,
                Fund.Id AS FundId,
                Fund.Name AS FundName,
                Chart.Id AS AccountId,
                Chart.Name AS AccountName
            FROM Split
            JOIN Transactions ON Split.Tran_id = Transactions.Id
            LEFT JOIN Fund ON Split.FundId = Fund.Id
            LEFT JOIN Chart ON Split.AccountId = Chart.Id
            WHERE Transactions.Deleted = 0 AND Chart.Id = {account_id}
            ORDER BY Transactions.UserDate, Transactions.Id, Split.Id
        """
        return pd.read_sql_query(query, self.conn)
    
    def close(self):
        self.conn.close()

class ChartSelector:
    def __init__(self, root, db_manager, on_change_callback):
        self.root = root
        self.db_manager = db_manager
        self.on_change_callback = on_change_callback
        
        self.chart_options = self.db_manager.fetch_chart_options()
        self.dropdown_options = [f"{row['Id']} - {row['Name']}" for _, row in self.chart_options.iterrows()]
        self.initial_option = next(option for option in self.dropdown_options if option.startswith("1 -"))
        
        self.selected_chart = tk.StringVar()
        self.selected_chart.set(self.initial_option)
        self.dropdown = tk.OptionMenu(self.root, self.selected_chart, *self.dropdown_options, command=self.on_change_callback)
        self.dropdown.pack(pady=10)
    
    def get_selected_account_id(self):
        return int(self.selected_chart.get().split(" - ")[0])
    
    def set_enabled(self, enabled):
        self.dropdown.config(state="normal" if enabled else "disabled")

class EditModeManager:
    def __init__(self, root, on_exit_callback):
        self.root = root
        self.on_exit_callback = on_exit_callback
        self.buttons = []
    
    def show_edit_buttons(self):
        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.on_exit_callback)
        self.cancel_button.pack(side="left", padx=5, pady=10)
        
        self.save_button = tk.Button(self.root, text="Save Transaction")
        self.save_button.pack(side="left", padx=5, pady=10)
        
        self.delete_split_button = tk.Button(self.root, text="Delete Split")
        self.delete_split_button.pack(side="left", padx=5, pady=10)
        
        self.delete_transaction_button = tk.Button(self.root, text="Delete Transaction")
        self.delete_transaction_button.pack(side="left", padx=5, pady=10)
        
        self.buttons = [self.cancel_button, self.save_button, self.delete_split_button, self.delete_transaction_button]
    
    def hide_edit_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []

class LedgerSheet:
    def __init__(self, root, db_manager, on_cell_click_callback):
        self.root = root
        self.db_manager = db_manager
        self.on_cell_click_callback = on_cell_click_callback
        
        self.display_columns = [
            'UserDate',
            'Description',
            'Posted',
            'Amount',
            'FundId',
            'FundName',
            'AccountId',
            'AccountName'
        ]
        
        self.sheet = Sheet(self.root,
                          data=[],
                          headers=self.display_columns,
                          editable=True)
        self.sheet.enable_bindings(("single_select", "edit_cell"))
        self.sheet.pack(expand=True, fill="both")
        self.sheet.bind("<ButtonRelease-1>", self.on_cell_click_callback)
    
    def update_data(self, account_id):
        full_df = self.db_manager.fetch_ledger_data(account_id)
        self.sheet.set_sheet_data(full_df[self.display_columns].values.tolist())
    
    def highlight_row(self, row_index, bg="red", fg="white"):
        self.sheet.highlight_rows(rows=[row_index], bg=bg, fg=fg)
    
    def get_selected_row(self):
        return self.sheet.get_currently_selected()[0]
    
    def set_row_readonly(self, start_row, end_row=None):
        self.sheet.span(start_row, 0, end_row, None).readonly()
    
    def set_all_readonly(self, readonly=True):
        self.sheet.span(0, 0, None, None).readonly(readonly)

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Split Entry Form")
        
        self.mode = "initial"
        self.selected_row = None
        
        self.db_manager = DatabaseManager()
        self.chart_selector = ChartSelector(root, self.db_manager, self.update_table_with_chart)
        self.edit_mode_manager = EditModeManager(root, self.exit_edit_mode)
        self.ledger_sheet = LedgerSheet(root, self.db_manager, self.enter_edit_mode)
        
        self.update_table_with_chart(self.chart_selector.initial_option)
    
    def update_table_with_chart(self, selected_option=None):
        account_id = self.chart_selector.get_selected_account_id()
        self.ledger_sheet.update_data(account_id)
    
    def enter_edit_mode(self, event=None):
        if self.mode == "initial":
            self.selected_row = self.ledger_sheet.get_selected_row()
            self.ledger_sheet.highlight_row(self.selected_row)
            self.mode = "edit"
            self.chart_selector.set_enabled(False)
            
            self.ledger_sheet.set_row_readonly(0, self.selected_row)
            self.ledger_sheet.set_row_readonly(self.selected_row + 1, None)
            
            self.edit_mode_manager.show_edit_buttons()
            
    
    def exit_edit_mode(self):
        if self.mode == "edit":
            self.ledger_sheet.highlight_row(self.selected_row, bg="white", fg="black")
            self.mode = "initial"
            self.chart_selector.set_enabled(True)
            self.selected_row = None
            self.edit_mode_manager.hide_edit_buttons()
            self.ledger_sheet.set_all_readonly(False)



# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
