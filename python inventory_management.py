import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os
from datetime import datetime

# -------------------- FILES --------------------
INVENTORY_FILE = "inventory.json"
SALES_FILE = "sales.json"
USERS_FILE = "users.json"


# -------------------- LOAD & SAVE --------------------
def load_data(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# -------------------- REGISTER --------------------
def register_user():
    users = load_data(USERS_FILE)
    username = simpledialog.askstring("Register", "Enter new username:")
    if not username:
        return
    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return
    password = simpledialog.askstring("Register", "Enter new password:", show="*")
    users[username] = password
    save_data(USERS_FILE, users)
    messagebox.showinfo("Success", "User registered successfully!")


# -------------------- LOGIN --------------------
def login_window():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x220")
    login.configure(bg="#f2f2f2")

    tk.Label(login, text="Inventory Management Login", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(pady=10)

    tk.Label(login, text="Username:", bg="#f2f2f2").pack()
    username_entry = tk.Entry(login)
    username_entry.pack(pady=5)

    tk.Label(login, text="Password:", bg="#f2f2f2").pack()
    password_entry = tk.Entry(login, show="*")
    password_entry.pack(pady=5)

    def verify_login():
        users = load_data(USERS_FILE)
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if username in users and users[username] == password:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            login.destroy()
            open_main_window(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    tk.Button(login, text="Login", command=verify_login, bg="#4CAF50", fg="white", width=10).pack(pady=8)
    tk.Button(login, text="Register", command=register_user, bg="#2196F3", fg="white", width=10).pack(pady=5)

    login.mainloop()


# -------------------- MAIN WINDOW --------------------
def open_main_window(user):
    inventory = load_data(INVENTORY_FILE)
    sales = load_data(SALES_FILE)

    root = tk.Tk()
    root.title(f"Inventory Management - {user}")
    root.geometry("700x500")
    root.configure(bg="#f2f2f2")

    listbox = tk.Listbox(root, width=80, height=15)
    listbox.pack(pady=10)

    # ----------------- Helper -----------------
    def refresh_display():
        listbox.delete(0, tk.END)
        for name, details in inventory.items():
            listbox.insert(tk.END, f"{name} | Qty: {details['quantity']} | Price: ₹{details['price']:.2f}")

    def validate(qty, price):
        if qty is None or price is None or qty < 0 or price < 0:
            messagebox.showerror("Error", "Enter valid positive values!")
            return False
        return True

    # ----------------- Functions -----------------
    def add_product():
        name = simpledialog.askstring("Add Product", "Product Name:")
        if not name:
            return
        qty = simpledialog.askinteger("Add Product", "Quantity:")
        price = simpledialog.askfloat("Add Product", "Price:")
        if not validate(qty, price):
            return
        inventory[name] = {"quantity": qty, "price": price}
        save_data(INVENTORY_FILE, inventory)
        refresh_display()
        messagebox.showinfo("Success", f"{name} added successfully!")

    def edit_product():
        name = simpledialog.askstring("Edit Product", "Enter product name:")
        if name not in inventory:
            messagebox.showerror("Error", "Product not found!")
            return
        qty = simpledialog.askinteger("Edit Product", "New Quantity:", initialvalue=inventory[name]["quantity"])
        price = simpledialog.askfloat("Edit Product", "New Price:", initialvalue=inventory[name]["price"])
        if not validate(qty, price):
            return
        inventory[name] = {"quantity": qty, "price": price}
        save_data(INVENTORY_FILE, inventory)
        refresh_display()
        messagebox.showinfo("Updated", f"{name} updated successfully!")

    def delete_product():
        name = simpledialog.askstring("Delete Product", "Enter product name:")
        if name in inventory:
            del inventory[name]
            save_data(INVENTORY_FILE, inventory)
            refresh_display()
            messagebox.showinfo("Deleted", f"{name} deleted successfully!")
        else:
            messagebox.showerror("Error", "Product not found!")

    def sell_product():
        name = simpledialog.askstring("Sell Product", "Enter product name:")
        if name not in inventory:
            messagebox.showerror("Error", "Product not found!")
            return
        qty = simpledialog.askinteger("Sell Product", "Enter quantity:")
        if qty is None or qty <= 0:
            messagebox.showerror("Error", "Invalid quantity!")
            return
        if inventory[name]["quantity"] < qty:
            messagebox.showerror("Error", "Not enough stock!")
            return
        total = qty * inventory[name]["price"]
        inventory[name]["quantity"] -= qty
        sales[str(datetime.now())] = {"product": name, "quantity": qty, "total": total}
        save_data(INVENTORY_FILE, inventory)
        save_data(SALES_FILE, sales)
        refresh_display()
        messagebox.showinfo("Sale Complete", f"Sold {qty} {name} for ₹{total:.2f}")

    def low_stock():
        low_items = [n for n, d in inventory.items() if d["quantity"] < 5]
        if low_items:
            messagebox.showwarning("Low Stock", f"Low stock: {', '.join(low_items)}")
        else:
            messagebox.showinfo("OK", "All items in stock!")

    def sales_summary():
        total_income = sum(item["total"] for item in sales.values())
        summary = "\n".join(f"{v['product']} | Qty: {v['quantity']} | ₹{v['total']:.2f}" for v in sales.values())
        if not summary:
            summary = "No sales recorded."
        messagebox.showinfo("Sales Summary", f"{summary}\n\nTotal Income: ₹{total_income:.2f}")

    # ----------------- Buttons -----------------
    frame = tk.Frame(root, bg="#f2f2f2")
    frame.pack()

    buttons = [
        ("Add Product", add_product, "#4CAF50"),
        ("Edit Product", edit_product, "#2196F3"),
        ("Delete Product", delete_product, "#f44336"),
        ("Sell Product", sell_product, "#9C27B0"),
        ("Low Stock", low_stock, "#FF9800"),
        ("Sales Summary", sales_summary, "#607D8B")
    ]

    for i, (text, cmd, color) in enumerate(buttons):
        tk.Button(frame, text=text, command=cmd, bg=color, fg="white", width=15).grid(row=i // 3, column=i % 3, padx=5, pady=5)

    refresh_display()
    root.mainloop()


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    login_window()

