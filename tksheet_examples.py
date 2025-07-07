"""
tksheet Examples - Working code you can run and modify
"""

import tkinter as tk
from tksheet import Sheet, float_formatter, int_formatter, percentage_formatter
import random
from datetime import datetime

class BasicExample:
    """Basic tksheet setup and usage"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic tksheet Example")
        self.root.geometry("800x600")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sample data
        data = [
            ["John Doe", 30, "Engineer", 75000.50],
            ["Jane Smith", 25, "Designer", 65000.00],
            ["Bob Johnson", 35, "Manager", 85000.75],
            ["Alice Brown", 28, "Developer", 70000.25]
        ]
        
        headers = ["Name", "Age", "Position", "Salary"]
        
        # Create sheet
        self.sheet = Sheet(
            self.root,
            data=data,
            headers=headers,
            theme="light blue"
        )
        
        # Enable bindings
        self.sheet.enable_bindings("all")
        
        # Grid the sheet
        self.sheet.grid(row=0, column=0, sticky="nswe")
        
        # Apply some formatting
        self.setup_formatting()
    
    def setup_formatting(self):
        # Format salary column as currency
        self.sheet["D:D"].format(float_formatter(decimals=2))
        
        # Center align age column
        self.sheet["B:B"].align("center")
        
        # Highlight header
        self.sheet.span(header=True, table=False).highlight(bg="darkblue", fg="white")
    
    def run(self):
        self.root.mainloop()


class InteractiveExample:
    """Example with dropdowns, checkboxes, and event handling"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interactive tksheet Example")
        self.root.geometry("900x700")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", relief="sunken", anchor="w")
        self.status_label.grid(row=0, column=0, sticky="ew", padx=5, pady=2)
        
        # Create sheet with sample data
        self.create_sheet()
        
        # Setup interactive features
        self.setup_interactive_features()
        
        # Setup event handling
        self.setup_events()
    
    def create_sheet(self):
        # Sample task data
        data = [
            ["Task 1", "High", False, 0.8, "John"],
            ["Task 2", "Medium", True, 0.5, "Jane"],
            ["Task 3", "Low", False, 0.2, "Bob"],
            ["Task 4", "High", True, 0.9, "Alice"],
            ["Task 5", "Medium", False, 0.3, "John"]
        ]
        
        headers = ["Task Name", "Priority", "Complete", "Progress", "Assignee"]
        
        self.sheet = Sheet(
            self.root,
            data=data,
            headers=headers,
            theme="light green"
        )
        
        self.sheet.enable_bindings("all")
        self.sheet.grid(row=1, column=0, sticky="nswe")
    
    def setup_interactive_features(self):
        # Priority dropdown
        priorities = ["Low", "Medium", "High", "Critical"]
        self.sheet["B:B"].dropdown(
            values=priorities,
            selection_function=self.on_priority_change
        )
        
        # Completion checkbox
        self.sheet["C:C"].checkbox(
            text="Done",
            check_function=self.on_completion_change
        )
        
        # Progress as percentage
        self.sheet["D:D"].format(percentage_formatter(decimals=0))
        
        # Assignee dropdown
        assignees = ["John", "Jane", "Bob", "Alice", "Charlie"]
        self.sheet["E:E"].dropdown(values=assignees)
        
        # Color code priority column
        self.color_code_priorities()
    
    def color_code_priorities(self):
        """Color code rows based on priority"""
        priority_colors = {
            "Low": {"bg": "lightgreen"},
            "Medium": {"bg": "yellow"},
            "High": {"bg": "orange"},
            "Critical": {"bg": "red", "fg": "white"}
        }
        
        data = self.sheet.get_sheet_data()
        for i, row in enumerate(data):
            if len(row) > 1:
                priority = row[1]
                if priority in priority_colors:
                    self.sheet[i].highlight(**priority_colors[priority])
    
    def setup_events(self):
        self.sheet.bind("<<SheetModified>>", self.on_sheet_modified)
        self.sheet.edit_validation(self.validate_input)
    
    def on_priority_change(self, event):
        self.status_label.config(text=f"Priority changed to {event.value}")
        # Re-apply color coding
        self.color_code_priorities()
    
    def on_completion_change(self, event):
        status = "completed" if event.value else "pending"
        self.status_label.config(text=f"Task marked as {status}")
    
    def on_sheet_modified(self, event):
        self.status_label.config(text=f"Sheet modified: {event.eventname}")
    
    def validate_input(self, event):
        # Validate progress values (column 3)
        if event.column == 3:
            try:
                value = float(event.value)
                if 0 <= value <= 1:
                    return value
                else:
                    self.status_label.config(text="Progress must be between 0 and 1")
                    return None
            except ValueError:
                self.status_label.config(text="Progress must be a number")
                return None
        
        return event.value
    
    def run(self):
        self.root.mainloop()


