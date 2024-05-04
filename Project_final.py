import pickle
import os
import pathlib
import datetime

class Account:
    def __init__(self, accNo, name, deposit, account_type, password):
        self.accNo = accNo
        self.name = name
        self.deposit = deposit
        self.type = account_type
        self.password = password
        self.login_attempts = 0
        self.locked = False
        self.last_login_attempt = None

    def createAccount(self):
        self.accNo = int(input("Enter the account number: "))
        self.setName()
        self.type = input("Enter the type of account [C/S]: ")
        self.deposit = int(input("Enter The Initial amount(>=500 for Saving and >=1000 for current): "))
        self.password = input("Set a 4-digit password for your account: ")
        print("Account Created")

    def setName(self):
        while True:
            name = input("Enter the account holder name: ")
            if name.replace(" ", "").isalpha():  # Check if the name contains only alphabets and spaces
                self.name = name
                break
            else:
                print("Invalid name! Name should contain only alphabets and spaces.")

    def showAccount(self):
        print("\nAccount Details:")
        print("Account Number:", self.accNo)
        print("Account Holder Name:", self.name)
        print("Type of Account:", self.type)
        print("Balance:", self.deposit)

    def modifyAccount(self):
        print("\nModify Account Details:")
        print("1. Change Name")
        print("2. Account Type")
        print("3. Change Password")
        print("4. Exit")
        modify_option = input("Select Your Option (1-4): ")

        if modify_option == '1':
            self.setName()
        elif modify_option == '2':
            self.type = input("Modify type of Account: ")
        elif modify_option == '3':
            self.changePassword()
        elif modify_option == '4':
            print("Exiting modify account menu.")
        else:
            print("Invalid option.")

    def changePassword(self):
        old_password = input("Enter your old 4-digit password: ")
        if old_password == self.password:
            new_password = input("Enter your new 4-digit password: ")
            self.password = new_password
            print("Password changed successfully.")
        else:
            print("Incorrect old password. Password change failed.")

    def depositAmount(self, amount):
        self.deposit += amount  

    def withdrawAmount(self, amount):
        if amount <= self.deposit:
            self.deposit -= amount  
        else:
            print("Insufficient balance")

    def report(self):
        print(self.accNo, self.name, self.type, self.deposit)  

    def getAccountNo(self):
        return self.accNo

    def getAccountHolderName(self):
        return self.name

    def getAccountType(self):
        return self.type

    def getDeposit(self):
        return self.deposit

def load_accounts():
    file_path = "accounts.data"
    if pathlib.Path(file_path).exists():
        file_size = os.path.getsize(file_path)
        if file_size > 0:
            with open(file_path, "rb") as infile:
                return pickle.load(infile)
    return []

def save_accounts(account_list):
    with open("accounts.data", "wb") as outfile:
        pickle.dump(account_list, outfile)

def authenticate_account(account_list):
    acc_no = int(input("Enter your account number: "))
    password = input("Enter your 4-digit password: ")

    for account in account_list:
        if account.accNo == acc_no and not account.locked:
            if account.password == password:
                account.login_attempts = 0
                account.locked = False
                save_accounts(account_list)
                return account
            else:
                account.login_attempts += 1
                if account.login_attempts >= 3:
                    account.locked = True
                    account.last_login_attempt = datetime.datetime.now()
                    print("Too many failed attempts. Account locked for 24 hours.")
                    save_accounts(account_list)
                    return None
                else:
                    print("Invalid password. Please try again.")
                    save_accounts(account_list)
                    return None
    print("Invalid account number or account locked.")
    return None

def display_accounts(account_list):
    print("\nAll Accounts:")

    # Sort the accounts based on the selected criteria
    while True:
        print("\nSORT BY:")
        print("1. Account Number")
        print("2. Name")
        print("3. Account Type")
        print("4. Balance")
        print("5. Exit")

        sort_option = input("Select Your Sorting Option (1-5): ")

        if sort_option == '1':
            sorted_accounts = sorted(account_list, key=lambda x: x.accNo)
            break
        elif sort_option == '2':
            sorted_accounts = sorted(account_list, key=lambda x: x.name)
            break
        elif sort_option == '3':
            account_type_option = input("Filter by account type [C/S]: ").lower()
            if account_type_option == 'c':
                sorted_accounts = [acc for acc in account_list if acc.type.lower() == 'c']
            elif account_type_option == 's':
                sorted_accounts = [acc for acc in account_list if acc.type.lower() == 's']
            else:
                print("Invalid account type filter.")
                continue
            break
        elif sort_option == '4':
            sorted_accounts = sorted(account_list, key=lambda x: x.deposit)
            break
        elif sort_option == '5':
            print("Exiting sort menu.")
            return
        else:
            print("Invalid sort option.")

    # Display sorted accounts in tabular format
    print("\nSorted Accounts:")
    print("Serial No. \t| Account Number \t| Name \t\t| Account Type \t\t| Balance\t\n")
    for index, account in enumerate(sorted_accounts, 1):
        print(f"{index:<15} | {account.accNo:<21} | {account.name:<13} | {account.type:<21} | {account.deposit:<13}")

