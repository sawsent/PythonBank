import csv
from account import Account
from savings import Savings

# ACTIONS YOURE ABLE TO DO: 
# OPEN ACCOUNT -> need to:      - select the type
#                               - if normal: give it a name and a starting value
#                               - if savings: select which account from
# CLOSE ACCOUNT -> destroy an account
# withdraw: from normal
# move: from normal -> savings / savings -> normal
# deposit: to normal

def get_action_to_take():
    while True:
        print("What action do you want to do?")
        print("Available actions are: 'open account', 'close account', 'move', 'deposit', 'withdraw', 'change interest payment receiver', 'check account details', 'skip month', 'save and quit'.")
        action_to_take = input("»» ")
        if action_to_take in ['change interest payment receiver', 'check account details', 'skip month', 'open account', 'close account', 'move', 'deposit', 'withdraw', 'save and quit']:
            return action_to_take
        else: print("Please select one of the available options!")

def select_account(display_text, available_accounts):
    print(display_text)
    selected_account = input(f"Available accounts are: {list(available_accounts.keys())}!\n»» ")
    return available_accounts[selected_account]

def open_account(acc_type, open_accounts):
    if acc_type == 'savings':
        if open_accounts == {}:
            print("You have no open Accounts! Please open a checking account first!")
            return
        connected_account = select_account("Please select the the account you want to connect to your savings account!", open_accounts)
        name = input("Please select the name for your savings account!\n»» ")
        starting_value = float(input("Please select the constitution value for your savings account!\n»» "))
        connected_account.remove_money(starting_value)

        Savings(name, starting_value, connected_account)

        print(f"Successfully opened a Savings account! Name:'{name}', Value: {starting_value}€.\n\
The new value on your checking account: '{connected_account.name}' is {connected_account.value}€!")

    if acc_type == 'checking':
        name = input("Please select the name for your checking account!\n»» ")
        starting_value = float(input("Please select the constitution value for your checking account!\n»» "))
        Account(name, starting_value)
        print(f"Created new checking account: Name: '{name}', value: '{starting_value}'!")

def move(account_from, account_to):
    print(f"How much money do you want to move? You have {account_from.value}€ in your account: '{account_from.name}'!")
    money_to_move = float(input("»» "))
    account_from.remove_money(money_to_move)
    account_to.add_money(money_to_move)
    print(f"Successfully moved {money_to_move}€ from '{account_from.name}' to '{account_to}'!")
    print(f"'{account_from.name}' new balance: {account_from.value}€")
    print(f"'{account_to.name}' new balance: {account_to.value}€")

def load_user(user: str):
    Account.get_open_accounts(f"../data/{user}checking.csv")
    Savings.get_open_accounts(f"../data/{user}savings.csv")

def save(user:str, all_accounts, savings_accounts):
    for account in list(savings_accounts.keys()):
        all_accounts.pop(account)

    header = ['name', 'value']
    with open(f"../data/{user}checking.csv", 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for account in all_accounts.values():
            writer.writerow([account.name, account.value])
    
    with open(f"../data/{user}savings.csv", 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for account in savings_accounts.values():
            writer.writerow([account.name, account.value])

def running_interface(user=None):
    user = user
    running = True

    # if there are no accounts, force create a checking account
    if Account.all == []:
        print("There are no open accounts, please open a checking account!")
        open_account('checking', {})
    
    while running:
        
        # updating existing accounts
        open_accounts = {x.name: x for x in Account.all}
        open_savings_accounts = {x.name: x for x in Savings.all_savings}

        # getting the action
        action_to_take = get_action_to_take()
        
        if action_to_take == 'save and quit': 
            save(user, open_accounts, open_savings_accounts)
            break

        if action_to_take == 'open account':
            acc_type = input("Please select the type of account you want to open! ('checking' or 'savings')\n»» ")
            open_account(acc_type, open_accounts)

        if action_to_take == 'close account':
            account_to_destroy = select_account("Please select the the account you want to close!", open_accounts)
            account_to_destroy.destroy()
            print(f"Success, {account_to_destroy.name} was closed! It had {account_to_destroy.value}€!")
        
        if action_to_take == 'deposit':
            account_to_deposit = select_account("Please select the account you want to deposit to!", open_accounts)
            account_to_deposit.deposit()
        
        if action_to_take == 'withdraw':
            account_to_deposit = select_account("Please select the account you want to withdraw from!", open_accounts)
            account_to_deposit.withdraw()

        if action_to_take == 'move':
            account_from = select_account("Select the account you want to move money from!", open_accounts)
            account_to = select_account("Select the account you want to move money to!", open_accounts)
            move(account_from, account_to)

        if action_to_take == 'check account details':
            account_to_check = select_account("Please select the account you want to check!", open_accounts)
            print(account_to_check.get_readable_details())
        
        if action_to_take == 'change interest payment receiver':
            if open_savings_accounts == {}:
                print("You don't have any open savings accounts!")
            else:
                account_to_switch = select_account("Select Savings Account to change receiver!", open_savings_accounts)
                new_receiver = select_account(f"Original receiver is {account_to_switch.name}! Please select new receiver!", open_accounts)
                account_to_switch.returns_to = new_receiver
                print(f"{account_to_switch.name}'s interest payments will now go to {new_receiver.name}")

        if action_to_take == 'skip month':
            for account in open_savings_accounts.values():
                interest = account.get_interest()
                account.pay_interest(interest)
                print(f"{account.name} yielded {interest}€ to {account.returns_to.name}!")
            
            print("Your Accounts:\n")
            for account in open_accounts.values():
                print(account.get_readable_details(), "\n")

# selecting user: 

if __name__ == '__main__':
    print("Welcome to this simple banking system!\n")
    print("Please type your username!")
    user = input("»» ")
    users = []

    with open('../data/users.csv', 'r') as f:
        reader = csv.DictReader(f)
        bad_users = list(reader)
        for old_user in bad_users:
            users.append(str(old_user.get('user')))

    if user in users:
        load_user(user)
        running_interface(user)
    
    else: 
        with open('../data/users.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([user,])
        with open(f'../data/{user}checking.csv', 'w') as f:
            writer = csv.writer(f)
        with open(f'../data/{user}savings.csv', 'w') as f:
            writer = csv.writer(f)
        print(f"New User Created: {user}\n")
        running_interface(user)
    