from objects import Accounts
import backend

if __name__ == "__main__":
    backend.init()
    accounts = Accounts()
    account = accounts.who('hana292sale')

    if account is not None:
        print(account.get('Key'))