def search_account(account_list):
    search_query = input("Enter the account number or account holder name to search: ")
    found_accounts = []

    for account in account_list:
        if search_query.lower() in account.name.lower() or search_query == str(account.accNo):
            found_accounts.append(account)

    if found_accounts:
        print("\nSearch Results:")
        print("Serial No. \t| Account Number \t| Name \t\t| Account Type \t\t| Balance\t\n")
        for index, account in enumerate(found_accounts, 1):
            print(f"{index:<15} | {account.accNo:<21} | {account.name:<13} | {account.type:<21} | {account.deposit:<13}")
    else:
        print("No matching accounts found.")

def modify_account(account_list):
    acc_no = int(input("Enter the account number to modify: "))
    for account in account_list:
        if account.accNo == acc_no:
            account.modifyAccount()
            save_accounts
def modify_account(account_list):
    acc_no = int(input("Enter the account number to modify: "))
    for account in account_list:
        if account.accNo == acc_no:
            account.modifyAccount()
            save_accounts(account_list)
            print("Account modified successfully.")
            return
    print("Account not found.")

def main():
    account_list = load_accounts()

    while True:
        print("\nMAIN MENU")
        print("1. LOGIN")
        print("2. CREATE NEW ACCOUNT")
        print("3. EXIT")
        choice = input("Select Your Option (1-3): ")

        if choice == '1':
            print("Login as:")
            print("1. Admin")
            print("2. User")
            login_choice = input("Select Your Option (1-2): ")

            if login_choice == '1':  # Admin login
                admin_password = input("Enter the admin password: ")
                if admin_password == "admin@123":  # Sample admin password
                    print("Admin login successful!")
                    while True:
                        print("\nADMIN MENU")
                        print("1. DISPLAY ACCOUNTS")
                        print("2. SEARCH ACCOUNT")
                        print("3. MODIFY ACCOUNT")
                        print("4. DELETE ACCOUNT")
                        print("5. CHANGE PASSWORD")
                        print("6. EXIT")
                        admin_option = input("Select Your Option (1-6): ")

                        if admin_option == '1':
                            display_accounts(account_list)
                        elif admin_option == '2':
                            search_account(account_list)
                        elif admin_option == '3':
                            modify_account(account_list)
                        elif admin_option == '4':
                            acc_no = int(input("Enter the account number to delete: "))
                            for account in account_list:
                                if account.accNo == acc_no:
                                    account_list.remove(account)
                                    save_accounts(account_list)
                                    print("Account deleted successfully.")
                                    break
                            else:
                                print("Account not found.")
                        elif admin_option == '5':
                            acc_no = int(input("Enter the account number to change password: "))
                            for account in account_list:
                                if account.accNo == acc_no:
                                    new_password = input("Enter the new 4-digit password: ")
                                    account.password = new_password
                                    save_accounts(account_list)
                                    print("Password changed successfully.")
                                    break
                            else:
                                print("Account not found.")
                        elif admin_option == '6':
                            print("Exiting admin menu.")
                            save_accounts(account_list)
                            break
                        else:
                            print("Invalid admin option.")

                else:
                    print("Invalid admin password.")
            elif login_choice == '2':  # User login
                account = authenticate_account(account_list)
                if account:
                    print("Login successful!")
                    while True:
                        print("\nACCOUNT MENU")
                        print("1. SHOW ACCOUNT DETAILS")
                        print("2. MODIFY ACCOUNT")
                        print("3. DEPOSIT AMOUNT")
                        print("4. WITHDRAW AMOUNT")
                        print("5. CHANGE PASSWORD")
                        print("6. LOGOUT")
                        option = input("Select Your Option (1-6): ")

                        if option == '1':
                            account.showAccount()
                        elif option == '2':
                            account.modifyAccount()
                        elif option == '3':
                            amount = int(input("Enter the amount to deposit: "))
                            account.depositAmount(amount)
                            print("Deposit successful.")
                        elif option == '4':
                            amount = int(input("Enter the amount to withdraw: "))
                            account.withdrawAmount(amount)
                        elif option == '5':
                            account.changePassword()
                        elif option == '6':
                            print("Logging out...")
                            save_accounts(account_list)  # Save changes before logout
                            break
                        else:
                            print("Invalid option.")
                else:
                    print("Login failed. Please try again.")
            else:
                print("Invalid login choice.")
        elif choice == '2':
            new_account = Account(0, "", 0, "", "")
            new_account.createAccount()
            account_list.append(new_account)
            save_accounts(account_list)
        elif choice == '3':
            print("Thanks for using bank management system")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

