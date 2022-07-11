from pow import pow
from hashlib import sha256
from rsa import generateKeys, encrypt, decrypt
from hashlib import sha256

class Input:

    def __init__(self, preTxHash, outIndex, signature):
        self.preTxHash = preTxHash
        self.outIndex = outIndex
        self.signature = signature


class Output:

    def __init__(self, index, value, publicKey):
        self.index = index
        self.value = value
        self.publicKey = publicKey
        self.spent = False
    
    def spend(self):
        self.spent = True


class Transaction:

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.index = 0

    def message(self):
        message = ' Inputs: \n'
        for input in self.inputs:
            message += ' --> preTxHash: ' + str(input.preTxHash) + '\n'
            message += '     outIndex: ' + str(input.outIndex) + '\n'
            message += '     signature: ' + str(input.signature) + '\n'
        message += ' Outputs: \n'
        for output in self.outputs:
            message += ' --> index: ' + str(output.index) + '\n'
            message += '     value: ' + str(output.value) + '\n'
            message += '     publicKey: ' + str(output.publicKey) + '\n'
        return message

    def hash(self):
        sha256_hash = sha256((self.message()).encode('utf-8'))
        return sha256_hash.hexdigest()

    def add_input(self, preTxHash, outIndex, signature):
        input = Input(preTxHash, outIndex, signature)
        self.inputs.append(input)

    def add_output(self, value, publicKey):
        output = Output(self.index, value, publicKey)
        self.index += 1
        self.outputs.append(output)

    def __repr__(self):
        return self.message()


class Block:

    def __init__(self, index, data, previous_hash=''):
        """
        Initialize the block
        """
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0

    def mine(self):
        """
        Perform power of work until we get a hash with the specified treshold
        """
        self.nonce = pow(self.message(), Blockchain.TRESHOLD)

    def message(self):
        """
        Construct the block content: index + previous hash + data 
        """
        message = ' # Index: ' + str(self.index) + '\n'
        message += ' # Previous hash: ' + self.previous_hash  + '\n'
        message += ' # Transactions: \n'
        message += ' ' + '-'*80 + '\n  Transaction:  {}\n'.format(self.data[0].hash()) + ' ' + '-'*80 + '\n' + str(self.data[0])
        message += ' ' + '-'*80 + '\n  Transaction:  {}\n'.format(self.data[1].hash()) + ' ' + '-'*80 + '\n' + str(self.data[1])
        message += ' ' + '-'*80 + '\n  Transaction:  {}\n'.format(self.data[2].hash()) + ' ' + '-'*80 + '\n' + str(self.data[2])
        return message

    def hash(self):
        """
        Get the block hash calculed with the nonce
        """
        sha256_hash = sha256((self.message() + str(self.nonce)).encode('utf-8'))
        return sha256_hash.hexdigest()

    def __eq__(self, other):
        """
        Allow comparison between blocks, two blocks are said to be equal if they have the same message.
        """
        return self.message() == other.message()


class Blockchain:

    # Define treshold
    TRESHOLD = 6

    def __init__(self):
        """
        Initialize blocks with empty list
        """
        self.blocks = []
    
    def add_block(self, block, utxo):
        """
        Raise an assertion error if the block is not valid, otherwise add the block to the blockchain
        """
        assert block.index >= 0 , 'Invalid index!'
        assert len(block.data) == 3 , 'Invalid data!'
        assert block.index != 0 or not self.blocks , 'Blockchain already have index 0'
        assert block.previous_hash or block.index == 0 , 'Previous hash cannot be empty if index is not 0'
        assert block.hash()[:self.TRESHOLD] == '0' * self.TRESHOLD,  'Invalid hash!'

        for b in self.blocks:
            if b == block:  # This works because we defined __eq__ to compare blocks
                raise AssertionError('Block already exists!')

        if self.blocks:
            if self._verify_block(block) and self._verify_transactions(block.data, utxo):
                for transaction in block.data:
                    utxo.execute_transaction(transaction)
                self.blocks.append(block)
            else:
                raise AssertionError('Block could not be verified!')
        else:
            self.blocks.append(block)
            self.initialized = True

    def _verify_transactions(self, transactions, utxo):

        for transaction in transactions:
            if not utxo.validate_transaction(transaction):
                return False

        return True

    def _verify_block(self, new_block):
        """
        For a new block, search for all the blocks with (index - 1) and check if the new block
        reference one of them and return True
        return False otherwise
        """
        blocks = self._get_blocks_with_index(new_block.index - 1)

        if not blocks:
            return False
        
        for block in blocks:
            if block.hash() == new_block.previous_hash:
                return True
        
        return False

    def _get_blocks_with_index(self, index):
        """
        Given an index, retrun all blocks with this index.
        """
        blocks = []
        
        for block in self.blocks:
            if block.index == index:
                blocks.append(block)
        
        return blocks

    @property
    def transactions(self):
        transactions = {}
        for block in self.blocks:
            for data in block.data:
                transactions[data.hash()] = data
        return transactions

    def __repr__(self):
        """
        Method to represents all the blocks within the blockchain
        """
        message = ''
        for block in self.blocks:
            message +=  '-'* 84 + '\n'
            message +=  '| Block #{}: hash: {} |'.format(block.index, block.hash())
            message +=  '\n' + '-'* 84 + '\n' + block.message()
        
        return message


