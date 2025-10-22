import ctypes
from tkinter import *
from tkinter import messagebox, filedialog

# Load the shared library
lib = ctypes.CDLL("./libclient_management.so")  # change to "./libclient_management.so" if on Linux/Mac

# Define argument and return types for wrapper functions
lib.Bank_new.argtypes = [ctypes.c_char_p]
lib.Bank_new.restype = ctypes.c_void_p

lib.Bank_deposit.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
lib.Bank_withdraw.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
lib.Bank_add_new_client.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_double]
lib.Bank_find_client.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.Bank_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]


class BankApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Management System")
        self.master.geometry("400x400")

        # ---- Load Bank File ----
        Button(master, text="Load Clients File", command=self.load_file).pack(pady=10)

        # ---- Deposit ----
        Label(master, text="Client ID").pack()
        self.client_id_entry = Entry(master)
        self.client_id_entry.pack()

        Label(master, text="Amount").pack()
        self.amount_entry = Entry(master)
        self.amount_entry.pack()

        Button(master, text="Deposit", command=self.deposit).pack(pady=5)
        Button(master, text="Withdraw", command=self.withdraw).pack(pady=5)

        # ---- Add New Client ----
        Label(master, text="--- Add New Client ---").pack(pady=10)
        Label(master, text="Name").pack()
        self.name_entry = Entry(master)
        self.name_entry.pack()
        Label(master, text="Phone").pack()
        self.phone_entry = Entry(master)
        self.phone_entry.pack()
        Label(master, text="Account #").pack()
        self.acc_entry = Entry(master)
        self.acc_entry.pack()
        Label(master, text="Balance").pack()
        self.balance_entry = Entry(master)
        self.balance_entry.pack()

        Button(master, text="Add Client", command=self.add_client).pack(pady=5)

    # ----------- Backend Actions -----------

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select clients file")
        if not file_path:
            return
        self.bank = lib.Bank_new(file_path.encode('utf-8'))
        messagebox.showinfo("Success", "Clients loaded successfully!")

    def deposit(self):
        if not hasattr(self, 'bank'):
            messagebox.showerror("Error", "Load clients file first!")
            return
        try:
            cid = int(self.client_id_entry.get())
            amount = float(self.amount_entry.get())
            lib.Bank_deposit(self.bank, cid, amount)
            messagebox.showinfo("Success", f"${amount} deposited to client {cid}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    def withdraw(self):
        if not hasattr(self, 'bank'):
            messagebox.showerror("Error", "Load clients file first!")
            return
        try:
            cid = int(self.client_id_entry.get())
            amount = float(self.amount_entry.get())
            lib.Bank_withdraw(self.bank, cid, amount)
            messagebox.showinfo("Success", f"${amount} withdrawn from client {cid}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    def add_client(self):
        if not hasattr(self, 'bank'):
            messagebox.showerror("Error", "Load clients file first!")
            return
        try:
            name = self.name_entry.get().encode('utf-8')
            phone = self.phone_entry.get().encode('utf-8')
            acc = int(self.acc_entry.get())
            balance = float(self.balance_entry.get())

            lib.Bank_add_new_client(self.bank, name, phone, acc, balance)
            messagebox.showinfo("Success", "New client added!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")


# ----------- Run GUI -----------
if __name__ == "__main__":
    root = Tk()
    app = BankApp(root)
    root.mainloop()