class DataManipulationExample:
    """Example showing data manipulation, filtering, and analysis"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Manipulation Example")
        self.root.geometry("1000x700")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Control frame
        self.create_controls()
        
        # Create sheet with sample sales data
        self.create_sales_sheet()
        
        # Setup events
        self.setup_events()
    
    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Buttons
        tk.Button(control_frame, text="Add Random Sale", 
                 command=self.add_random_sale).pack(side="left", padx=2)
        tk.Button(control_frame, text="Calculate Totals", 
                 command=self.calculate_totals).pack(side="left", padx=2)
        tk.Button(control_frame, text="Filter High Value", 
                 command=self.filter_high_value).pack(side="left", padx=2)
        tk.Button(control_frame, text="Show All", 
                 command=self.show_all).pack(side="left", padx=2)
        tk.Button(control_frame, text="Sort by Amount", 
                 command=self.sort_by_amount).pack(side="left", padx=2)
    
    def create_sales_sheet(self):
        # Generate sample sales data
        products = ["Widget A", "Widget B", "Gadget X", "Tool Z", "Device Y"]
        customers = ["ACME Corp", "Beta Inc", "Gamma LLC", "Delta Co", "Echo Ltd"]
        
        data = []
        for i in range(20):
            data.append([
                f"S{i+1:03d}",  # Sale ID
                random.choice(products),
                random.choice(customers),
                random.randint(1, 10),  # Quantity
                round(random.uniform(10, 500), 2),  # Unit Price
                0  # Total (calculated)
            ])
        
        # Calculate totals
        for row in data:
            row[5] = round(row[3] * row[4], 2)
        
        headers = ["Sale ID", "Product", "Customer", "Quantity", "Unit Price", "Total"]
        
        self.sheet = Sheet(
            self.root,
            data=data,
            headers=headers,
            theme="dark blue"
        )
        
        self.sheet.enable_bindings("all")
        self.sheet.grid(row=1, column=0, sticky="nswe")
        
        # Format currency columns
        self.sheet["E:E"].format(float_formatter(decimals=2))  # Unit Price
        self.sheet["F:F"].format(float_formatter(decimals=2))  # Total
        
        # Center align quantity
        self.sheet["D:D"].align("center")
        
        # Highlight high-value sales
        self.highlight_high_value()
    
    def highlight_high_value(self):
        """Highlight sales over $1000"""
        data = self.sheet.get_sheet_data()
        for i, row in enumerate(data):
            if len(row) > 5 and isinstance(row[5], (int, float)) and row[5] > 1000:
                self.sheet[i].highlight(bg="gold")
    
    def add_random_sale(self):
        products = ["Widget A", "Widget B", "Gadget X", "Tool Z", "Device Y"]
        customers = ["ACME Corp", "Beta Inc", "Gamma LLC", "Delta Co", "Echo Ltd"]
        
        # Get current data length for new ID
        current_data = self.sheet.get_sheet_data()
        new_id = f"S{len(current_data)+1:03d}"
        
        # Create new sale
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10, 500), 2)
        total = round(quantity * unit_price, 2)
        
        new_sale = [
            new_id,
            random.choice(products),
            random.choice(customers),
            quantity,
            unit_price,
            total
        ]
        
        # Insert at end
        self.sheet.insert_row(row=new_sale)
        self.highlight_high_value()
    
    def calculate_totals(self):
        """Calculate and display summary statistics"""
        data = self.sheet.get_sheet_data()
        
        total_sales = sum(row[5] for row in data if len(row) > 5 and isinstance(row[5], (int, float)))
        avg_sale = total_sales / len(data) if data else 0
        max_sale = max((row[5] for row in data if len(row) > 5 and isinstance(row[5], (int, float))), default=0)
        
        # Add summary row
        summary = ["TOTAL", "", "", "", "", total_sales]
        self.sheet.insert_row(row=summary)
        
        # Highlight summary row
        last_row = len(self.sheet.get_sheet_data()) - 1
        self.sheet[last_row].highlight(bg="lightblue", fg="darkblue")
        
        print(f"Total Sales: ${total_sales:.2f}")
        print(f"Average Sale: ${avg_sale:.2f}")
        print(f"Largest Sale: ${max_sale:.2f}")
    
    def filter_high_value(self):
        """Show only sales over $500"""
        data = self.sheet.get_sheet_data()
        high_value_rows = []
        
        for i, row in enumerate(data):
            if len(row) > 5 and isinstance(row[5], (int, float)) and row[5] > 500:
                high_value_rows.append(i)
        
        if high_value_rows:
            self.sheet.display_rows(rows=high_value_rows, all_displayed=False)
    
    def show_all(self):
        """Show all rows"""
        self.sheet.display_rows("all")
    
    def sort_by_amount(self):
        """Sort by total amount descending"""
        # Get current selection for reference
        self.sheet.sort_columns_by_row(row=None)  # This will sort by currently selected column
        # For more control, you'd implement custom sorting
    
    def setup_events(self):
        self.sheet.bind("<<SheetModified>>", self.on_modification)
    
    def on_modification(self, event):
        # Recalculate totals when quantity or unit price changes
        if event.eventname == "edit_table":
            for (row, col), old_value in event.cells.table.items():
                if col in [3, 4]:  # Quantity or Unit Price columns
                    self.recalculate_row_total(row)
    
    def recalculate_row_total(self, row_idx):
        """Recalculate total for a specific row"""
        try:
            quantity = self.sheet[row_idx, 3].data
            unit_price = self.sheet[row_idx, 4].data
            
            if isinstance(quantity, (int, float)) and isinstance(unit_price, (int, float)):
                total = round(quantity * unit_price, 2)
                self.sheet[row_idx, 5].data = total
        except Exception as e:
            print(f"Error recalculating total for row {row_idx}: {e}")
    
    def run(self):
        self.root.mainloop()


class FormattingExample:
    """Example showing various formatting options"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Formatting Example")
        self.root.geometry("800x600")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.create_formatted_sheet()
    
    def create_formatted_sheet(self):
        # Sample financial data
        data = [
            ["Q1 Revenue", 150000.50, 0.15, True, "Excellent"],
            ["Q2 Revenue", 175000.75, 0.18, True, "Good"],
            ["Q3 Revenue", 160000.25, -0.05, False, "Fair"],
            ["Q4 Revenue", 180000.00, 0.12, True, "Excellent"],
            ["Annual Total", 665001.50, 0.10, True, "Good"]
        ]
        
        headers = ["Item", "Amount ($)", "Growth (%)", "Target Met", "Rating"]
        
        self.sheet = Sheet(
            self.root,
            data=data,
            headers=headers,
            theme="light green"
        )
        
        self.sheet.enable_bindings("all")
        self.sheet.grid(row=0, column=0, sticky="nswe")
        
        self.apply_formatting()
    
    def apply_formatting(self):
        # Format amounts as currency
        self.sheet["B:B"].format(float_formatter(decimals=2))
        
        # Format growth as percentage
        self.sheet["C:C"].format(percentage_formatter(decimals=1))
        
        # Checkboxes for target met
        self.sheet["D:D"].checkbox(text="Met")
        
        # Dropdown for ratings
        self.sheet["E:E"].dropdown(values=["Poor", "Fair", "Good", "Excellent"])
        
        # Conditional formatting based on growth
        data = self.sheet.get_sheet_data()
        for i, row in enumerate(data):
            if len(row) > 2 and isinstance(row[2], (int, float)):
                if row[2] > 0.15:  # High growth
                    self.sheet[i, 2].highlight(bg="lightgreen")
                elif row[2] < 0:  # Negative growth
                    self.sheet[i, 2].highlight(bg="lightcoral")
        
        # Highlight header
        self.sheet.span(header=True, table=False).highlight(bg="darkgreen", fg="white")
        
        # Highlight total row
        self.sheet[4].highlight(bg="lightyellow")
        
        # Align columns
        self.sheet["B:B"].align("right")  # Currency right-aligned
        self.sheet["C:C"].align("center") # Percentages centered
        self.sheet["D:D"].align("center") # Checkboxes centered
    
    def run(self):
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    # Uncomment the example you want to run
    
    # Basic example
    # app = BasicExample()
    # app.run()
    
    # Interactive example with dropdowns and checkboxes
    # app = InteractiveExample()
    # app.run()
    
    # Data manipulation example
    app = DataManipulationExample()
    app.run()
    
    # Formatting example
    # app = FormattingExample()
    # app.run()
