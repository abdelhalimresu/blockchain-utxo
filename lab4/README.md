# Unspent Transaction Output

## Overview

This lab implements a system of transactions following the UTXO model with simple classes and main program to test the implementation.

## Classes

* ```Input```: a simple class that represents an input and contains 3 fields preTxHash, outIndex and Signature, although the signature represents the encryption of the component e of the public key, it is not secure because anyone can simply reuse this signature for other transactions.

* ```Output```: class for Output, contains 4 fields: index, value, publicKey and additional boolean field spent which indicates whether this output is consumed or not.

* ```Transaction```: A simple class that allows adding inputs and outputs (without verification), and has a ```hash``` method to return the SHA256 of the transaction.

* ```UTXO```: The class responsible of keeping track of the Unspent outputs, validate and execute transactions. There are two main methods:
    - ```validate_transaction```: Verify if there's enough outputs that are unspent to satisfy the spendings (the sum of inputs is greater or equal the sum of outputs), also verify the signature of the given publickey.
    - ```execute_transaction```: if the transaction is valid, mark the outputs as spent, and add it the transactions database.
    - In addition to these methods, there's a representation method that diplays all the transaction in the UTXO. in the following format:
```
        --------------------------------------------------------------------------------
        Transaction:  bb93a5f5870545f4b0a0a04226d2baddc83628872460ebdad004c206466612f3
        --------------------------------------------------------------------------------
        Inputs: 
        --> preTxHash: 161cc718138ef06ec10840b6f7ad24b6944dacfad7b77cd9b2f375b43a006e44
            outIndex: 0
            signature: 101079189330851472
        --> preTxHash: f39d63e34158541eca11ca1f47af40e640a910049fd9cc3af558bb3325437b9d
            outIndex: 0
            signature: 101079189330851472
        Outputs: 
        --> index: 0
            value: 2
            publicKey: (257, 4475943590943616321)
        --> index: 1
            value: 2.5
            publicKey: (83, 11773908048679821791)
        --> index: 2
            value: 0.5
            publicKey: (239, 3573570961347180217)
```
* ```Wallet```: A client representing a user withing the UTXO protocol, identified with public key and can create transactions that can be verified and executed by an UTXO instance. the main methods are:
    - ```signature```: returns the encryption of the RSA e of the public key, using the private key.
    - ```create_transaction```: Create a transaction from a list of dictionnaries, each dictionary contains the public key of the reciever and the amount of coins to be sent, this method looks for the minimum unspent output referencing the owner of the public key and use them accordingly to satisfy the outputs, also it sends the remaining (sum of input - sum of outputs) back to the sender as a change.
    - ```get_transactions```: get all transaction referencing the public key of the owner of the wallet.
    - ```get_unspent_outputs```: get all the unspent outputs referencing the public key of the owner of the wallet.

## Test

To test the implementation, we created 4 wallets, one for alice, bob, halim and maryam. and perform the following transaction:

- **Transaction 1**: sends 10 coins to each alice and bob, as it is the first transaction, there's no input and the UTXO class is implemented to execute the first transaction without validation.
- **Transaction 2**: from alice wallet, send 3 coins to halim and 4 coins to bob. this transaction is accepted since alice has 10 coins in the unspent output from the previous transaction.
- **Transaction 3**: from alice wallet, send 2 coins to halim and 0.5 coin to maryam.
- **Transaction 4**: from halim wallet, send 2 coins to bob and 2.5 coin to maryam. this transaction uses 2 inputs (3 + 2) and 3 outputs 2 to bob, 2.5 to maryam and 0,5 to halim as a change.
- **Transaction 5**: from halim wallet, send 2 coins to bob, this transaction will fail since halim has only 0.5 in the unspent output.

This is the output of ```print(utxo)```:

```
--------------------------------------------------------------------------------
 Transaction:  c9b966c0859ee495381f0c22cabf329525a574c9ba85adef0fd817a667e41a9f
--------------------------------------------------------------------------------
Inputs: 
Outputs: 
 --> index: 0
     value: 10
     publicKey: (257, 9535823202615331729)
 --> index: 1
     value: 10
     publicKey: (191, 12223045814293872791)
--------------------------------------------------------------------------------
 Transaction:  df0830eda3634795c91b5adbc810eea810a04c65b0d196899b37ea18ec4bb281
--------------------------------------------------------------------------------
Inputs: 
 --> preTxHash: c9b966c0859ee495381f0c22cabf329525a574c9ba85adef0fd817a667e41a9f
     outIndex: 0
     signature: 4702376880746884655
Outputs: 
 --> index: 0
     value: 3
     publicKey: (227, 3491524140139484719)
 --> index: 1
     value: 4
     publicKey: (191, 12223045814293872791)
 --> index: 2
     value: 3
     publicKey: (257, 9535823202615331729)
--------------------------------------------------------------------------------
 Transaction:  5ced07cc50f6ba9690dbc753a10cd7e69009d6be986d66169818939c6e978047
--------------------------------------------------------------------------------
Inputs: 
 --> preTxHash: df0830eda3634795c91b5adbc810eea810a04c65b0d196899b37ea18ec4bb281
     outIndex: 2
     signature: 4702376880746884655
Outputs: 
 --> index: 0
     value: 2
     publicKey: (227, 3491524140139484719)
 --> index: 1
     value: 0.5
     publicKey: (293, 7895063165325224293)
 --> index: 2
     value: 0.5
     publicKey: (257, 9535823202615331729)
--------------------------------------------------------------------------------
 Transaction:  9e9851b83882c4f66b4beea53db7f23a25265a7eec60740bbe643ebd12706bd8
--------------------------------------------------------------------------------
Inputs: 
 --> preTxHash: df0830eda3634795c91b5adbc810eea810a04c65b0d196899b37ea18ec4bb281
     outIndex: 0
     signature: 1867187925481620120
 --> preTxHash: 5ced07cc50f6ba9690dbc753a10cd7e69009d6be986d66169818939c6e978047
     outIndex: 0
     signature: 1867187925481620120
Outputs: 
 --> index: 0
     value: 2
     publicKey: (191, 12223045814293872791)
 --> index: 1
     value: 2.5
     publicKey: (293, 7895063165325224293)
 --> index: 2
     value: 0.5
     publicKey: (227, 3491524140139484719)

Error : Unspent outputs cannot satisfy this transaction
```