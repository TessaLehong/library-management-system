import tkinter as tk
import book_gui
import member_gui

def close_main_window(window):
    window.destroy()
    app.deiconify()


def open_book_window():
    app.withdraw()  # Hide main window
    book_window = book_gui.book_window() # Opens book window
    book_window.protocol("WM_DELETE_WINDOW", lambda: close_main_window(book_window)) # Unhide main window when book window closes


def open_member_window():
    app.withdraw()  # Hide main window
    member_window = member_gui.member_window() # Opens member window
    member_window.protocol("WM_DELETE_WINDOW", lambda: close_main_window(member_window)) # Unhide main window when member window closes


# Create window object
app = tk.Tk()
app.title("Library Management System")
app.geometry("500x400")

# Labels
tk.Label(app, text="Library Management System", font=("bold", 24)).pack(pady=15)

# buttons
tk.Button(app, text="Manage Books", font=("Arial", 20), command=open_book_window, width=20,
          bg="#1c669f", fg="white",).pack(pady=5)
tk.Button(app, text="Manage Members", font=("Arial", 20), command=open_member_window, width=20,
          bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(app, text="Exit", font=("Arial", 20), command=app.quit, width=20,
          bg="#f44336", fg="white").pack(pady=20)

# Start Program
app.mainloop()
