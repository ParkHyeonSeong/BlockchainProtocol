# BlockchainProtocol
### New Encrypt Protocol 0.1v
##### 1. PROCESS
0) Participants : S(Server), C(Client)
1) S Makes Nonce(s)
2) C Makes Nonce(c)
3) Exchange Nonce()
4) Calculation Nonce() to create blocknonce
5) Create GenesisBlock(Seperately)
6) S Send Message C (Prev_Hash||Msg)
7) C Check Prev_Hash
8) Create Blockchain(Seperately)
9) C Send Message S (Prev_Hash||Msg)
10) S Check Prev_Hash
11) Create Blockchain(Seperately)
12) Repeat 6 to 12

##### 2. Technical Report
- Check Authentication
- None Encrypt(Will be patched)
- Weak to man-in-the-middle attack(Will be patched)

##### 3. Help(CMD, Terminal)
1) ```python server.py```
2) ```python client.py```
3) Server : ```send msg```
4) Server : ```Anything Else...```
5) Client : ```Anything Else...```
