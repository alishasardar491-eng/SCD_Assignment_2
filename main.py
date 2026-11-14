
def log_operation(func):
    """Decorator to log the start and completion of an operation."""
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Starting: {func.__name__}", flush=True)
        result = func(*args, **kwargs)
        print(f"[LOG] Completed: {func.__name__}", flush=True)
        return result
    return wrapper


# =========================
# BASE CLASS
# =========================

class Book:
    def __init__(self, book_id, title, author, year):
        self.__book_id = str(book_id)
        self.__title = str(title)
        self.__author = str(author)
        self.__year = int(year)
        self.__is_available = True

    @property
    def book_id(self):
        return self.__book_id

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def year(self):
        return self.__year

    @property
    def is_available(self):
        return self.__is_available

    def lend(self):
        if not self.__is_available:
            print("This book is already lent.")
            return False

        self.__is_available = False
        print("Book lent successfully.")
        return True

    def return_book(self):
        if self.__is_available:
            print("This book is already available.")
            return False

        self.__is_available = True
        print("Book returned successfully.")
        return True

    def display_details(self):
        print("\nBook ID:", self.book_id)
        print("Title:", self.title)
        print("Author:", self.author)
        print("Year:", self.year)
        print("Availability:",
              "Available" if self.is_available else "Lent")


# =========================
# PRINTED BOOK SUBCLASS
# =========================

class PrintedBook(Book):
    def __init__(self, book_id, title, author, year, pages):
        super().__init__(book_id, title, author, year)

        self.pages = int(pages)

        if self.pages <= 0:
            raise ValueError("Pages must be greater than zero.")

    def display_details(self):
        super().display_details()
        print("Book Type: Printed Book")
        print("Pages:", self.pages)


# =========================
# EBOOK SUBCLASS
# =========================

class EBook(Book):
    def __init__(self, book_id, title, author, year, file_size):
        super().__init__(book_id, title, author, year)

        self.file_size = float(file_size)

        if self.file_size <= 0:
            raise ValueError("File size must be greater than zero.")

    def display_details(self):
        super().display_details()
        print("Book Type: EBook")
        print("File Size:", self.file_size, "MB")


# =========================
# LIBRARY CLASS
# =========================

class Library:
    def __init__(self):
        self.books = []

    @log_operation
    def add_books(self, *books):
        added = 0

        for book in books:
            if any(existing.book_id == book.book_id
                   for existing in self.books):
                print("Book ID already exists:", book.book_id)
            else:
                self.books.append(book)
                print("Successfully added:", book.title)
                added += 1

        print("Total books added:", added)

    def display_books(self):
        if not self.books:
            print("\nLibrary is empty.")
            return

        print("\n========== LIBRARY BOOKS ==========")

        for book in self.books:
            book.display_details()
            print("-----------------------------------")

    def search_books(self, **kwargs):
        results = self.books.copy()

        for key, value in kwargs.items():
            if key == "title":
                results = [
                    book for book in results
                    if value.lower() in book.title.lower()
                ]

            elif key == "author":
                results = [
                    book for book in results
                    if value.lower() in book.author.lower()
                ]

            elif key == "year":
                results = [
                    book for book in results
                    if book.year == int(value)
                ]

            elif key == "type":
                results = [
                    book for book in results
                    if type(book).__name__.lower() == value.lower()
                ]

            elif key == "available":
                results = [
                    book for book in results
                    if book.is_available == value
                ]

        if not results:
            print("\nNo matching books found.")
        else:
            print("\n========== SEARCH RESULTS ==========")

            for book in results:
                book.display_details()
                print("-----------------------------------")

        return results

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == str(book_id):
                return book

        return None

    @log_operation
    def lend_book(self, book_id):
        book = self.find_book(book_id)

        if book is None:
            print("Book not found.")
            return

        book.lend()

    @log_operation
    def return_book(self, book_id):
        book = self.find_book(book_id)

        if book is None:
            print("Book not found.")
            return

        book.return_book()

    # Generator: books by author
    def books_by_author(self, author):
        for book in self.books:
            if author.lower() in book.author.lower():
                yield book

    # Generator: books by type
    def books_by_type(self, book_type):
        for book in self.books:
            if type(book).__name__.lower() == book_type.lower():
                yield book

    # Generator: available books
    def available_books(self):
        for book in self.books:
            if book.is_available:
                yield book


# =========================
# INPUT VALIDATION
# =========================

