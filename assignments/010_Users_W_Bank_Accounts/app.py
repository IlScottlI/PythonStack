# Assignment: User
# Objectives:
# Practice creating a class and making instances from it
# Practice accessing the methods and attributes of different instances
# If you've been following along, you're going to utilize the User class we've been discussing for this assignment.

# For this assignment, we'll add some functionality to the User class:


class User:
    def __init__(self, name, email, username):
        self.name = name
        self.email = email
        self.username = username
        self.checking = BankAccount(.03, 900, self.name)
        self.savings = BankAccount(.04, 1387, self.name)

    def make_deposit_checking(self, amount):
        self.checking.deposit(amount)
        print(f'Deposit was made to checking account: ${float(amount)}')
        self.info()
        return self

    def make_withdrawal_checking(self, amount):
        self.checking.withdraw(amount)
        print(f'Withdrawal was made from checking: (${float(amount)})')
        self.info()
        return self

    def make_deposit_savings(self, amount):
        self.savings.deposit(amount)
        print(f'Deposit was made to savings account: ${float(amount)}')
        self.info()
        return self

    def make_withdrawal_savings(self, amount):
        self.savings.withdraw(amount)
        print(f'Withdrawal was made from savings: (${float(amount)})')
        self.info()
        return self

    def info(self):
        print(
            f"Name: {self.name}, Email: {self.email}, UserName: {self.username}, CheckingBalance: ${self.checking.account_balance}, SavingsBalance: ${self.savings.account_balance}"
        )
        return self


class BankAccount:
    # don't forget to add some default values for these parameters!
    def __init__(self, int_rate, balance, owner):
        # your code here! (remember, this is where we specify the attributes for our class)
        self.int_rate = float(int_rate)
        self.account_balance = float(balance)
        self.owner = owner

    def deposit(self, amount):
        self.account_balance += amount
        return self

    def withdraw(self, amount):
        if self.account_balance < amount:
            print("Insufficient funds: Charging a $5 fee")
            self.withdraw(float(5))
        else:
            self.account_balance -= amount
        return self

    def display_account_info(self):
        print(
            f'Balance: ${self.account_balance} ')

    def yield_interest(self):
        if self.account_balance > 0:
            increase = self.account_balance * self.int_rate
            self.account_balance = self.account_balance + increase
            print(
                f"Intreest Deposit: ${increase}")
        return self


Scott = User('Scott Johnson', 'johnson.se@pg.com', 'johnson.se')

Scott.make_deposit_checking(230).make_deposit_savings(
    45).make_withdrawal_checking(230)
