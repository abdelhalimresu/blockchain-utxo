from blockain import Block
from blockain import Blockchain
from blockain import Wallet
from blockain import Transaction
from blockain import UTXO


def create_transaction(wallet, recipients):
    """
    A helper function that create and return a transaction and handles assertion errors with appropriate messages.
    """
    try:
        return wallet.create_transaction(recipients)

    except AssertionError as e:
        print('Error :', e.args[0])


def add_block_to_blockchain(block, blockchain, utxo):
    """
    A helper function that execute the method add_block and handles assertion errors with appropriate messages.
    """
    try:
        blockchain.add_block(block, utxo)
        print('==> Block {} with hash {} added successfully!'.format(block.index, block.hash()))

    except AssertionError as e:
        print('XXX Invalid block {}:'.format(block.hash()), e.args[0])


def print_balance(name, wallet):
    unspent_outputs = wallet.get_unspent_outputs()
    print('{} wallet contains {} coin!'.format(name, sum([unspent_output[2] for unspent_output in unspent_outputs])))


if __name__ == '__main__':

    # Create Blockchain
    blockchain = Blockchain()

    # Create UTXO instance 
    utxo = UTXO(blockchain)

    # Create users wallets
    alice = Wallet(blockchain)
    halim = Wallet(blockchain)
    maryam = Wallet(blockchain)

    # Prepare the first block with transaction created manually with NULL input
    block1_data = []
    transaction = Transaction()
    transaction.add_output(100, alice.publicKey)
    block1_data.append(transaction)
    transaction = Transaction()
    transaction.add_output(100, halim.publicKey)
    block1_data.append(transaction)
    transaction = Transaction()
    transaction.add_output(100, maryam.publicKey)
    block1_data.append(transaction)
    # Create and mine the block
    block1 = Block(0, block1_data)
    block1.mine()
    add_block_to_blockchain(block1, blockchain, utxo)

    # Prepare a second block with transactions made by users.
    block2_data = []
    block2_data.append(create_transaction(alice, [{'publicKey': halim.publicKey, 'value': 10}]))
    block2_data.append(create_transaction(halim, [{'publicKey': maryam.publicKey, 'value': 50}]))
    block2_data.append(create_transaction(maryam, [{'publicKey': halim.publicKey, 'value': 5}]))
    block2 = Block(1, block2_data, block1.hash())
    # Create and mine the block
    block2.mine()
    add_block_to_blockchain(block2, blockchain, utxo)

    # Prepare another block with transactions made by users.
    block3_data = []
    block3_data.append(create_transaction(alice, [{'publicKey': halim.publicKey, 'value': 10}]))
    block3_data.append(create_transaction(halim, [{'publicKey': maryam.publicKey, 'value': 15}]))
    block3_data.append(create_transaction(maryam, [{'publicKey': alice.publicKey, 'value': 15}]))
    block3 = Block(2, block3_data, block2.hash())
    # Create and mine the block
    block3.mine()
    add_block_to_blockchain(block3, blockchain, utxo)

    # Prepare another block with transactions made by users.
    block4_data = []
    block4_data.append(create_transaction(alice, [{'publicKey': halim.publicKey, 'value': 10}]))
    block4_data.append(create_transaction(halim, [{'publicKey': maryam.publicKey, 'value': 30}]))
    block4_data.append(create_transaction(maryam, [{'publicKey': halim.publicKey, 'value': 70}]))
    block4 = Block(3, block4_data, block3.hash())
    # Create and mine the block
    block4.mine()
    add_block_to_blockchain(block4, blockchain, utxo)

    # Show the blockchain data
    print(blockchain)

    # Show wallets
    print_balance('alice', alice)
    print_balance('halim', halim)
    print_balance('maryam', maryam)