def get_text(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Try again.")


def get_integer(message):
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("Please enter a valid whole number.")


def get_positive_float(message):
    while True:
        try:
            value = float(input(message).strip())

            if value > 0:
                return value

            print("Value must be greater than zero.")

        except ValueError:
            print("Please enter a valid number.")


# =========================
# ADD BOOK MENU
# =========================

def add_book_menu(library):
    print("\n========== ADD BOOK ==========")
    print("1. Printed Book")
    print("2. EBook")

    choice = input("Select book type: ").strip()

    if choice not in ("1", "2"):
        print("Invalid book type.")
        return

    book_id = get_text("Enter Book ID: ")

    title = get_text("Enter Book Title: ")

    author = get_text("Enter Author Name: ")

    year = get_integer("Enter Publication Year: ")

    if year <= 0:
        print("Year must be greater than zero.")
        return

    if choice == "1":
        pages = get_integer("Enter Number of Pages: ")

        if pages <= 0:
            print("Pages must be greater than zero.")
            return

        book = PrintedBook(
            book_id, title, author, year, pages
        )

    else:
        file_size = get_positive_float("Enter File Size in MB: ")

        book = EBook(
            book_id, title, author, year, file_size
        )

    library.add_books(book)


# =========================
# SEARCH MENU
# =========================

def search_menu(library):
    print("\n========== SEARCH BOOKS ==========")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by Year")
    print("4. Search by Book Type")
    print("5. Search Available Books")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        title = get_text("Enter title: ")
        library.search_books(title=title)

    elif choice == "2":
        author = get_text("Enter author: ")
        library.search_books(author=author)

    elif choice == "3":
        year = get_integer("Enter year: ")
        library.search_books(year=year)

    elif choice == "4":
        print("1. PrintedBook")
        print("2. EBook")

        book_type = input("Enter book type: ").strip()

        if book_type == "1":
            library.search_books(type="PrintedBook")
        elif book_type == "2":
            library.search_books(type="EBook")
        else:
            print("Invalid book type.")

    elif choice == "5":
        library.search_books(available=True)

    else:
        print("Invalid search choice.")


# =========================
# GENERATOR MENU
# =========================

def generator_menu(library):
    print("\n========== GENERATOR MENU ==========")
    print("1. Books by Author")
    print("2. Books by Type")
    print("3. Available Books")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        author = get_text("Enter author name: ")
        results = library.books_by_author(author)

    elif choice == "2":
        print("1. PrintedBook")
        print("2. EBook")

        book_type = input("Enter book type: ").strip()

        if book_type == "1":
            results = library.books_by_type("PrintedBook")
        elif book_type == "2":
            results = library.books_by_type("EBook")
        else:
            print("Invalid book type.")
            return

    elif choice == "3":
        results = library.available_books()

    else:
        print("Invalid choice.")
        return

    found = False

    for book in results:
        found = True
        book.display_details()
        print("-----------------------------------")

    if not found:
        print("No matching books found.")


# =========================
# MAIN MENU
# =========================

def main():
    library = Library()

    while True:
        try:
            print("\n")
            print("======================================")
            print("       LIBRARY RESOURCE SYSTEM")
            print("======================================")
            print("1. Add Book")
            print("2. Display All Books")
            print("3. Search Books")
            print("4. Lend Book")
            print("5. Return Book")
            print("6. Display Available Books")
            print("7. Generator Menu")
            print("8. Exit")
            print("======================================")

            choice = input("\nEnter your choice: ").strip()

            # Diagnostic message to verify input
            print(
                "\n[DEBUG] Selected option:",
                repr(choice),
                flush=True
            )

            if choice == "1":
                add_book_menu(library)

            elif choice == "2":
                library.display_books()

            elif choice == "3":
                search_menu(library)

            elif choice == "4":
                book_id = get_text("Enter Book ID to lend: ")
                library.lend_book(book_id)

            elif choice == "5":
                book_id = get_text("Enter Book ID to return: ")
                library.return_book(book_id)

            elif choice == "6":
                print("\n========== AVAILABLE BOOKS ==========")

                found = False

                for book in library.available_books():
                    found = True
                    book.display_details()
                    print("-----------------------------------")

                if not found:
                    print("No available books found.")

            elif choice == "7":
                generator_menu(library)

            elif choice == "8":
                print("\nThank you for using the Library System!")
                break

            else:
                print("Invalid menu choice. Select 1-8.")

        except EOFError:
            print("\nInput stream closed. Exiting program.")
            break

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting safely.")
            break

        except Exception as error:
            print("\nAn unexpected error occurred:", error)

            input("\nPress Enter to return to the main menu...")


# =========================
# PROGRAM START
# =========================

if __name__ == "__main__":
    main()
