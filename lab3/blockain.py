from pow import pow
from hashlib import sha256

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
        message = str(self.index) + '\n'
        message += self.previous_hash  + '\n'
        message += self.data[0] + self.data[1]
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
    
    def add_block(self, block):
        """
        Raise an assertion error if the block is not valid, otherwise add the block to the blockchain
        """
        assert block.index >= 0 , 'Invalid index!'
        assert len(block.data) == 2 , 'Invalid data!'
        assert block.index != 0 or not self.blocks , 'Blockchain already have index 0'
        assert block.previous_hash or block.index == 0 , 'Previous hash cannot be empty if index is not 0'
        assert block.hash()[:self.TRESHOLD] == '0' * self.TRESHOLD,  'Invalid hash!'

        for b in self.blocks:
            if b == block:  # This works because we defined __eq__ to compare blocks
                raise AssertionError('Block already exists!')

        if self.blocks:
            if self._verify_block(block):
                self.blocks.append(block)
            else:
                raise AssertionError('Block could not be verified!')
        else:
            self.blocks.append(block)
            self.initialized = True

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

    def __repr__(self):
        """
        Method to represents all the blocks within the blockchain
        """
        message = ''
        for block in self.blocks:
            message +=  '-'* 80 + '\n'
            message +=  'Block #{}: hash: {}'.format(block.index, block.hash())
            message +=  '\n' + '-'* 80 + '\n' + block.message()
        
        return message
        

def add_block_to_blockchain(block, blockchain):
    """
    A helper function that execute the method add_block and handles assertion errors with appropriate messages.
    """
    try:
        blockchain.add_block(block)
        print('==> Block {} with hash {} added successfully!'.format(block.index, block.hash()))

    except AssertionError as e:
        print('XXX Invalid block {}:'.format(block.hash()), e.args[0])


if __name__ == '__main__':
    # Create a generator with data from records.txt file
    records = (line for line in open('records.txt', 'r'))

    # Create Blockchain
    blockchain = Blockchain()

    # Create the first block and mine it
    block1 = Block(0, [next(records), next(records)])
    block1.mine()
    add_block_to_blockchain(block1, blockchain)

    # Try to create another block with same index 0
    block2 = Block(0, [next(records), next(records)])
    block2.mine()
    add_block_to_blockchain(block2, blockchain)

    # Try to add block with invalid index
    block3 = Block(-15, [next(records), next(records)])
    block3.mine()
    add_block_to_blockchain(block3, blockchain)

    # try to add the block with index 1, without previous hash
    block4 = Block(1, [next(records), next(records)])
    block4.mine()
    add_block_to_blockchain(block4, blockchain)

    # Add a valid block with index 1
    block5 = Block(1, [next(records), next(records)], block1.hash())
    block5.mine()
    add_block_to_blockchain(block5, blockchain)

    # Try adding block witout mining
    block6 = Block(1, [next(records), next(records)], block5.hash())
    add_block_to_blockchain(block6, blockchain)

    # Try adding block with invalid data
    block7 = Block(1, [next(records), next(records), next(records)], block5.hash())
    add_block_to_blockchain(block7, blockchain)

    # Add block with index 1 (creating another chain)
    block8 = Block(1, [next(records), next(records)], block1.hash())
    block8.mine()
    add_block_to_blockchain(block8, blockchain)

    # Add multiple blocks
    previous_hash = block8.hash()
    for i in range(2, 10):
        block = Block(i, [next(records), next(records)], previous_hash)
        block.mine()
        add_block_to_blockchain(block, blockchain)
        previous_hash = block.hash()

    # Show all blocks
    print(blockchain)