class UTXO:

    def __init__(self, blockchain):
        self.blockchain = blockchain

    def validate_transaction(self, transaction):

        input_sum = 0

        for input in transaction.inputs:
            outputs = self.blockchain.transactions.get(input.preTxHash).outputs

            for output in outputs:
                if output.index == input.outIndex:
                    msg = decrypt(input.signature, output.publicKey)

                    if output.publicKey[0] != msg or output.spent:
                        return False

                    input_sum += output.value

        output_sum = sum([output.value for output in transaction.outputs])

        if output_sum > input_sum:
            return False

        return True

    def execute_transaction(self, transaction):

        if self.validate_transaction(transaction) or not self.blockchain.transactions:
            for input in transaction.inputs:
                outputs = self.blockchain.transactions.get(input.preTxHash).outputs
 
                for output in outputs:
                    if output.index == input.outIndex:
                        output.spend()
 
            self.blockchain.transactions[transaction.hash()] = transaction

    def __repr__(self):
        message = ''
        for hash, tx in self.blockchain.transactions.items():
            message += '-'*80 + '\n Transaction:  {}\n'.format(hash) + '-'*80 + '\n' + repr(tx)
        return message


class Wallet:

    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.publicKey, self._privateKey = generateKeys(32)

    def signature(self):
        return encrypt(self.publicKey[0], self._privateKey)

    def create_transaction(self, recipients):
        # Create the transaction
        transaction = Transaction()
        # Get all unspent inputs
        unspent_outputs = self.get_unspent_outputs()
        # Assert that available unspent output can satisfy the spending
        input_sum = sum([unspent_output[2] for unspent_output in unspent_outputs])
        output_sum = sum([recipient['value'] for recipient in recipients])
        assert  input_sum > output_sum , 'Unspent outputs cannot satisfy this transaction'
        i = 0
        preTxHash, outIndex, total_input = unspent_outputs[i]
        transaction.add_input(preTxHash, outIndex, self.signature())
        total_output = 0
        for recipient in recipients:
            total_output += recipient['value']

            while total_output > total_input:
                i += 1
                preTxHash, outIndex, amount = unspent_outputs[i]
                total_input += amount
                transaction.add_input(preTxHash, outIndex, self.signature())

            transaction.add_output(recipient['value'], recipient['publicKey'])
            total_input -= recipient['value']
            total_output -= recipient['value']

        # Add output as a change to the sender's wallet
        if total_input != total_output:
            transaction.add_output(total_input, self.publicKey)

        return transaction

    def get_transactions(self):
        transactions = []
        for hash, transaction in self.blockchain.transactions.items():
            for output in transaction.outputs:
                if output.publicKey == self.publicKey:
                    transactions.append(transaction)
        return transactions

    def get_unspent_outputs(self):
        unspent_outputs = []
        for tx in self.get_transactions():
            for output in tx.outputs:
                if not output.spent and output.publicKey == self.publicKey:
                    unspent_outputs.append((tx.hash(), output.index, output.value))
        return unspent_outputs

