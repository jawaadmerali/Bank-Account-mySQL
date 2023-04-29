import mysql.connector


db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Jawaad123!',
    database = 'project_schema'
)  

cursor = db.cursor(buffered=True)
db.autocommit = True

def account():
    first_name = input("What is your first name?: ")
    last_name = input("What is your last name?: ")
    birth_date = input("When is your birthday?  ")
    password = int(input("Create password: "))
    starting_balance = int(input("How much do you want to deposit?: "))
    cursor.execute("INSERT INTO bank_account (firstname, lastname, birthday, password, balance) VALUES (%s,%s,%s,%s,%s)", (first_name, last_name, birth_date, password, starting_balance))
    print("Account successfully made!")
    

def operation(id):
    exit1 = 'N'
    while exit1 != 'Y':
        operation_decision = input("What would you like to do with your account? (Deposit, Withdraw, Check balance, Settings, Exit): ")
        if operation_decision == 'Check Balance':
            cursor.execute("SELECT balance FROM bank_account WHERE idbank_accounts = %s", (id))
            print(cursor.fetchone())
        elif operation_decision == "Deposit":
            get_deposit(id)
        elif operation_decision == "Withdraw":
            get_withdrawal(id)
        elif operation_decision == "Settings":
            settings(id)
        else:
            exit_prompt = input("Would you like to exit?")
            if exit_prompt == 'Y':
                exit1 = 'Y'

def get_deposit(id):
    id1 = str(id)
    id2 = id1.replace("(","").replace(",","").replace(")","")
    id3 = int(id2)
    cursor.execute("SELECT balance FROM bank_account WHERE idbank_accounts = %s", (id))
    balance_raw = str(cursor.fetchone())
    balance_intermediate = balance_raw.replace("(","").replace(",","").replace(")","")
    balance_final = int(balance_intermediate)
    deposit_amount = int(input("How much would you like to deposit?"))
    new_balance = balance_final + deposit_amount
    cursor.execute(f"UPDATE bank_account SET balance = {new_balance} WHERE idbank_accounts = {id3}")

def get_withdrawal(id):
    id1 = str(id)
    id2 = id1.replace("(","").replace(",","").replace(")","")
    id3 = int(id2)
    cursor.execute("SELECT balance FROM bank_account WHERE idbank_accounts = %s", (id))
    balance_raw = str(cursor.fetchone())
    balance_intermediate = balance_raw.replace("(","").replace(",","").replace(")","")
    balance_final = int(balance_intermediate)
    deposit_amount = int(input("How much would you like to withdraw?"))
    new_balance = balance_final - deposit_amount
    cursor.execute(f"UPDATE bank_account SET balance = {new_balance} WHERE idbank_accounts = {id3}")
    

def login():
    correct_password = 'N'
    while correct_password != 'Y':
        password1 = int(input("Password: "))
        cursor.execute(f"SELECT idbank_accounts, firstname FROM bank_account WHERE password = {password1}")
        if cursor.fetchone() != None:
            cursor.execute(f"SELECT idbank_accounts FROM bank_account WHERE password = {password1}")
            id_raw = cursor.fetchone()
            correct_password = 'Y'
            operation(id_raw)
        else:
            print("Try again")

def settings(id):
    exit = 'N'
    while exit != 'Y':
        what_setting = input("Settings: Change name, Delete account: ")
        if what_setting == "change name":
            id1 = str(id)
            id2 = id1.replace("(","").replace(",","").replace(")","")
            id3 = int(id2)
            first_name = input('What is your first name?')
            last_name = input("What is your last name?")
            cursor.execute(f"UPDATE bank_account SET firstname = '{first_name}', lastname = '{last_name}' WHERE idbank_accounts = {id3}")
            print("Name updated!")
        elif what_setting == "delete account":
            cursor.execute("DELETE FROM bank_account WHERE idbank_accounts = %s", (id))
            print("Account has been deleted!")
            exit = 'Y'
        elif what_setting == "check everything":
            cursor.execute("SELECT * FROM bank_account WHERE idbank_accounts = %s", (id))
            print(cursor.fetchone())
        else:
            exit_prompt = input("Would you like to exit?")
            if exit_prompt == 'Y':
                exit = 'Y'


exit = 'N'
while exit != 'Y':
    print("Welcome to my bank!")
    has_account = input("Do you have an account? (Y or N)")
    if has_account == 'Y':
        login()
    else:
        like_to_make_acc = input("Would you like to make an account? (Y or N)")
        if like_to_make_acc == 'Y':
            account()
    print("Welcome to my bank!")
    exit_prompt = input("Would you like to exit?")
    if exit_prompt == 'Y':
        exit = 'Y'
        break

print("Come back Soon!")
