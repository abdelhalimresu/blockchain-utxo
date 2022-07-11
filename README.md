# Putting all together

## Overview

This lab implements a system of a bank based on blockchain and UTXO protocol to handle all the transactions made by clients.

A client is represented with a wallet, and can create transaction, with 3 transactions we can create a block that can be mined, verified and added to blockchain.

## Classes

This lab uses the same classes in lab3 (blockchain) and lab4 (UTXO), with some differences in some methods.

* ```UTXO```: The same class from lab4, but now it doesn't store any transaction, instead it retreive all the transactions from the blockchain.
* ```Wallet```: The same class from lab4, also depends on the blockchain to get unspent outputs, in order to create a valid transaction.
* ```Block```: Same class from lab3, but now the datablock is placeholder for 3 transactions instead of strings.
* ```Blockchain```: Same class from lab3, Uses UTXO to validate the datablock in addition to the previous validation in lab3.


## Test

To test the implementation, we created 3 wallets: alice, halim and maryam and performed the following scenario:

- **Block 0**: Contains 3 transactions, to send 100 coins to each wallet, those transactions are accepted without inputs.
- **Block 1**: Contains 3 transactions: alice 10 -> halim, halim 50 -> maryam, maryam 5 -> halim
- **Block 2**: Contains 3 transactions: alice 10 -> halim, halim 15 -> maryam, maryam 15 -> alice
- **Block 3**: Contains 3 transactions: alice 10 -> halim, halim 50 -> maryam, maryam 70 -> halim

At the end we print how much coins left in each of wallet. We can verify that the sum of all wallets is 300. because we always send the remaining back to the sender as a change.

This is the output of ```print(blockchain)``` in addition to ```print_balance('wallet', wallet)```:

