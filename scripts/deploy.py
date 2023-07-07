from brownie import certificateFactory, accounts
from dotenv import load_dotenv

load_dotenv()

def main():
    account = accounts[0]
    deployFactory(account)

def deployFactory(_from):
    factory = certificateFactory.deploy({
        'from': _from,
        'priority_fee': '1 wei'
    })
    print(f'Factory deployed at {factory}!')
    return factory
