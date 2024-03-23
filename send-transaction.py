# Send a transaction with Polygon
# https://docs.infura.io/tutorials/layer-2-networks/send-a-transaction
# https://docs.infura.io/tutorials/ethereum/send-a-transaction/send-a-transaction-py
import os

from web3 import Web3, exceptions

# Connect to the Polygon network (e.g., Infura)
alchemy_url = "https://polygon-mumbai.g.alchemy.com/v2/" + os.getenv("ALCHEMY_API_KEY")
infura_url = "https://polygon-mumbai.infura.io/v3/" + os.getenv("INFURA_API_KEY")
if os.getenv("API_NETWORK", "alchemy") == "alchemy":
    endpoint_uri = alchemy_url
else:
    endpoint_uri = infura_url
web3 = Web3(Web3.HTTPProvider(endpoint_uri))

# Contract address and ABI
contract_address = os.getenv("CONTRACT_ADDR")
function_name = os.getenv("FUNCTION_NAME")
contract_abi = [
    {
        "constant": False,
        "inputs": [
            {
                "name": "arg0",
                "type": "uint256"
            }
        ],
        "name": function_name,
        "outputs": [],
        "payable": True,  # Set to True to allow sending value with the transaction
        "stateMutability": "payable",
        "type": "function"
    }
]

# Your Polygon account private key
private_key = os.getenv("SIGNER_PRIVATE_KEY")

signer_address = os.getenv("SIGNER_ADDR")
try:
    from_account = web3.to_checksum_address(signer_address)
except exceptions.InvalidAddress as ex:
    print(f"Invalid 'from_account' address: {signer_address}")
    raise ex

try:
    to_account = web3.to_checksum_address(contract_address)
except exceptions.InvalidAddress as ex:
    print(f"Invalid 'to_account' address: {contract_address}")
    raise ex

# Nonce of the sender address
nonce = web3.eth.get_transaction_count(from_account)
print("Nonce:", nonce)

# Create a contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Estimate gas
tx = {
    'chainId': 80001,
    'from': from_account,
    'value': 420000000000,  # Amount in wei
    'gas': 53000,  # Gas limit
    'gasPrice': web3.to_wei('3', 'gwei'),  # Gas price in wei
    'nonce': nonce,  # Nonce of the sender address
}
estimated_gas = web3.eth.estimate_gas(tx)
print("Estimated Gas:", estimated_gas)
tx['gas'] = estimated_gas

# Prepare transaction data
argument = int(os.getenv("FUNC_ARG"))
argument_hex = hex(argument)
tx['data'] = function_name + argument_hex[2:]
tx['to'] = to_account
transaction_data = tx
print("Transaction Data:", transaction_data)

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction_data, private_key)
print("Signed Transaction:", signed_txn)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Transaction Hash:", tx_hash.hex())
