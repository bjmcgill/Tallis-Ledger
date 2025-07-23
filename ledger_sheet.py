"""
Ledger sheet module for Tallis Ledger.
Wraps the tksheet widget and handles data display.
"""

from tksheet import Sheet

_DEBUG = False  # Set to True for debugging output


class LedgerSheet:
    """Wraps the tksheet widget and handles data display."""
    
    def __init__(self, sheet_frame, db_manager, on_cell_click_callback):
        self.sheet_frame = sheet_frame
        self.db_manager = db_manager
        self.on_cell_click_callback = on_cell_click_callback
        
        self.sheet = Sheet(self.sheet_frame,
                          data=[],
                          headers=[],
                          editable=True)
        self.sheet.enable_bindings(("single_select", "edit_cell"))
        self.sheet.pack(expand=True, fill="both")
        self.sheet.bind("<ButtonRelease-1>", self.on_cell_click_callback)
    
    def format_decimal_columns(self, df, include_balance=True):
        """Format Amount and Balance columns to 2 decimal places."""
        formatted_data = df.copy()
        formatted_data['Amount'] = formatted_data['Amount'].apply(lambda x: f"{float(x):.2f}")
        if include_balance and 'Balance' in formatted_data.columns:
            formatted_data['Balance'] = formatted_data['Balance'].apply(lambda x: f"{float(x):.2f}")
        return formatted_data
    
    def update_data(self, filter_id, filter_type='account', include_balance=True):
        """Update the sheet with data for the selected account or fund."""
        full_df = self.db_manager.fetch_ledger_data(filter_id, filter_type)
        
        if include_balance:
            # Add balance column with cumulative sum of Amount column
            full_df['Balance'] = full_df['Amount'].cumsum()
        
        # Format Amount and Balance columns to 2 decimal places
        formatted_data = self.format_decimal_columns(full_df, include_balance)
        
        self.sheet.headers(list(formatted_data.columns))
        self.sheet.set_sheet_data(formatted_data.values.tolist())
        self.set_column_widths()
    
    def highlight_row(self, row_index, bg="red", fg="white"):
        """Highlight a specific row with the given colors."""
        self.sheet.highlight_rows(rows=[row_index], bg=bg, fg=fg)
    
    def get_selected_row(self):
        """Get the currently selected row index."""
        selected = self.sheet.get_currently_selected()
        if selected:
            return selected[0]
        else:
            return None
    
    def get_current_data(self):
        """Get all current sheet data."""
        return self.sheet.get_sheet_data()
    
    def set_row_readonly(self, start_row, end_row=None, readonly=True):
        """Set specific rows to readonly or editable."""
        self.sheet.span(start_row, 0, end_row, None).readonly(readonly)
  
    def set_all_readonly(self, readonly=True):
        """Set all rows to readonly or editable."""
        self.sheet.span(0, 0, None, None).readonly(readonly)
    
    def setup_account_dropdown(self, start_row, end_row):
        """Set up account dropdown for the specified row range."""
        # Get all account options from database
        account_options = self.db_manager.fetch_chart_options()
        dropdown_values = [f"{row['Id']}:{row['Name']}" for _, row in account_options.iterrows()]
        
        # Find the AccountChoice column index
        headers = self.sheet.headers()
        try:
            account_col_idx = headers.index('AccountChoice')
            # Apply dropdown to the AccountChoice column for the specified rows
            for row in range(start_row, end_row):
                # Get the current value in the cell
                current_value = self.sheet[row, account_col_idx].data
                # Set up dropdown with current value selected
                self.sheet[row, account_col_idx].dropdown(
                    values=dropdown_values,
                    set_value=current_value
                )
        except ValueError:
            if _DEBUG:
                print("AccountChoice column not found in headers")
    
    def setup_fund_dropdown(self, start_row, end_row):
        """Set up fund dropdown for the specified row range."""
        # Get all fund options from database
        fund_options = self.db_manager.fetch_fund_options()
        dropdown_values = [f"{row['Id']}:{row['Name']}" for _, row in fund_options.iterrows()]
        
        # Find the FundChoice column index
        headers = self.sheet.headers()
        try:
            fund_col_idx = headers.index('FundChoice')
            # Apply dropdown to the FundChoice column for the specified rows
            for row in range(start_row, end_row):
                # Get the current value in the cell
                current_value = self.sheet[row, fund_col_idx].data
                # Set up dropdown with current value selected
                self.sheet[row, fund_col_idx].dropdown(
                    values=dropdown_values,
                    set_value=current_value
                )
        except ValueError:
            if _DEBUG:
                print("FundChoice column not found in headers")
    
    def setup_dropdowns(self, start_row, end_row):
        """Set up both account and fund dropdowns for the specified row range."""
        self.setup_account_dropdown(start_row, end_row)
        self.setup_fund_dropdown(start_row, end_row)
    
    def set_column_widths(self):
        """Set column widths for the sheet. Modify this method to change column widths."""
        column_widths = {
            'SplitId': 50,
            'TransactionsId': 50,
            'UserDate': 150,
            'Description': 800,
            'FundChoice': 150,
            'AccountChoice': 150,
            'Amount': 150,
            'Balance': 150
        }
        
        headers = self.sheet.headers()
        if headers:
            for i, header in enumerate(headers):
                if header in column_widths:
                    self.sheet.column_width(column=i, width=column_widths[header])