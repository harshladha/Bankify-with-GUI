import tkinter as tk
from tkinter import ttk  # Import themed widgets
from tkinter import messagebox  # Import for pop-up dialogs
from bank_management import Bank, Account  # Import our backend logic

# --- Constants for styling ---
BG_COLOR = "#F0F4F8"       # Light blue-gray background
BTN_COLOR = "#4F46E5"      # Indigo button
BTN_TEXT_COLOR = "#FFFFFF" # White text
HEADER_FONT = ("Helvetica", 16, "bold")
LABEL_FONT = ("Helvetica", 10)
BTN_FONT = ("Helvetica", 10, "bold")

class BankApp(tk.Tk):
    """Main application class for the Bankify GUI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Initialize the Bank logic ---
        self.bank = Bank("Bankify")

        # --- Configure the main window ---
        self.title("Bankify - Bank Management System")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)
        
        # --- Create a container for all frames ---
        # This container will hold all our "pages"
        container = ttk.Frame(self, padding=(10, 10))
        container.pack(fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Dictionary to hold all our page frames

        # --- Create and add all pages to the self.frames dictionary ---
        # We iterate over a tuple of page classes
        for F in (StartPage, CreateAccountPage, DepositPage, WithdrawPage, 
                  BalancePage, DetailsPage, AllAccountsPage, CloseAccountPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # Place all frames in the same grid cell; the one on top will be visible
            frame.grid(row=0, column=0, sticky="nsew") 

        # Show the starting page
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Raises the given page frame to the top."""
        frame = self.frames[page_name]
        frame.tkraise()
        # Call 'on_show' method if it exists, to refresh data
        if hasattr(frame, "on_show"):
            frame.on_show()

# --- Page 1: The Main Menu (StartPage) ---

class StartPage(ttk.Frame):
    """The main menu page."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid layout for this frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3) # Give more space to the button grid

        # --- Header ---
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, pady=20)
        
        label = ttk.Label(header_frame, text="Welcome to Bankify!", font=HEADER_FONT)
        label.pack()
        
        sub_label = ttk.Label(header_frame, text="Please choose an option:", font=LABEL_FONT)
        sub_label.pack(pady=5)

        # --- Button Grid ---
        button_grid = ttk.Frame(self)
        button_grid.grid(row=1, column=0)

        # Define button texts and their corresponding page names
        buttons = [
            ("Create Account", "CreateAccountPage"),
            ("Deposit", "DepositPage"),
            ("Withdraw", "WithdrawPage"),
            ("Check Balance", "BalancePage"),
            ("Account Details", "DetailsPage"),
            ("List All Accounts", "AllAccountsPage"),
            ("Close Account", "CloseAccountPage"),
            ("Exit", None) # 'None' for special action (exit)
        ]

        # Create and place buttons in a 4x2 grid
        for i, (text, page) in enumerate(buttons):
            row, col = divmod(i, 2)
            if page:
                # Standard button that shows a frame
                btn = ttk.Button(
                    button_grid, 
                    text=text, 
                    width=20,
                    command=lambda p=page: controller.show_frame(p)
                )
            else:
                # Special case for the Exit button
                btn = ttk.Button(
                    button_grid, 
                    text=text, 
                    width=20,
                    command=self.controller.quit # Call the quit method
                )
            btn.grid(row=row, column=col, padx=10, pady=10)

# --- Helper function for creating standard "Back" button ---

def create_back_button(parent, controller):
    """Creates a standardized 'Back to Menu' button."""
    return ttk.Button(
        parent, 
        text="Back to Menu", 
        command=lambda: controller.show_frame("StartPage")
    )

# --- Base Page for common functionality ---

class BasePage(ttk.Frame):
    """A base class for pages that need an account number."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1) # Center content

    def create_common_widgets(self, title_text):
        """Creates common widgets like title, account entry, and back button."""
        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=0)
        
        ttk.Label(content_frame, text=title_text, font=HEADER_FONT).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(content_frame, text="Account Number:", font=LABEL_FONT).grid(row=1, column=0, sticky="e", padx=5, pady=10)
        self.acc_num_entry = ttk.Entry(content_frame, width=30)
        self.acc_num_entry.grid(row=1, column=1, sticky="w", padx=5, pady=10)

        create_back_button(self, self.controller).grid(row=3, column=0, pady=20)
        
        return content_frame

# --- Page 2: Create Account ---

