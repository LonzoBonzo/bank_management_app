from tkinter import Tk, Label, Button, Entry, messagebox, filedialog
import ctypes
from ctypes import cdll, c_char_p, c_double, c_void_p 
import os
import sys


try:
    lib = ctypes.CDLL("./client_management.dll")
    DLL_LOADED = True
    print("DLL loaded successfully!")
except Exception as e:
    print(f"DLL not found: {e}")
    print("Running in mock mode for testing...")
    DLL_LOADED = False
    
 
    class MockLib:
        def __getattr__(self, name):
            def mock_method(*args, **kwargs):
                print(f"Mock method called: {name} with args: {args[1:]}")
                return 1  
            return mock_method
    lib = MockLib()


if DLL_LOADED:
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
        
        if not DLL_LOADED:
            Label(master, text="RUNNING IN MOCK MODE - DLL NOT FOUND", 
                  fg="red", font=("Arial", 10, "bold")).pack(pady=5)

       
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