```
==> Block 0 with hash 000000859b1bfac5d6ecafdea66bf717ca69a22825f3b15fde85c1fe2c524395 added successfully!
==> Block 1 with hash 0000004ac043d71c1904d35611f5ada5d97f33147eacbb327a5ed5de66dbc856 added successfully!
==> Block 2 with hash 000000c3aa7ca4f40c019ef4d7f43943c4e27768e1eb33cb8630e1de73d2c5a6 added successfully!
==> Block 3 with hash 0000008e8cba158b3c07ccbaba439444f4f5bddbaa77d8920181d81038af4af3 added successfully!
------------------------------------------------------------------------------------
| Block #0: hash: 000000859b1bfac5d6ecafdea66bf717ca69a22825f3b15fde85c1fe2c524395 |
------------------------------------------------------------------------------------
 # Index: 0
 # Previous hash: 
 # Transactions: 
 --------------------------------------------------------------------------------
  Transaction:  c817a49c6511eed70c4437712b194cce78d92c147f793272b5555b3bc046b9e4
 --------------------------------------------------------------------------------
 Inputs: 
 Outputs: 
 --> index: 0
     value: 100
     publicKey: (149, 4274439633069851851)
 --------------------------------------------------------------------------------
  Transaction:  fc11f91eca510d398fcf08c6d627dcc5b5ac5ec8d4afe49369a5591a571663cd
 --------------------------------------------------------------------------------
 Inputs: 
 Outputs: 
 --> index: 0
     value: 100
     publicKey: (269, 3983947648000273133)
 --------------------------------------------------------------------------------
  Transaction:  edda03bac521749fd68c4e5a43cccb861e33b0ef05707c280d9d83dc0b809e04
 --------------------------------------------------------------------------------
 Inputs: 
 Outputs: 
 --> index: 0
     value: 100
     publicKey: (83, 1934405103424916263)
------------------------------------------------------------------------------------
| Block #1: hash: 0000004ac043d71c1904d35611f5ada5d97f33147eacbb327a5ed5de66dbc856 |
------------------------------------------------------------------------------------
 # Index: 1
 # Previous hash: 000000859b1bfac5d6ecafdea66bf717ca69a22825f3b15fde85c1fe2c524395
 # Transactions: 
 --------------------------------------------------------------------------------
  Transaction:  f17284a76375f77b9ead8e35baa94d9374c46f00daf12b29be43c45b315bf029
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: c817a49c6511eed70c4437712b194cce78d92c147f793272b5555b3bc046b9e4
     outIndex: 0
     signature: 4097917425272685048
 Outputs: 
 --> index: 0
     value: 10
     publicKey: (269, 3983947648000273133)
 --> index: 1
     value: 90
     publicKey: (149, 4274439633069851851)
 --------------------------------------------------------------------------------
  Transaction:  5fec5d4e2b54cc461ff30b3320e125d3d1ef7e859201cd2b7f55aac2052638c0
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: fc11f91eca510d398fcf08c6d627dcc5b5ac5ec8d4afe49369a5591a571663cd
     outIndex: 0
     signature: 3546625313968773340
 Outputs: 
 --> index: 0
     value: 50
     publicKey: (83, 1934405103424916263)
 --> index: 1
     value: 50
     publicKey: (269, 3983947648000273133)
 --------------------------------------------------------------------------------
  Transaction:  b0cc7db44dd0aac9911c12255bf2025198cc0ea79728353f8c00dbf45c062e10
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: edda03bac521749fd68c4e5a43cccb861e33b0ef05707c280d9d83dc0b809e04
     outIndex: 0
     signature: 1362514560436643992
 Outputs: 
 --> index: 0
     value: 5
     publicKey: (269, 3983947648000273133)
 --> index: 1
     value: 95
     publicKey: (83, 1934405103424916263)
------------------------------------------------------------------------------------
| Block #2: hash: 000000c3aa7ca4f40c019ef4d7f43943c4e27768e1eb33cb8630e1de73d2c5a6 |
------------------------------------------------------------------------------------
 # Index: 2
 # Previous hash: 0000004ac043d71c1904d35611f5ada5d97f33147eacbb327a5ed5de66dbc856
 # Transactions: 
 --------------------------------------------------------------------------------
  Transaction:  e99f9f2242228fe4fabf508e7ed5b1b3911ccdd54c7b2e18139adee56f499fb5
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: f17284a76375f77b9ead8e35baa94d9374c46f00daf12b29be43c45b315bf029
     outIndex: 1
     signature: 4097917425272685048
 Outputs: 
 --> index: 0
     value: 10
     publicKey: (269, 3983947648000273133)
 --> index: 1
     value: 80
     publicKey: (149, 4274439633069851851)
 --------------------------------------------------------------------------------
  Transaction:  9008ecec6fe325bd476a8799601ca76832d586383fc2e524a3594b3c5793b6a2
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: f17284a76375f77b9ead8e35baa94d9374c46f00daf12b29be43c45b315bf029
     outIndex: 0
     signature: 3546625313968773340
 --> preTxHash: 5fec5d4e2b54cc461ff30b3320e125d3d1ef7e859201cd2b7f55aac2052638c0
     outIndex: 1
     signature: 3546625313968773340
 Outputs: 
 --> index: 0
     value: 15
     publicKey: (83, 1934405103424916263)
 --> index: 1
     value: 45
     publicKey: (269, 3983947648000273133)
 --------------------------------------------------------------------------------
  Transaction:  2f26e1604b2d5d15245f00c5a9dfeb8a3e643719a10f63a6522968b75dabe78d
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: 5fec5d4e2b54cc461ff30b3320e125d3d1ef7e859201cd2b7f55aac2052638c0
     outIndex: 0
     signature: 1362514560436643992
 Outputs: 
 --> index: 0
     value: 15
     publicKey: (149, 4274439633069851851)
 --> index: 1
     value: 35
     publicKey: (83, 1934405103424916263)
------------------------------------------------------------------------------------
| Block #3: hash: 0000008e8cba158b3c07ccbaba439444f4f5bddbaa77d8920181d81038af4af3 |
------------------------------------------------------------------------------------
 # Index: 3
 # Previous hash: 000000c3aa7ca4f40c019ef4d7f43943c4e27768e1eb33cb8630e1de73d2c5a6
 # Transactions: 
 --------------------------------------------------------------------------------
  Transaction:  16224931eed42c924bc1796548053a7ba1ffd7b8214f0ea83329137b6909b7fb
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: e99f9f2242228fe4fabf508e7ed5b1b3911ccdd54c7b2e18139adee56f499fb5
     outIndex: 1
     signature: 4097917425272685048
 Outputs: 
 --> index: 0
     value: 10
     publicKey: (269, 3983947648000273133)
 --> index: 1
     value: 70
     publicKey: (149, 4274439633069851851)
 --------------------------------------------------------------------------------
  Transaction:  522da669688fd491d774834b5eaebad5e3ac137c28170d213bb49fd0484a555f
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: b0cc7db44dd0aac9911c12255bf2025198cc0ea79728353f8c00dbf45c062e10
     outIndex: 0
     signature: 3546625313968773340
 --> preTxHash: e99f9f2242228fe4fabf508e7ed5b1b3911ccdd54c7b2e18139adee56f499fb5
     outIndex: 0
     signature: 3546625313968773340
 --> preTxHash: 9008ecec6fe325bd476a8799601ca76832d586383fc2e524a3594b3c5793b6a2
     outIndex: 1
     signature: 3546625313968773340
 Outputs: 
 --> index: 0
     value: 30
     publicKey: (83, 1934405103424916263)
 --> index: 1
     value: 30
     publicKey: (269, 3983947648000273133)
 --------------------------------------------------------------------------------
  Transaction:  dc3947d9ba8d25e4309c0e341097072b2b7bd33d82bb6f28e7e2598573d3664c
 --------------------------------------------------------------------------------
 Inputs: 
 --> preTxHash: b0cc7db44dd0aac9911c12255bf2025198cc0ea79728353f8c00dbf45c062e10
     outIndex: 1
     signature: 1362514560436643992
 Outputs: 
 --> index: 0
     value: 70
     publicKey: (269, 3983947648000273133)
 --> index: 1
     value: 25
     publicKey: (83, 1934405103424916263)

alice wallet contains 85 coin!
halim wallet contains 110 coin!
maryam wallet contains 105 coin!
```