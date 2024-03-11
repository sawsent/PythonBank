import csv

class Account:
    all = []

    @classmethod
    def get_open_accounts(cls, file):
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            items = list(reader)
        
        for item in items:
            Account(
                name=str(item.get('name')),
                starting_value=float(item.get('value'))
                )
                
    def __init__(self, name: str, starting_value=0):
        self.name = name
        self.__value = starting_value  # the name can be changed, but the value can only be changed through the funcs

        self.all.append(self)
    
    @property
    def value(self):
        return self.__value
    
    def get_details(self):
        return {'name': self.name, 'value': self.__value}
    
    def get_readable_details(self):
        details = self.get_details()
        return f"> Account Name: {details['name']}\n> Account Value: {details['value']}€"

    def deposit(self):
        while True:
            user_input = input("How much do you want to deposit?\n»» ")
            if user_input == 'cancel': return

            amount_to_deposit = round(float(user_input), 2)
            if amount_to_deposit > 0:
                break
            else: print("Can't deposit negative amounts of money!")

        self.__value += amount_to_deposit
        print(f"Successfully deposited {amount_to_deposit}€, your new balance is {self.__value}€!")

    def add_money(self, money: float):
        self.__value += round(money, 2)

    def remove_money(self, money: float):
        self.__value -= round(money, 2)

    def withdraw(self):
        while True:
            user_input = input("How much do you want to withdraw?\n»» ")
            if user_input == 'cancel': return
            amount_to_withdraw = round(float(user_input), 2)
            if amount_to_withdraw <= self.__value and amount_to_withdraw > 0:
                break
            else: print(f"Can't withdraw more money than your current balance or negative money: {self.__value}€")
            
        self.__value -= amount_to_withdraw
        print(f"Successfully withdrew {amount_to_withdraw}€, your new balance is {self.__value}€!")

    def destroy(self):
        self.all.remove(self)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.__value})"