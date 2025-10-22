
balance = 1000
pin = "1234"

def check_balance():
    print(f"Balance: ₹{balance}")

def deposit():
    global balance
    amt = float(input("Enter deposit amount: "))
    balance += amt
    print(f"Deposited ₹{amt}, New Balance = ₹{balance}")

def withdraw():
    global balance
    amt = float(input("Enter withdraw amount: "))
    if amt <= balance:
        balance -= amt
        print(f"Withdrawn ₹{amt}, New Balance = ₹{balance}")
    else:
        print("Insufficient funds")

while True:
    print("\n1. Balance  2. Deposit  3. Withdraw  4. Exit")
    choice = input("Enter choice: ")
    if choice == "1":
        check_balance()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        print("Exit ATM")
        break
    else:
        print("Invalid choice")
