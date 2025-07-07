# tksheet Reference Guide

## Core Classes and Initialization

### Sheet Class
```python
from tksheet import Sheet
import tkinter as tk

# Basic initialization
sheet = Sheet(parent, 
    data=[[row_data...], ...],          # 2D list of data
    headers=["Col1", "Col2", ...],      # Column headers
    index=["Row1", "Row2", ...],        # Row index
    theme="light blue",                 # Theme options
    height=400,                         # Widget height
    width=600                           # Widget width
)
```

### Essential Setup Pattern
```python
def setup_sheet(parent):
    sheet = Sheet(parent, data=[])
    sheet.enable_bindings("all")  # Enable all standard functionality
    sheet.grid(row=0, column=0, sticky="nswe")
    return sheet
```

## Data Operations

### Setting Data
```python
# Set entire sheet data
sheet.set_sheet_data([[1, 2, 3], [4, 5, 6]])

# Set cell data
sheet["A1"].data = "New Value"
sheet[0, 0].data = "Same cell, different notation"

# Set row data
sheet[0].data = ["Row 0 Col 0", "Row 0 Col 1", "Row 0 Col 2"]

# Set column data (transposed)
sheet["A"].transpose().data = ["Col A Row 0", "Col A Row 1", "Col A Row 2"]

# Set range data
sheet["A1:C2"].data = [["A1", "B1", "C1"], ["A2", "B2", "C2"]]
```

### Getting Data
```python
# Get entire sheet data
all_data = sheet.get_sheet_data()

# Get cell data
cell_value = sheet["A1"].data
cell_value = sheet[0, 0].data

# Get row data
row_data = sheet[0].data

# Get column data
col_data = sheet["A"].data

# Get range data
range_data = sheet["A1:C3"].data

# Get selected data
selected_data = sheet.get_selected_cells()
```

## Span Objects (Core Concept)

### Creating Spans
```python
# Cell spans
cell_span = sheet["A1"]
cell_span = sheet[0, 0]
cell_range = sheet["A1:C3"]

# Row spans
row_span = sheet[0]           # Single row
row_range = sheet[0:5]        # Multiple rows
all_rows = sheet[:]           # All rows

# Column spans
col_span = sheet["A"]         # Single column
col_range = sheet["A:C"]      # Multiple columns
all_cols = sheet[None, :, None, None]  # All columns
```

### Span Methods (Chainable)
```python
# Method chaining
sheet["A1"].options(undo=True).highlight(bg="red").align("center")

# Individual operations
span = sheet["A:A"]
span.highlight(bg="yellow", fg="black")
span.align("center")
span.readonly(True)
```

## User Interface Features

### Highlighting
```python
# Cell highlighting
sheet["A1"].highlight(bg="yellow", fg="black")
sheet["A1"].bg = "yellow"  # Shorthand
sheet["A1"].fg = "black"   # Shorthand

# Row highlighting
sheet[0].highlight(bg="lightblue")

# Column highlighting
sheet["A"].highlight(bg="lightgreen")

# Conditional highlighting
for r in range(10):
    if r % 2 == 0:
        sheet[r].highlight(bg="lightgray")
```

### Dropdown Boxes
```python
# Simple dropdown
sheet["A1"].dropdown(values=["Option 1", "Option 2", "Option 3"])

# Dropdown with callback
def on_dropdown_change(event):
    print(f"Selected: {event.value}")

sheet["A1"].dropdown(
    values=["Yes", "No", "Maybe"],
    set_value="No",
    selection_function=on_dropdown_change
)

# Column dropdown
sheet["A:A"].dropdown(values=["Category A", "Category B", "Category C"])
```

### Checkboxes
```python
# Simple checkbox
sheet["B1"].checkbox(checked=True)

# Checkbox with text and callback
def on_checkbox_change(event):
    print(f"Checkbox is now: {event.value}")

sheet["B1"].checkbox(
    checked=False,
    text="Enable Feature",
    check_function=on_checkbox_change
)

# Column of checkboxes
sheet["B:B"].checkbox(checked=False, text="Select")
```

### Data Formatting
```python
from tksheet import float_formatter, int_formatter, percentage_formatter

# Format as float with 2 decimal places
sheet["C:C"].format(float_formatter(decimals=2))

# Format as integer
sheet["D:D"].format(int_formatter())

# Format as percentage
sheet["E:E"].format(percentage_formatter(decimals=1))
```

## Event Handling

### Basic Events
```python
def on_sheet_modified(event):
    print(f"Sheet modified: {event.eventname}")
    print(f"Changed cells: {event.cells}")

# Bind to sheet modification events
sheet.bind("<<SheetModified>>", on_sheet_modified)
```

### Cell Edit Validation
```python
def validate_cell_edit(event):
    # Validate numeric input
    if event.column == 0:  # First column
        try:
            float(event.value)
            return event.value
        except ValueError:
            return None  # Reject the edit
    
    # Uppercase text in second column
    if event.column == 1:
        return event.value.upper()
    
    return event.value

sheet.edit_validation(validate_cell_edit)
```

### Specific Event Bindings
```python
def on_cell_edit(event):
    print(f"Cell edited: ({event.row}, {event.column}) = {event.value}")

def on_cell_select(event):
    print(f"Cell selected: ({event.row}, {event.column})")

# Bind specific events
sheet.extra_bindings("edit_cell", on_cell_edit)
sheet.extra_bindings("cell_select", on_cell_select)
```

