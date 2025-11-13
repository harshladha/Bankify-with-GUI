import random

class Account:
    """Represents a bank account."""

    def __init__(self, account_number, name, account_type, balance):
        """
        Initializes an Account object.

        Args:
            account_number (int): The account number.
            name (str): The name of the account holder.
            account_type (str): The type of account (e.g., 'Savings', 'Checking').
            balance (float): The initial balance of the account.
        """
        self.account_number = account_number
        self.name = name
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        """
        Deposits a specified amount into the account.

        Args:
            amount (float): The amount to deposit.

        Returns:
            bool: True if the deposit is successful, False otherwise.
        """
        if amount > 0:
            self.balance += amount
            print(f"\nSuccessfully deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
            return True
        else:
            print("\nInvalid deposit amount. Please enter a positive value.")
            return False

    def withdraw(self, amount):
        """
        Withdraws a specified amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Returns:
            bool: True if the withdrawal is successful, False otherwise.
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"\nSuccessfully withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
            return True
        elif amount > self.balance:
            print("\nInsufficient funds for this withdrawal.")
            return False
        else:
            print("\nInvalid withdrawal amount. Please enter a positive value.")
            return False

    def get_balance(self):
        """Returns the current balance of the account."""
        return self.balance

    def __str__(self):
        """Returns a string representation of the account details."""
        return (f"\nAccount Number: {self.account_number}"
                f"\nHolder Name: {self.name}"
                f"\nAccount Type: {self.account_type}"
                f"\nBalance: ${self.balance:.2f}")


class Bank:
    """Manages bank operations and a collection of accounts."""

    def __init__(self, name):
        """
        Initializes a Bank object.

        Args:
            name (str): The name of the bank.
        """
        self.name = name
        self.accounts = {}

    def create_account(self, name, account_type, initial_deposit):
        """
        Creates a new bank account and adds it to the bank.

        Args:
            name (str): The name of the account holder.
            account_type (str): The type of account.
            initial_deposit (float): The initial deposit amount.

        Returns:
            Account: The newly created Account object, or None if creation failed.
        """
        if initial_deposit < 0:
            print("\nInitial deposit cannot be negative.")
            return None

        account_number = self._generate_account_number()
        new_account = Account(account_number, name, account_type, initial_deposit)
        self.accounts[account_number] = new_account
        print(f"\nAccount created successfully for {name} with Account Number: {account_number}")
        return new_account

    def _generate_account_number(self):
        """Generates a unique 10-digit account number."""
        while True:
            account_number = random.randint(1000000000, 9999999999)
            if account_number not in self.accounts:
                return account_number

    def find_account(self, account_number):
        """
        Finds an account by its account number.

        Args:
            account_number (int): The account number to search for.

        Returns:
            Account: The Account object if found, otherwise None.
        """
        return self.accounts.get(account_number)

    def close_account(self, account_number):
        """
        Closes an account by removing it from the bank.

        Args:
            account_number (int): The account number of the account to close.

        Returns:
            bool: True if the account was closed successfully, False otherwise.
        """
        if account_number in self.accounts:
            del self.accounts[account_number]
            print(f"\nAccount {account_number} has been successfully closed.")
            return True
        else:
            print("\nAccount not found.")
            return False

    def list_all_accounts(self):
        """Displays details for all accounts in the bank."""
        if not self.accounts:
            print("\nNo accounts in the bank.")
            return

        print("\n--- All Bank Accounts ---")
        for account in self.accounts.values():
            print(account)
            print("-------------------------")