class CreateAccountPage(ttk.Frame):
    """Page for creating a new bank account."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1) # Center content
        
        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=0)

        ttk.Label(content_frame, text="Create New Account", font=HEADER_FONT).grid(row=0, column=0, columnspan=2, pady=20)
        
        # --- Entry Fields ---
        fields = [
            ("Holder's Name:", ttk.Entry(content_frame, width=30)),
            ("Account Type:", ttk.Entry(content_frame, width=30)),
            ("Initial Deposit:", ttk.Entry(content_frame, width=30))
        ]
        
        self.entries = {}
        for i, (text, entry) in enumerate(fields, start=1):
            ttk.Label(content_frame, text=text, font=LABEL_FONT).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.entries[text] = entry
            
        # --- Buttons ---
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        create_btn = ttk.Button(button_frame, text="Create Account", command=self.on_create)
        create_btn.pack(side="left", padx=10)
        
        back_btn = create_back_button(button_frame, controller)
        back_btn.pack(side="left", padx=10)

    def on_create(self):
        """Handles the 'Create Account' button click."""
        try:
            name = self.entries["Holder's Name:"].get()
            acc_type = self.entries["Account Type:"].get()
            deposit = float(self.entries["Initial Deposit:"].get())
            
            if not name or not acc_type:
                messagebox.showerror("Error", "Name and Account Type cannot be empty.")
                return

            new_account = self.controller.bank.create_account(name, acc_type, deposit)
            
            if new_account:
                messagebox.showinfo(
                    "Success", 
                    f"Account created for {name}!\nAccount Number: {new_account.account_number}"
                )
                # Clear fields after success
                for entry in self.entries.values():
                    entry.delete(0, 'end')
                self.controller.show_frame("StartPage")
            else:
                messagebox.showerror("Error", "Initial deposit must be $0 or more.")
        
        except ValueError:
            messagebox.showerror("Error", "Invalid input for deposit. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# --- Page 3: Deposit ---

class DepositPage(BasePage):
    """Page for depositing money."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        content_frame = self.create_common_widgets("Deposit Funds")
        
        ttk.Label(content_frame, text="Amount:", font=LABEL_FONT).grid(row=2, column=0, sticky="e", padx=5, pady=10)
        self.amount_entry = ttk.Entry(content_frame, width=30)
        self.amount_entry.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        
        submit_btn = ttk.Button(content_frame, text="Deposit", command=self.on_deposit)
        submit_btn.grid(row=3, column=1, sticky="w", padx=5, pady=20)
        
    def on_deposit(self):
        try:
            acc_num = int(self.acc_num_entry.get())
            amount = float(self.amount_entry.get())
            
            account = self.controller.bank.find_account(acc_num)
            
            if not account:
                messagebox.showerror("Error", "Account not found.")
                return
            
            if account.deposit(amount):
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}.\nNew Balance: ${account.get_balance():.2f}")
                self.acc_num_entry.delete(0, 'end')
                self.amount_entry.delete(0, 'end')
                self.controller.show_frame("StartPage")
            else:
                messagebox.showerror("Error", "Invalid deposit amount. Must be positive.")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers.")

# --- Page 4: Withdraw ---

class WithdrawPage(BasePage):
    """Page for withdrawing money."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        content_frame = self.create_common_widgets("Withdraw Funds")
        
        ttk.Label(content_frame, text="Amount:", font=LABEL_FONT).grid(row=2, column=0, sticky="e", padx=5, pady=10)
        self.amount_entry = ttk.Entry(content_frame, width=30)
        self.amount_entry.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        
        submit_btn = ttk.Button(content_frame, text="Withdraw", command=self.on_withdraw)
        submit_btn.grid(row=3, column=1, sticky="w", padx=5, pady=20)
        
    def on_withdraw(self):
        try:
            acc_num = int(self.acc_num_entry.get())
            amount = float(self.amount_entry.get())
            
            account = self.controller.bank.find_account(acc_num)
            
            if not account:
                messagebox.showerror("Error", "Account not found.")
                return
            
            if account.withdraw(amount):
                messagebox.showinfo("Success", f"Withdrew ${amount:.2f}.\nNew Balance: ${account.get_balance():.2f}")
                self.acc_num_entry.delete(0, 'end')
                self.amount_entry.delete(0, 'end')
                self.controller.show_frame("StartPage")
            else:
                # The withdraw method prints to console, but we need a GUI message.
                # The method returns False for *both* insufficient funds and invalid amount.
                if amount <= 0:
                     messagebox.showerror("Error", "Invalid withdrawal amount. Must be positive.")
                else:
                     messagebox.showerror("Error", "Insufficient funds.")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers.")

# --- Page 5: Check Balance ---

class BalancePage(BasePage):
    """Page for checking account balance."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        content_frame = self.create_common_widgets("Check Balance")
        
        submit_btn = ttk.Button(content_frame, text="Check", command=self.on_check)
        submit_btn.grid(row=3, column=1, sticky="w", padx=5, pady=20)
        
    def on_check(self):
        try:
            acc_num = int(self.acc_num_entry.get())
            account = self.controller.bank.find_account(acc_num)
            
            if account:
                messagebox.showinfo("Balance", f"Current Balance: ${account.get_balance():.2f}")
                self.acc_num_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Account not found.")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid account number. Please enter a number.")

