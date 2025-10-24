from tkinter import Tk, Label, Button, Entry, messagebox, filedialog
import ctypes
from ctypes import cdll, c_char_p, c_double, c_void_p, c_int 
import os
import sys

DLL_LOADED = False


try:
    script_dir = os.path.dirname(os.path.abspath("__file__"))
    dll_path = os.path.join(script_dir, "cm.dll")
    lib = ctypes.CDLL(dll_path)
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
    lib.Bank_deposit.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
    lib.Bank_withdraw.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double]
    lib.Bank_add_new_client.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_double]
    lib.Bank_find_client.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.Bank_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

    lib.Bank_get_client_name.argtypes = [ c_void_p, c_double]
    lib.Bank_get_client_name.restype = c_char_p

    lib.Bank_get_client_phone.argtypes = [c_void_p, c_double]
    lib.Bank_get_client_phone.restype = c_char_p

    lib.Bank_get_client_balance.argtypes = [c_void_p, c_double]
    lib.Bank_get_client_balance.restype = c_double


class BankApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank Management System")
        self.master.geometry("500x600")
        
        if not DLL_LOADED:
            Label(master, text="RUNNING IN MOCK MODE - DLL NOT FOUND", 
                  fg="red", font=("Arial", 10, "bold")).pack(pady=5)

        
        Button(master, text="Load Clients File", command=self.load_file).pack(pady=10)
        Button(master, text="Show client Info", command=self.show_client_info).pack(pady=5)

        
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

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select clients file")
        if not file_path:
            return
        self.bank = lib.Bank_new(file_path.encode('utf-8'))
        self.save_path = file_path 
        messagebox.showinfo("Success", "Clients loaded successfully!")

        # Start autosave loop
        self.autosave()

    def show_client_info(self): 
        try:
            cid = int(self.client_id_entry.get())
            client_ptr = lib.Bank_find_client(self.bank, cid)
            if not client_ptr:
                messagebox.showerror("Error", "Client wasn't found")
                return
            
            name_ptr = lib.Bank_get_client_name(self.bank, cid)
            name = name_ptr.decode('utf-8') if name_ptr else "N/A"

            phone_ptr = lib.Bank_get_client_phone(self.bank, cid)
            phone = phone_ptr.decode('utf-8') if phone_ptr else "N/A" 

            balance = lib.Bank_get_client_balance(self.bank, cid)

            messagebox.showinfo(
                "Client Info", 
                f"Name: {name}\nPhone: {phone}\nAccount #: {cid}\nBalance: ${balance:.2f}"
            )
        except ValueError: 
            messagebox.showerror("Error", "Wrong Input.")

    def deposit(self):
        if not hasattr(self, 'bank'):
            messagebox.showerror("Error", "Load clients file first!")
            return
        try:
            cid = int(self.client_id_entry.get())
            amount = float(self.amount_entry.get())
            lib.Bank_deposit(self.bank, cid, amount)
            self.save_bank()

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

            self.save_bank()

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
            self.save_bank()

          
            if hasattr(self, 'save_path') and self.save_path:
                lib.Bank_save(self.bank, self.save_path.encode('utf-8'))

            messagebox.showinfo("Success", "New client added and saved!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    
    def autosave(self):
        """Automatically save bank data every 5 seconds."""
        if hasattr(self, 'bank') and hasattr(self, 'save_path') and self.save_path:
            try:
                lib.Bank_save(self.bank, self.save_path.encode('utf-8'))
            except Exception as e:
                print(f"Autosave failed: {e}")
        
        self.master.after(100, self.autosave)

    def save_bank(self): 
        """Save the bank data immediately."""
        if hasattr(self, 'bank') and hasattr(self, 'save_path') and self.save_path:
            try:
                lib.Bank_save(self.bank, self.save_path.encode('utf-8'))
            except Exception as e:
                messagebox.showerror("Save failed", f"Save failed: {e}")

    # ----------- Close / Exit -----------
    def on_close(self):
        """Automatically save client data when window closes."""
        if hasattr(self, 'bank') and hasattr(self, 'save_path') and self.save_path:
            try:
                lib.Bank_save(self.bank, self.save_path.encode('utf-8'))
            except Exception as e:
                resp = messagebox.askyesno("Save failed", f"Auto-save failed: {e}\nDo you want to try Save As?")
                if resp:
                    save_path = filedialog.asksaveasfilename(
                        title="Save clients file",
                        defaultextension=".txt",
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                    )
                    if save_path:
                        lib.Bank_save(self.bank, os.path.abspath(save_path).encode('utf-8'))
        self.master.destroy()


if __name__ == "__main__":
    root = Tk()
    app = BankApp(root)
    root.mainloop()
