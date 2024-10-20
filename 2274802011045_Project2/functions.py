import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from psycopg2 import sql
class SearchBooks:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app

        search_frame = tk.Frame(self.tab)
        search_frame.pack(pady=10)

        self.search_var = tk.StringVar()  # Tìm kiếm theo tên sách

        tk.Label(search_frame, text="Tìm kiếm theo tên sách:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(search_frame, text="Tìm kiếm", command=self.search_data).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(search_frame, text="Tải lại dữ liệu", command=self.load_data).grid(row=0, column=3, padx=5, pady=5)

        # Treeview for displaying search results
        self.data_tree = ttk.Treeview(self.tab, columns=("ID", "Tên sách", "Tác giả", "Năm xuất bản", "Thể loại"), show="headings", height=10)
        self.data_tree.column("ID", width=100, anchor="center")
        self.data_tree.column("Tên sách", width=200, anchor="center")
        self.data_tree.column("Tác giả", width=200, anchor="center")
        self.data_tree.column("Năm xuất bản", width=150, anchor="center")
        self.data_tree.column("Thể loại", width=150, anchor="center")
        self.data_tree.heading("ID", text="ID")
        self.data_tree.heading("Tên sách", text="Tên sách")
        self.data_tree.heading("Tác giả", text="Tác giả")
        self.data_tree.heading("Năm xuất bản", text="Năm xuất bản")
        self.data_tree.heading("Thể loại", text="Thể loại")
        self.data_tree.pack(side="bottom", fill="both", expand=True)

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(query)
            rows = self.app.cur.fetchall()

            # Clear previous data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            # Insert new data into Treeview
            for row in rows:
                self.data_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def search_data(self):
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE ten_sach ILIKE %s").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(search_query, ('%' + self.search_var.get() + '%',))
            rows = self.app.cur.fetchall()

            # Clear previous data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            # Insert search results into Treeview
            for row in rows:
                self.data_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {e}")



class AddBooks:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app

        # Insert section
        insert_frame = tk.Frame(self.tab)
        insert_frame.pack(pady=10)

        self.column1 = tk.StringVar()  # Tên sách
        self.column2 = tk.StringVar()  # Tác giả
        self.column3 = tk.StringVar()  # NXB
        self.column4 = tk.StringVar()  # Thể loại

        tk.Label(insert_frame, text="Tên sách:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Tác giả:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Năm xuất bản:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column3).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Thể loại:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column4).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Thêm sách", command=self.insert_data).grid(row=4, columnspan=2, pady=10)
        tk.Button(insert_frame, text="Tải lại dữ liệu", command=self.load_data).grid(row=5, columnspan=2, pady=10)

        # Treeview for displaying data
        self.data_tree = ttk.Treeview(self.tab, columns=("ID", "Tên sách", "Tác giả", "Năm xuất bản", "Thể loại"), show="headings", height=10)
        self.data_tree.column("ID", width=100, anchor="center")
        self.data_tree.column("Tên sách", width=200, anchor="center")
        self.data_tree.column("Tác giả", width=200, anchor="center")
        self.data_tree.column("Năm xuất bản", width=150, anchor="center")
        self.data_tree.column("Thể loại", width=150, anchor="center")
        self.data_tree.heading("ID", text="ID")
        self.data_tree.heading("Tên sách", text="Tên sách")
        self.data_tree.heading("Tác giả", text="Tác giả")
        self.data_tree.heading("Năm xuất bản", text="Năm xuất bản")
        self.data_tree.heading("Thể loại", text="Thể loại")
        self.data_tree.pack(side="bottom", fill="both", expand=True)

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(query)
            rows = self.app.cur.fetchall()

            # Clear previous data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            # Insert new data into Treeview
            for row in rows:
                self.data_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def insert_data(self):
        try:
            if not self.column1.get() or not self.column2.get():
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin sách!")
                return

            add_query = sql.SQL("INSERT INTO {} (ten_sach, tac_gia, nxb, the_loai) VALUES (%s, %s, %s, %s)").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(add_query, (self.column1.get(), self.column2.get(), self.column3.get(), self.column4.get()))
            self.app.conn.commit()

            messagebox.showinfo("Thành công", "Sách đã được thêm thành công!")
            self.load_data()  # Refresh data after addition
            
        except Exception as e:
            self.app.conn.rollback()  # Rollback the transaction on error
            messagebox.showerror("Lỗi", f"Lỗi thêm sách: {e}")



class UpdateBooks:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app

        # Insert section
        update_frame = tk.Frame(self.tab)
        update_frame.pack(pady=10)

        self.column1 = tk.StringVar()  # ID (disabled)
        self.column2 = tk.StringVar()  # Tên sách
        self.column3 = tk.StringVar()  # Tác giả
        self.column4 = tk.StringVar()  # NXB
        self.column5 = tk.StringVar()  # Thể loại

        tk.Label(update_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(update_frame, textvariable=self.column1, state='disabled')  # ID disabled
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Tên sách:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(update_frame, textvariable=self.column2)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Tác giả:").grid(row=2, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(update_frame, textvariable=self.column3)
        self.author_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Năm xuất bản:").grid(row=3, column=0, padx=5, pady=5)
        self.nxb_entry = tk.Entry(update_frame, textvariable=self.column4)
        self.nxb_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Thể loại:").grid(row=4, column=0, padx=5, pady=5)
        self.the_loai_entry = tk.Entry(update_frame, textvariable=self.column5)
        self.the_loai_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(update_frame, text="Cập nhật dữ liệu", command=self.update_data).grid(row=5, columnspan=2, pady=10)
        tk.Button(update_frame, text="Tải lại dữ liệu", command=self.load_data).grid(row=6, columnspan=2, pady=10)

        # Treeview for displaying data
        self.data_tree = ttk.Treeview(self.tab, columns=("ID", "Tên sách", "Tác giả", "Năm xuất bản", "Thể loại"), show="headings", height=10)
        self.data_tree.column("ID", width=100, anchor="center")
        self.data_tree.column("Tên sách", width=200, anchor="center")
        self.data_tree.column("Tác giả", width=200, anchor="center")
        self.data_tree.column("Năm xuất bản", width=150, anchor="center")
        self.data_tree.column("Thể loại", width=150, anchor="center")
        self.data_tree.heading("ID", text="ID")
        self.data_tree.heading("Tên sách", text="Tên sách")
        self.data_tree.heading("Tác giả", text="Tác giả")
        self.data_tree.heading("Năm xuất bản", text="Năm xuất bản")
        self.data_tree.heading("Thể loại", text="Thể loại")
        self.data_tree.pack(side="bottom", fill="both", expand=True)

        # Bind Treeview click event
        self.data_tree.bind("<ButtonRelease-1>", self.select_item)
    
    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(query)
            rows = self.app.cur.fetchall()

            # Clear previous data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            # Insert new data into Treeview
            for row in rows:
                self.data_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def select_item(self, event):
        # Get selected item from Treeview
        selected_item = self.data_tree.selection()[0]
        item_values = self.data_tree.item(selected_item, 'values')

        # Set the selected values into the Entry widgets
        self.column1.set(item_values[0])  # ID
        self.column2.set(item_values[1])  # Tên sách
        self.column3.set(item_values[2])  # Tác giả
        self.column4.set(item_values[3])  # NXB
        self.column5.set(item_values[4])  # Thể loại

    def update_data(self):
        try:
            if not self.column1.get():
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID của sách cần sửa!")
                return

            update_query = sql.SQL("UPDATE {} SET ten_sach=%s, tac_gia=%s, nxb=%s, the_loai=%s WHERE id=%s").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(update_query, (self.column2.get(), self.column3.get(), self.column4.get(), self.column5.get(), self.column1.get()))

            if self.app.cur.rowcount == 0:  # Kiểm tra số bản ghi bị ảnh hưởng
                messagebox.showwarning("Cảnh báo", "Không có ID nào trùng khớp để sửa!")
            else:
                self.app.conn.commit()
                messagebox.showinfo("Thành công", "Sách đã được sửa thành công!")
                self.load_data()  # Refresh data after update
            
        except Exception as e:
            self.app.conn.rollback()  # Rollback the transaction on error
            messagebox.showerror("Lỗi", f"Lỗi sửa sách: {e}")


class DeleteBooks:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app

        delete_frame = tk.Frame(self.tab)
        delete_frame.pack(pady=10)

        self.id_var = tk.StringVar()  # ID

        tk.Label(delete_frame, text="ID sách để xóa:").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(delete_frame, textvariable=self.id_var)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(delete_frame, text="Xóa sách", command=self.delete_data).grid(row=1, columnspan=2, pady=10)
        tk.Button(delete_frame, text="Tải lại dữ liệu", command=self.load_data).grid(row=2, columnspan=2, pady=10)

        # Treeview for displaying data
        self.data_tree = ttk.Treeview(self.tab, columns=("ID", "Tên sách", "Tác giả", "Năm xuất bản", "Thể loại"), show="headings", height=10)
        self.data_tree.column("ID", width=100, anchor="center")
        self.data_tree.column("Tên sách", width=200, anchor="center")
        self.data_tree.column("Tác giả", width=200, anchor="center")
        self.data_tree.column("Năm xuất bản", width=150, anchor="center")
        self.data_tree.column("Thể loại", width=150, anchor="center")
        self.data_tree.heading("ID", text="ID")
        self.data_tree.heading("Tên sách", text="Tên sách")
        self.data_tree.heading("Tác giả", text="Tác giả")
        self.data_tree.heading("Năm xuất bản", text="Năm xuất bản")
        self.data_tree.heading("Thể loại", text="Thể loại")
        self.data_tree.pack(side="bottom", fill="both", expand=True)

        # Bind double-click event
        self.data_tree.bind("<ButtonRelease-1>", self.on_treeview_select)

    def on_treeview_select(self, event):
        # Get selected item
        selected_item = self.data_tree.selection()
        if selected_item:
            item_values = self.data_tree.item(selected_item, "values")
            if item_values:
                self.id_var.set(item_values[0])  # Set ID vào entry

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(query)
            rows = self.app.cur.fetchall()

            # Clear previous data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)

            # Insert new data into Treeview
            for row in rows:
                self.data_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def delete_data(self):
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE id=%s").format(sql.Identifier(self.app.table_name.get()))
            self.app.cur.execute(delete_query, (self.id_var.get(),))
            
            if self.app.cur.rowcount == 0:  # Kiểm tra số bản ghi bị ảnh hưởng
                messagebox.showwarning("Cảnh báo", "Không có ID nào trùng khớp!")
            else:
                self.app.conn.commit()
                messagebox.showinfo("Thành công", "Sách đã được xóa thành công!")
                self.load_data()  # Refresh data after deletion
                
        except Exception as e:
            self.app.conn.rollback()  # Rollback the transaction on error
            messagebox.showerror("Lỗi", f"Lỗi xóa sách: {e}")


class DisconnectDB:
    def __init__(self, tab, app):
        self.tab = tab
        self.app = app

        disconnect_frame = tk.Frame(self.tab)
        disconnect_frame.pack(pady=10)

        tk.Label(disconnect_frame, text="Ngắt kết nối cơ sở dữ liệu:").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(disconnect_frame, text="Ngắt kết nối", command=self.disconnect_data).grid(row=1, columnspan=2, pady=10)

    def disconnect_data(self):
        try:
            if hasattr(self.app, 'conn') and self.app.conn is not None:
                self.app.cur.close()
                self.app.conn.close()
                messagebox.showinfo("Thành công", "Đã ngắt kết nối cơ sở dữ liệu!")
                
                # Quay về tab đăng nhập
                self.app.tab_control.select(self.app.login_tab)

                # Ẩn các tab khác sau khi ngắt kết nối
                self.app.tab_control.hide(self.app.search_tab)
                self.app.tab_control.hide(self.app.add_tab)
                self.app.tab_control.hide(self.app.update_tab)
                self.app.tab_control.hide(self.app.delete_tab)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi ngắt kết nối: {e}")