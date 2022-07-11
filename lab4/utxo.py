from email import message
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
        message = 'Inputs: \n'
        for input in self.inputs:
            message += ' --> preTxHash: ' + str(input.preTxHash) + '\n'
            message += '     outIndex: ' + str(input.outIndex) + '\n'
            message += '     signature: ' + str(input.signature) + '\n'
        message += 'Outputs: \n'
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


class UTXO:

    def __init__(self):
        self.transactions = {}

    def validate_transaction(self, transaction):

        input_sum = 0

        for input in transaction.inputs:
            outputs = self.transactions.get(input.preTxHash).outputs

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

        if self.validate_transaction(transaction) or not self.transactions:
            for input in transaction.inputs:
                outputs = self.transactions.get(input.preTxHash).outputs
 
                for output in outputs:
                    if output.index == input.outIndex:
                        output.spend()
 
            self.transactions[transaction.hash()] = transaction


    def __repr__(self):
        message = ''
        for hash, tx in self.transactions.items():
            message += '-'*80 + '\n Transaction:  {}\n'.format(hash) + '-'*80 + '\n' + repr(tx)
        return message


class Wallet:

    def __init__(self, utxo):
        self.utxo = utxo
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
        for hash, transaction in self.utxo.transactions.items():
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
