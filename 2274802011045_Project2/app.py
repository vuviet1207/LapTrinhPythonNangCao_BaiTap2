import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import psycopg2
from functions import SearchBooks, AddBooks, UpdateBooks, DeleteBooks, DisconnectDB
class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Tabs
        self.tab_control = ttk.Notebook(self.root)
        self.login_tab = tk.Frame(self.tab_control)
        self.search_tab = tk.Frame(self.tab_control)
        self.add_tab = tk.Frame(self.tab_control)
        self.update_tab = tk.Frame(self.tab_control)
        self.delete_tab = tk.Frame(self.tab_control)
        self.file_tab = tk.Frame(self.tab_control)

        self.tab_control.add(self.login_tab, text="Login")
        self.tab_control.add(self.search_tab, text="Tìm kiếm sách")
        self.tab_control.add(self.add_tab, text="Thêm sách")
        self.tab_control.add(self.update_tab, text="Cập nhật sách")
        self.tab_control.add(self.delete_tab, text="Xóa sách")

        self.tab_control.pack(expand=1, fill="both")

        # Hide tabs initially
        self.tab_control.hide(self.search_tab)
        self.tab_control.hide(self.add_tab)
        self.tab_control.hide(self.update_tab)
        self.tab_control.hide(self.delete_tab)

        # Database connection fields
        self.db_name = tk.StringVar(value='sach')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='1234567890')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='sach')

        # Create the login interface
        self.create_login_widgets()

        # Create the add, update, delete interfaces
        self.search_books = SearchBooks(self.search_tab, self)
        self.add_books = AddBooks(self.add_tab, self)
        self.update_books = UpdateBooks(self.update_tab, self)
        self.delete_books = DeleteBooks(self.delete_tab, self)

        self.disconnect_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.disconnect_tab, text="Ngắt kết nối")
        self.disconnect_db = DisconnectDB(self.disconnect_tab, self)

        self.create_file_menu()
    def create_file_menu(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)

        # Create the File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()  # Optional separator
        file_menu.add_command(label="Exit", command=self.exit_app)

        # Add the File menu to the menubar
        menubar.add_cascade(label="File", menu=file_menu)

        # Configure the root window to use the menubar
        self.root.config(menu=menubar)

    def save_data(self):
        # Mở hộp thoại lưu file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",  # Định dạng mặc định
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],  # Các loại file hỗ trợ
            title="Lưu file"
        )

        if file_path:  # Nếu người dùng đã chọn file
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Ví dụ: Lưu dữ liệu từ một biến hoặc danh sách
                    data_to_save = "Dữ liệu ví dụ để lưu vào file"  # Thay thế bằng dữ liệu thực tế
                    file.write(data_to_save)
                messagebox.showinfo("Save", "Dữ liệu đã được lưu thành công!")
            except Exception as e:
                messagebox.showerror("Error", f"Không thể lưu file: {e}")
    def exit_app(self):
        # Hàm thoát ứng dụng
        self.root.quit()

    def create_login_widgets(self):
        # Connection section in login tab
        connection_frame = tk.Frame(self.login_tab)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Kết nối cơ sở dữ liệu thành công!")

            # Show search, add, update, delete book tabs
            self.tab_control.add(self.search_tab, text="Tìm kiếm sách")
            self.tab_control.add(self.add_tab, text="Thêm sách")
            self.tab_control.add(self.update_tab, text="Cập nhật sách")
            self.tab_control.add(self.delete_tab, text="Xóa sách")
            self.tab_control.select(self.search_tab)

            # Load data in all Treeviews
            self.search_books.load_data()
            self.add_books.load_data()
            self.update_books.load_data()
            self.delete_books.load_data()

            # Bind tab change event to load data
            self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

        except Exception as e:
            messagebox.showerror("Error", f"Lỗi xảy ra trong quá trình kết nối cơ sở dữ liệu: {e}")

    def on_tab_change(self, event):
        current_tab = event.widget.tab(event.widget.select(), "text")
        if current_tab == "Tìm kiếm sách":
            self.search_books.load_data()
        elif current_tab == "Thêm sách":
            self.add_books.load_data()
        elif current_tab == "Cập nhật sách":
            self.update_books.load_data()
        elif current_tab == "Xóa sách":
            self.delete_books.load_data()