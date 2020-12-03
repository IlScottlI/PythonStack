# deposit(self, amount) - increases the account balance by the given amount
# withdraw(self, amount) - decreases the account balance by the given amount if there are sufficient funds; if there is not enough money, print a message "Insufficient funds: Charging a $5 fee" and deduct $5
# display_account_info(self) - print to the console: eg. "Balance: $100"
# yield_interest(self) - increases the account balance by the current balance * the interest rate (as long as the balance is positive)
import time


class BankAccount:
    # don't forget to add some default values for these parameters!
    def __init__(self, int_rate, balance):
        # your code here! (remember, this is where we specify the attributes for our class)
        self.int_rate = float(int_rate)
        self.account_balance = float(balance)

    def deposit(self, amount):
        self.account_balance += amount
        print(f'Deposit was made: ${float(amount)}')
        return self

    def withdraw(self, amount):
        if self.account_balance < amount:
            print("Insufficient funds: Charging a $5 fee")
            self.withdraw(float(5))
        else:
            self.account_balance -= amount
            print(f'Withdrawal was made: (${float(amount)})')
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


# Everytime this file is saved it adds a this single command to a new line.......
card1 = BankAccount(.03, 900)
card1.deposit(200).deposit(100).deposit(10).withdraw(
    300).yield_interest().display_account_info()
# Everytime this file is saved it adds a this single command to a new line.......
card2 = BankAccount(.04, 10)
card2.deposit(200).deposit(100).deposit(10).withdraw(
    600).yield_interest().deposit(490).display_account_info()