"""Output
==> Block 0 with hash 000814b652e9173eae09e7cc5a91d6aad4a028a9cde56e90b8c5ef40582e2a18 added successfully!
XXX Invalid block 0004262ace7e7951933854badcba9ac0a5b41695dbf14133c3d3bcbbcbfe7e2a: Blockchain already have index 0
XXX Invalid block 000be95caeb58919b1057230e2237874682459a373ad363cf25e2c28ab3f961c: Invalid index!
XXX Invalid block 00080c087b819cc3ea4fb60e88c75bf4f22a5a7f3f277a2fca9dd2f0d1054bdd: Previous hash cannot be empty if index is not 0
==> Block 1 with hash 00048171d432fef3fe23ac62714a301f8f611c30d4d15feb4f0d71047d01db4d added successfully!
XXX Invalid block 9e21dd054fb15f522e08ea2cf3538150cabf8667b13817555da3797c97084a76: Invalid hash!
XXX Invalid block 277413b25e8cdccddd506dfecfac8692b4ebeb5e93215bf9997b88d30d13903a: Invalid data!
==> Block 1 with hash 0005740e9c56bebc150db86e581a732d981a4ff765dd204720c591216255fc3b added successfully!
==> Block 2 with hash 0004ad0fcbf34287ed6da9844236b34ec5f77845df96feb310e5838ad5c136ad added successfully!
==> Block 3 with hash 0006b49c35fd4fc4db89e38cc65822a23490f422b542dc375cf6046674d240c2 added successfully!
==> Block 4 with hash 000c6399b1029686d5930249bb86578eebcceb665d1f4d6061fc2cca8b1eac06 added successfully!
==> Block 5 with hash 000c3c4701870092bed7bb5a57f90a677be5eecca74c98b6ad60e5995cd26a1d added successfully!
==> Block 6 with hash 000fb099a476a846db971ace4747099595ee120da4fca39378aa9b7a1e5b8675 added successfully!
==> Block 7 with hash 00034779280d4c12cf24054dc27d8481f812c73f755b7798ed12f99b82a89011 added successfully!
==> Block 8 with hash 000696a9fb2736ab34903ff2fb882d4a0381b953687de503b3bcbf95ddef0659 added successfully!
==> Block 9 with hash 0004f76fb6c4a2d676940016897eb6dac0de3cd0a7a2dd0ab061e23635cd5310 added successfully!
--------------------------------------------------------------------------------
Block #0: hash: 000814b652e9173eae09e7cc5a91d6aad4a028a9cde56e90b8c5ef40582e2a18
--------------------------------------------------------------------------------
0

resink
transversomedial
--------------------------------------------------------------------------------
Block #1: hash: 00048171d432fef3fe23ac62714a301f8f611c30d4d15feb4f0d71047d01db4d
--------------------------------------------------------------------------------
1
000814b652e9173eae09e7cc5a91d6aad4a028a9cde56e90b8c5ef40582e2a18
punnigram
imminution
--------------------------------------------------------------------------------
Block #1: hash: 0005740e9c56bebc150db86e581a732d981a4ff765dd204720c591216255fc3b
--------------------------------------------------------------------------------
1
000814b652e9173eae09e7cc5a91d6aad4a028a9cde56e90b8c5ef40582e2a18
knotwort
apocodeine
--------------------------------------------------------------------------------
Block #2: hash: 0004ad0fcbf34287ed6da9844236b34ec5f77845df96feb310e5838ad5c136ad
--------------------------------------------------------------------------------
2
0005740e9c56bebc150db86e581a732d981a4ff765dd204720c591216255fc3b
escortee
dogwatch
--------------------------------------------------------------------------------
Block #3: hash: 0006b49c35fd4fc4db89e38cc65822a23490f422b542dc375cf6046674d240c2
--------------------------------------------------------------------------------
3
0004ad0fcbf34287ed6da9844236b34ec5f77845df96feb310e5838ad5c136ad
eaglewood
unbrotherliness
--------------------------------------------------------------------------------
Block #4: hash: 000c6399b1029686d5930249bb86578eebcceb665d1f4d6061fc2cca8b1eac06
--------------------------------------------------------------------------------
4
0006b49c35fd4fc4db89e38cc65822a23490f422b542dc375cf6046674d240c2
mulse
dermobranchiata
--------------------------------------------------------------------------------
Block #5: hash: 000c3c4701870092bed7bb5a57f90a677be5eecca74c98b6ad60e5995cd26a1d
--------------------------------------------------------------------------------
5
000c6399b1029686d5930249bb86578eebcceb665d1f4d6061fc2cca8b1eac06
typhic
poststertorous
--------------------------------------------------------------------------------
Block #6: hash: 000fb099a476a846db971ace4747099595ee120da4fca39378aa9b7a1e5b8675
--------------------------------------------------------------------------------
6
000c3c4701870092bed7bb5a57f90a677be5eecca74c98b6ad60e5995cd26a1d
indevout
anatomicopathologic
--------------------------------------------------------------------------------
Block #7: hash: 00034779280d4c12cf24054dc27d8481f812c73f755b7798ed12f99b82a89011
--------------------------------------------------------------------------------
7
000fb099a476a846db971ace4747099595ee120da4fca39378aa9b7a1e5b8675
unimpenetrable
hoggy
--------------------------------------------------------------------------------
Block #8: hash: 000696a9fb2736ab34903ff2fb882d4a0381b953687de503b3bcbf95ddef0659
--------------------------------------------------------------------------------
8
00034779280d4c12cf24054dc27d8481f812c73f755b7798ed12f99b82a89011
urrhodin
Dioecia
--------------------------------------------------------------------------------
Block #9: hash: 0004f76fb6c4a2d676940016897eb6dac0de3cd0a7a2dd0ab061e23635cd5310
--------------------------------------------------------------------------------
9
000696a9fb2736ab34903ff2fb882d4a0381b953687de503b3bcbf95ddef0659
unchapter
nonumbilicate
"""