# --- Page 6: Account Details ---

class DetailsPage(BasePage):
    """Page for viewing all account details."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        content_frame = self.create_common_widgets("View Account Details")
        
        submit_btn = ttk.Button(content_frame, text="Get Details", command=self.on_details)
        submit_btn.grid(row=3, column=1, sticky="w", padx=5, pady=20)
        
    def on_details(self):
        try:
            acc_num = int(self.acc_num_entry.get())
            account = self.controller.bank.find_account(acc_num)
            
            if account:
                # The __str__ method gives a formatted string
                details = account.__str__() 
                messagebox.showinfo("Account Details", details)
                self.acc_num_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Account not found.")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid account number. Please enter a number.")

# --- Page 7: List All Accounts ---

class AllAccountsPage(ttk.Frame):
    """Page to display a list of all accounts."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="All Bank Accounts", font=HEADER_FONT).pack(pady=10)
        
        # --- Create a Text widget with a Scrollbar ---
        text_frame = ttk.Frame(self, padding=5)
        text_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.text_area = tk.Text(
            text_frame, 
            wrap="word", 
            width=60, 
            height=15,
            yscrollcommand=scrollbar.set,
            font=("Courier", 10) # Use a monospace font for alignment
        )
        self.text_area.pack(fill="both", expand=True)
        
        scrollbar.config(command=self.text_area.yview)
        
        # Disable editing
        self.text_area.config(state="disabled")
        
        create_back_button(self, controller).pack(pady=10)

    def on_show(self):
        """Called when the frame is raised. Refreshes the account list."""
        self.text_area.config(state="normal") # Enable editing to insert text
        self.text_area.delete(1.0, "end") # Clear old content
        
        all_accounts = self.controller.bank.accounts
        
        if not all_accounts:
            self.text_area.insert("end", "No accounts in the bank.")
        else:
            for acc_num, account in all_accounts.items():
                self.text_area.insert("end", f"Account Number: {account.account_number}\n")
                self.text_area.insert("end", f"Holder Name: {account.name}\n")
                self.text_area.insert("end", f"Account Type: {account.account_type}\n")
                self.text_area.insert("end", f"Balance: ${account.balance:.2f}\n")
                self.text_area.insert("end", "--------------------------------------\n")
                
        self.text_area.config(state="disabled") # Disable editing again

# --- Page 8: Close Account ---

class CloseAccountPage(BasePage):
    """Page for closing an account."""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        content_frame = self.create_common_widgets("Close Account")
        
        submit_btn = ttk.Button(content_frame, text="Close Account", command=self.on_close)
        submit_btn.grid(row=3, column=1, sticky="w", padx=5, pady=20)
        
    def on_close(self):
        try:
            acc_num = int(self.acc_num_entry.get())
            
            # --- Add a confirmation dialog ---
            account = self.controller.bank.find_account(acc_num)
            if not account:
                 messagebox.showerror("Error", "Account not found.")
                 return
                 
            confirm = messagebox.askyesno(
                "Confirm", 
                f"Are you sure you want to close account:\n{account.account_number} - {account.name}?"
            )
            
            if confirm:
                if self.controller.bank.close_account(acc_num):
                    messagebox.showinfo("Success", f"Account {acc_num} has been closed.")
                    self.acc_num_entry.delete(0, 'end')
                    self.controller.show_frame("StartPage")
                else:
                    # This case should be covered by find_account, but good to have
                    messagebox.showerror("Error", "Account not found.")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid account number. Please enter a number.")

# --- Main execution ---
if __name__ == "__main__":
    app = BankApp()
    app.mainloop()