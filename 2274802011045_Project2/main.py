import tkinter as tk
from tkinter import ttk
from app import DatabaseApp

def main():
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
