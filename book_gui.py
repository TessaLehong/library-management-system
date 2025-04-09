import sqlite3
from db_config import LibraryDB
import tkinter as tk
from tkinter import ttk, messagebox


def book_window():
    db = LibraryDB('library.db')

    # Create window object
    book_window = tk.Toplevel()
    book_window.title("Book Management")
    book_window.geometry("1060x700")

    # Input Fields
    # Title
    tk.Label(book_window, text="Title:", font=("Arial", 20)).grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(book_window, font=("Arial", 16))
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    # Author
    tk.Label(book_window, text="Author:", font=("Arial", 20)).grid(row=0, column=3, padx=5, pady=5)
    author_entry = tk.Entry(book_window, font=("Arial", 16))
    author_entry.grid(row=0, column=4, padx=5, pady=5)

    # ISBN
    tk.Label(book_window, text="ISBN:", font=("Arial", 20)).grid(row=1, column=0, padx=5, pady=5)
    isbn_entry = tk.Entry(book_window, font=("Arial", 16))
    isbn_entry.grid(row=1, column=1, padx=5, pady=5)

    # Genre
    tk.Label(book_window, text="Genre:", font=("Arial", 20)).grid(row=1, column=3, padx=5, pady=5)
    genre_entry = tk.Entry(book_window, font=("Arial", 16))
    genre_entry.grid(row=1, column=4, padx=5, pady=5)

    # Availability dropdown
    tk.Label(book_window, text="Availability:", font=("Arial", 20)).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    availability_var = tk.StringVar()
    availability_var.set("Available")
    availability_dropdown = ttk.Combobox(book_window, textvariable=availability_var,
                                         values=["Available", "Checked Out"],
                                         font=("Arial", 16),
                                         state="readonly")
    availability_dropdown.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

    # Sort
    tk.Label(book_window, text='Sort by:', font=("Arial", 20)).grid(
        row=5, column=1, padx=5, pady=5)
    sort_var = tk.StringVar()
    sort_dropdown = ttk.Combobox(book_window, textvariable=sort_var,
                                 values=["Title", "Author", "ISBN", "Genre", "Availability"],
                                 state='readonly',
                                 font=("Arial", 16))
    sort_dropdown.grid(row=5, column=2, padx=5, pady=5)

    # Search
    tk.Label(book_window, text='Search:', font=("Arial", 20)).grid(row=6, column=1, padx=5, pady=5)
    search_entry = tk.Entry(book_window, font=("Arial", 20))
    search_entry.grid(row=6, column=2, padx=5, pady=5)


    # Buttons
    # Add Book
    tk.Button(book_window, text='Add Book', font=("Arial", 16), command=lambda: add_book(),
              bg="#4CAF50", fg="white").grid(row=3, column=0, padx=10)
    # Delete Book
    tk.Button(book_window, text='Delete Book', font=("Arial", 16), command= lambda: delete_book(),
              bg="#f44336", fg="white").grid(row=3, column=2, padx=10)
    # Update Book
    tk.Button(book_window, text='Update Book', font=("Arial", 16), command= lambda: update_book(),
              bg="#2196F3", fg="white").grid(row=3, column=4, padx=10)
    # Sort
    tk.Button(book_window, text='Sort', font=("Arial", 16), command= lambda: sort_books(),
              bg="#9E9E9E", fg="white").grid(row=5, column=3, padx=10)
    # Search
    tk.Button(book_window, text='Search', font=("Arial", 16), command= lambda: search_books(),
              bg="#f1b33e", fg="white").grid(row=6, column=3, padx=10)
    # Clear
    tk.Button(book_window, text='Clear', font=("Arial", 16), command=lambda: clear_fields(),
              bg="#3a7d71", fg="white").grid(row=7, column=0, columnspan=5, padx=5, pady=10)


    # Treeview
    columns = ("id", "title", "author", "isbn", "genre", "availability")
    tree = ttk.Treeview(book_window, columns=columns, show="headings", height=15)
    tree.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='ew')

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, minwidth=100, width=130, anchor="center")


    #Refreshes View
    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for book in db.fetch_books():
            tree.insert("", tk.END, values=book)


    # Enters selected books info into the text fields
    def on_row_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0]) # Fetches selected book's data
            values = item["values"]       # Extract the values from the book

            # Populate the input fields with the selected row's data
            # Title field
            title_entry.delete(0, tk.END)     # Deletes current entry
            title_entry.insert(0, values[1]) # Inserts selected value
            # Author field
            author_entry.delete(0, tk.END)
            author_entry.insert(0, values[2])
            # ISBN field
            isbn_entry.delete(0, tk.END)
            isbn_entry.insert(0, values[3])
            # Genre field
            genre_entry.delete(0, tk.END)
            genre_entry.insert(0, values[4])
            # Availability dropdown
            availability_var.set(values[5])

    # Binds the TreeviewSelect event to the on_row_select function
    tree.bind("<<TreeviewSelect>>", on_row_select)


    #Functions
    def add_book():
        if not title_entry.get() or not author_entry.get() or not isbn_entry.get() or not genre_entry.get():
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            db.add_book(title_entry.get(), author_entry.get(), isbn_entry.get(), genre_entry.get(), availability_var.get())
            refresh_tree()
            messagebox.showinfo("Success", "Book added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Book with this ISBN already exists!")


    def delete_book():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No book selected")
            return

        item = tree.item(selected[0])
        db.delete_book(item["values"][0])
        refresh_tree()


    def update_book():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No book selected")
            return

        item = tree.item(selected[0])
        db.update_book(item['values'][0],
                       title_entry.get(),
                       author_entry.get(),
                       isbn_entry.get(),
                       genre_entry.get(),
                       availability_var.get())
        refresh_tree()


    def sort_books():
        key = sort_var.get()
        if not key:
            messagebox.showwarning("Warning", "Select a field to sort by")
            return

        books = db.fetch_books() # Gives a list of tuples
        # Map field names to tuple index
        index_map = {
            'Title': 1,
            'Author': 2,
            'ISBN': 3,
            'Genre': 4,
            'Availability':5
        }
        idx = index_map.get(key) # Get the column index for the selected sort key
        sorted_books = sorted(books, key=lambda x: str(x[idx]).lower()) # Sort the list of books by the key

        tree.delete(*tree.get_children())
        for book in sorted_books:
            tree.insert("",tk.END, values=book)


    def search_books():
        query = search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Please Enter a Search term")
            return

        books = db.fetch_books()
        results = [book for book in books if query in str(book[1]).lower()  # search title
                   or query in str(book[2]).lower()                         # search author
                   or query in str(book[3]).lower()                         # search isbn
                   or query in str(book[4]).lower()                         # search genre
                   or query in str(book[5]).lower()]                        # search availability

        tree.delete(*tree.get_children())
        for book in results:
            tree.insert("", tk.END, values=book)


    def clear_fields():
        # Clear text entries
        title_entry.delete(0, tk.END),
        author_entry.delete(0, tk.END),
        isbn_entry.delete(0, tk.END),
        genre_entry.delete(0, tk.END),
        search_entry.delete(0, tk.END),

        # Reset dropdowns
        availability_var.set('Available')
        sort_var.set('')

        refresh_tree()


    refresh_tree()
    return book_window
