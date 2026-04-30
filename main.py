import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            data = []
    except Exception as error:
        print(f"Error loading data: {error}")

    @classmethod
    def __update(cls):
        try:
            with open(cls.database, 'w') as fs:
                json.dump(cls.data, fs, indent=4)
        except Exception as error:
            print(f"Error updating data: {error}")

    @classmethod
    def __generate_account_number(cls):
        while True:
            acc = ''.join(random.choices(string.digits, k=10))
            if not any(a['account_number'] == acc for a in cls.data):
                return acc

    @classmethod
    def __find_account(cls, account_number, pin):
        for acc in cls.data:
            if acc['account_number'] == account_number and acc['pin'] == pin:
                return acc
        return None

    def Createaccount(self):
        try:
            name = input("Enter name: ").strip()
            age = int(input("Enter age: "))
            email = input("Enter email: ").strip()
            pin = input("Enter 4-digit PIN: ").strip()

            if age < 18:
                print("Must be 18+")
                return
            if len(pin) != 4 or not pin.isdigit():
                print("PIN must be 4 digits")
                return

            acc = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "account_number": self.__generate_account_number(),
                "balance": 0
            }

            Bank.data.append(acc)
            Bank.__update()

            print("\n Account Created Successfully")
            print(f"Account Number: {acc['account_number']}")

        except:
            print("Invalid input")

    def Depositmoney(self):
        acc_no = input("Account number: ")
        pin = input("PIN: ")

        acc = self.__find_account(acc_no, int(pin))
        if not acc:
            print("Invalid credentials")
            return

        try:
            amt = float(input("Amount: "))
            if amt <= 0 or amt > 10000:
                print("Invalid amount")
                return

            acc['balance'] += amt
            Bank.__update()

            print(f"Deposited. Balance: {acc['balance']}")

        except:
            print("Invalid amount")

    def Withdrawmoney(self):
        acc_no = input("Account number: ")
        pin = input("PIN: ")

        acc = self.__find_account(acc_no, int(pin))
        if not acc:
            print("Invalid credentials")
            return

        try:
            amt = float(input("Amount: "))
            if amt <= 0:
                print("Invalid amount")
                return
            if amt > acc['balance']:
                print("Insufficient balance")
                return

            acc['balance'] -= amt
            Bank.__update()

            print(f"Withdrawn. Balance: {acc['balance']}")

        except:
            print("Invalid input")

    def Checkdetails(self):
        acc_no = input("Account number: ")
        pin = input("PIN: ")

        acc = self.__find_account(acc_no, int(pin))
        if not acc:
            print("Invalid credentials")
            return

        print("\nAccount Details:")
        for k, v in acc.items():
            print(f"{k}: {v}")

    def Updateaccount(self):
        acc_no = input("Account number: ")
        pin = input("PIN: ")

        acc = self.__find_account(acc_no, int(pin))
        if not acc:
            print("Invalid credentials")
            return

        print("1.Name  2.Email  3.PIN")
        choice = input("Choice: ")

        if choice == "1":
            new = input("New name: ").strip()
            if new:
                acc['name'] = new

        elif choice == "2":
            new = input("New email: ").strip()
            if new:
                acc['email'] = new

        elif choice == "3":
            new = input("New PIN: ")
            if len(new) == 4 and new.isdigit():
                acc['pin'] = int(new)
            else:
                print("Invalid PIN")
                return

        else:
            print("Invalid choice")
            return

        Bank.__update()
        print("Updated successfully")

    def Deleteaccount(self):
        acc_no = input("Account number: ")
        pin = input("PIN: ")

        acc = self.__find_account(acc_no, int(pin))
        if not acc:
            print("Invalid credentials")
            return

        Bank.data.remove(acc)
        Bank.__update()
        print("Account deleted")

# this code is for terminal testing 
# user = Bank()

# print("press 1 for creating the account")
# print("press 2 for deposit money in the account")
# print("press 3 for withdraw money from the account")
# print("press 4 for checking details of the account")
# print("press 5 for updating the account details")
# print("press 6 for deleting the account")

# check =int(input("enter your choice:- "))

# if check == 1:
#     user.Createaccount()
# if check == 2:
#     user.Depositmoney()
# if check == 3:
#     user.Withdrawmoney()
# if check == 4:
#     user.Checkdetails()
# if check == 5:
#     user.Updateaccount()
# if check == 6:
#     user.Deleteaccount()