## Selection and Navigation

### Getting Selections
```python
# Get currently selected cell
current = sheet.get_currently_selected()
if current:
    print(f"Selected: Row {current.row}, Col {current.column}")

# Get all selected cells
selected_cells = sheet.get_selected_cells()

# Get selected rows/columns
selected_rows = sheet.get_selected_rows()
selected_cols = sheet.get_selected_columns()
```

### Setting Selections
```python
# Select specific cell
sheet.select_cell(row=0, column=0)

# Select row
sheet.select_row(row=2)

# Select column
sheet.select_column(column=1)

# Select range programmatically
sheet.create_selection_box(r1=0, c1=0, r2=3, c2=3, type_="cells")
```

## Row and Column Operations

### Adding/Removing Rows
```python
# Insert row
sheet.insert_row(row=["New", "Row", "Data"], idx=0)  # Insert at beginning
sheet.insert_row()  # Insert empty row at end

# Delete row
sheet.del_row(idx=0)

# Insert multiple rows
sheet.insert_rows(rows=[["Row1"], ["Row2"]], idx=0)
```

### Adding/Removing Columns
```python
# Insert column
sheet.insert_column(column=["New", "Col"], idx=0)  # Insert at beginning
sheet.insert_column()  # Insert empty column at end

# Delete column
sheet.del_column(idx=0)
```

### Resizing
```python
# Auto-resize columns to content
sheet.set_all_cell_sizes_to_text()

# Set specific column width
sheet.column_width(column=0, width=150)

# Set specific row height
sheet.row_height(row=0, height=30)

# Set all columns to same width
sheet.set_all_column_widths(width=100)
```

## Headers and Index

### Working with Headers
```python
# Set headers
sheet.headers(["Name", "Age", "City", "Email"])

# Get headers
current_headers = sheet.headers()

# Header-only operations
sheet["A"].options(table=False, header=True).highlight(bg="blue", fg="white")
```

### Working with Row Index
```python
# Set row index
sheet.row_index(["Item 1", "Item 2", "Item 3"])

# Get row index
current_index = sheet.row_index()

# Index-only operations
sheet[0].options(table=False, index=True).highlight(bg="green")
```

## Advanced Features

### Named Spans (Persistent Rules)
```python
# Create a named span that persists through row/column changes
highlight_span = sheet.span(
    "A:A",
    type_="highlight", 
    name="important_column",
    bg="yellow"
)
sheet.named_span(highlight_span)

# Delete named span
sheet.del_named_span("important_column")
```

### Hiding Rows/Columns
```python
# Hide specific rows
sheet.hide_rows([1, 3, 5])

# Show all rows
sheet.display_rows("all")

# Hide specific columns
sheet.hide_columns([0, 2])

# Show all columns
sheet.display_columns("all")

# Display only specific rows (filtering)
visible_rows = [0, 2, 4, 6]
sheet.display_rows(rows=visible_rows, all_displayed=False)
```

### Readonly Cells
```python
# Make cells readonly
sheet["A:A"].readonly(True)

# Make specific range readonly
sheet["B1:D5"].readonly(True)

# Remove readonly
sheet["A:A"].readonly(False)
```

## Theme and Appearance

### Changing Themes
```python
# Available themes: "light blue", "light green", "dark", "black", "dark blue", "dark green"
sheet.change_theme("dark")
```

### Custom Colors
```python
# Set custom colors
sheet.set_options(
    table_bg="white",
    table_fg="black", 
    table_grid_fg="gray",
    table_selected_cells_bg="lightblue"
)
```

### Text Alignment
```python
# Align entire columns
sheet.align("A:A", align="center")
sheet.align("B:B", align="right")
sheet.align("C:C", align="left")

# Align specific cells
sheet["D1"].align = "center"
```

## Common Patterns and Best Practices

### Complete Application Setup
```python
import tkinter as tk
from tksheet import Sheet

class SpreadsheetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My Spreadsheet App")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create sheet
        self.sheet = Sheet(
            self.root,
            data=[],
            theme="light blue",
            height=600,
            width=800
        )
        
        # Enable functionality
        self.sheet.enable_bindings("all")
        
        # Set up event handlers
        self.setup_events()
        
        # Grid the sheet
        self.sheet.grid(row=0, column=0, sticky="nswe")
    
    def setup_events(self):
        self.sheet.bind("<<SheetModified>>", self.on_data_changed)
        self.sheet.edit_validation(self.validate_input)
    
    def on_data_changed(self, event):
        print("Data was modified")
    
    def validate_input(self, event):
        return event.value  # Accept all input
    
    def run(self):
        self.root.mainloop()

# Usage
app = SpreadsheetApp()
app.run()
```

### Error Handling
```python
def safe_set_data(sheet, row, col, value):
    try:
        sheet[row, col].data = value
    except Exception as e:
        print(f"Error setting data at ({row}, {col}): {e}")

def safe_get_data(sheet, row, col, default=None):
    try:
        return sheet[row, col].data
    except Exception as e:
        print(f"Error getting data at ({row}, {col}): {e}")
        return default
```

### Performance Tips
```python
# For large datasets, disable redraw during bulk operations
sheet.set_options(redraw=False)
for i in range(1000):
    sheet[i, 0].data = f"Row {i}"
sheet.refresh()  # Redraw once at the end

# Use spans for bulk operations
sheet["A:A"].data = [f"Row {i}" for i in range(1000)]
```
