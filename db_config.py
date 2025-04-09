import sqlite3


class LibraryDB():
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # books db
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    author TEXT NOT NULL,
                                    isbn TEXT UNIQUE NOT NULL,
                                    genre TEXT NOT NULL,
                                    availability TEXT CHECK (availability IN ('Available', 'Checked Out')))''')

        # members db
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    membership_id TEXT UNIQUE NOT NULL,
                                    contact TEXT NOT NULL,
                                    membership_type TEXT CHECK (membership_type IN ('VIP', 'Premium', 'Standard')))''')
        self.conn.commit()


    def add_book(self, title, author, isbn, genre, availability):
        self.cursor.execute('INSERT INTO books VALUES (NULL, ?, ?, ?, ?, ?)',
            (title, author, isbn, genre, availability))
        self.conn.commit()


    def add_member(self, name, membership_id, contact, membership_type):
        self.cursor.execute('INSERT INTO members VALUES (NULL, ?, ?, ?, ?)',
                            (name, membership_id, contact, membership_type))
        self.conn.commit()


    def update_book(self, book_id, title, author, isbn, genre, availability):
        self.cursor.execute(
            'UPDATE books SET title = ?, author = ?, isbn = ?, genre = ?, availability = ? WHERE id = ?',
            (title, author, isbn, genre, availability, book_id))
        self.conn.commit()


    def update_member(self, member_id, name, membership_id, contact, membership_type):
        self.cursor.execute(
            'UPDATE members SET name = ?, membership_id = ?, contact = ?, membership_type = ? WHERE id = ?',
            (name, membership_id, contact, membership_type, member_id))
        self.conn.commit()


    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()


    def delete_member(self, member_id):
        self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.conn.commit()


    def fetch_books(self):
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()


    def fetch_members(self):
        self.cursor.execute('SELECT * FROM members')
        return self.cursor.fetchall()


    # Closes db connection on garbage collection
    def __del__(self):
        self.conn.close()