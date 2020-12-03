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
        self.account_balance = 0

    def make_deposit(self, amount):
        self.account_balance += amount
        print(f'Deposit was made: ${float(amount)}')
        return self

# make_withdrawal(self, amount) - have this method decrease the user's balance by the amount specified

    def make_withdrawal(self, amount):
        self.account_balance -= amount
        print(f'Withdrawal was made: (${float(amount)})')
        return self
# display_user_balance(self) - have this method print the user's name and account balance to the terminal

    def info(self):
        print(
            f"Name: {self.name}, Email: {self.email}, UserName: {self.username}, AccountBalance: ${self.account_balance}"
        )
        return self

# BONUS: transfer_money(self, other_user, amount) - have this method decrease the user's balance by the amount and add that amount to other other_user's balance

    def transfer_money(self, other_user, amount):
        self.make_withdrawal(amount)
        other_user.make_deposit(amount)
        return self


Scott = User('Scott Johnson', 'johnson.se@pg.com', 'johnson.se')
Scott.make_deposit(97.34)
Scott.make_withdrawal(44.56)
Scott.info()

Jane = User('Jane Doe', 'doe.j@pg.com',
            'doe.j').make_deposit(1000).make_withdrawal(300).info()

Jim = User('Jim Bob', 'bob.j@pg.com', 'bob.j')
Jim.make_deposit(150)


Scott.transfer_money(Jim, 52.78)
Scott.info()
Jim.info()

Scott.make_deposit(100).make_deposit(
    200).make_deposit(300).make_withdrawal(50).info()
