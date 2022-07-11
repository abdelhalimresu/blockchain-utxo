from utxo import UTXO
from utxo import Wallet
from utxo import Transaction


def create_transaction(utxo, wallet, recipients):
    try:
        transaction = wallet.create_transaction(recipients)
        utxo.execute_transaction(transaction)
    except AssertionError as e:
        print('Error :', e.args[0])


if __name__ == '__main__':
    # Create UTXO instance 
    utxo = UTXO()

    # Create users wallets
    alice = Wallet(utxo)
    bob = Wallet(utxo)
    halim = Wallet(utxo)
    maryam = Wallet(utxo)

    # Create a transaction with no inputs that gives alice and bob 10 coins each
    transaction = Transaction()
    transaction.add_output(10, alice.publicKey)
    transaction.add_output(10, bob.publicKey)

    # This is the first transaction and wont be validated, it'll be executed directly
    utxo.execute_transaction(transaction)

    # Create and execute a transactions using create_transaction helper function
    create_transaction(
        utxo,
        alice,
        [{
            'publicKey': halim.publicKey,
            'value': 3
        },
        {
            'publicKey': bob.publicKey,
            'value': 4
        }]
    )
    create_transaction(
        utxo,
        alice,
        [{
            'publicKey': halim.publicKey,
            'value': 2
        },
        {
            'publicKey': maryam.publicKey,
            'value': 0.5
        }]
    )
    create_transaction(
        utxo,
        halim,
        [{
            'publicKey': bob.publicKey,
            'value': 2
        },
        {
            'publicKey': maryam.publicKey,
            'value': 2.5
        }]
    )
    print(utxo)

    # Try to create transaction with insufficient utxo
    create_transaction(
        utxo,
        halim,
        [{
            'publicKey': bob.publicKey,
            'value': 2
        }]
    )
