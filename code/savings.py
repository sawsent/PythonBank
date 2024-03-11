import csv
from account import Account

class Savings(Account):
    monthly_interest_rate = 0.02
    all_savings = []

    @classmethod
    def get_open_accounts(cls, file):
        with open(file, "r") as f:
            reader = csv.DictReader(f)
            items = list(reader)
        
        for item in items:
            Savings(
                name=str(item.get('name')),
                starting_value=float(item.get('value'))
                )
            
    def __init__(self, name, starting_value, connected_account=None):
        super().__init__(name, starting_value)
        self.returns_to = self
        self.all_savings.append(self)

    def get_details(self):
        return {'name': self.name, 'value': self.value, 'interest rate': self.monthly_interest_rate, 'returns to': self.returns_to}
    
    def get_readable_details(self):
        details = self.get_details()
        return f"\
> This is a Savings Account!\n> Account Name: {details['name']}\n\
> Account Value: {details['value']}€\n\
> The interest rate of this account is: {details['interest rate']}\n\
> The interest payments are going to the account: '{details['returns to'].name}'"

    def change_interest_payment_receiver(self, new_account):
        self.returns_to = new_account
        
    def get_interest(self):
        return round(self.value * self.monthly_interest_rate, 2)

    def pay_interest(self, interest):
        self.returns_to.add_money(interest)