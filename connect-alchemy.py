import os

from web3 import Web3

# Setup
alchemy_url = "https://polygon-mumbai.g.alchemy.com/v2/" + os.getenv("ALCHEMY_API_KEY")
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Print if web3 is successfully connected
print(f"Connected: {w3.is_connected()}")

# Get the latest block number
latest_block = w3.eth.block_number
print(f"Latest block: {latest_block}")

# Get the balance of an account
balance = w3.eth.get_balance(Web3.to_checksum_address(os.getenv("CONTRACT_ADDR")))
print(f"Balance: {balance}")
