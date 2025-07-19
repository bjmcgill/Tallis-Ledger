"""
Tallis Ledger - Main entry point
A Tkinter-based accounting application with spreadsheet interface.
"""

import tkinter as tk
from application import Application


def main():
    """Main entry point for the Tallis Ledger application."""
    root = tk.Tk()
    app = Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()