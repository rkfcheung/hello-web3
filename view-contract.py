import os

from web3 import Web3
from web3.middleware import geth_poa_middleware

# Connect to the Polygon Mumbai Testnet using Infura
infura_url = "https://polygon-mumbai.infura.io/v3/" + os.getenv("INFURA_PROJECT_ID")

# Connect to the Polygon network
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Inject middleware for POA chain

# Check connection status
if web3.is_connected():
    print("Connected to Polygon network")
else:
    print("Failed to connect to Polygon network")

# Address of the contract
contract_address = os.getenv("CONTRACT_ADDR")

# Function signature of the method you want to call
function_signature = os.getenv("CONTRACT_NAME")

# Parameters for the method (if any)
# For example, if the method takes a uint256 parameter, you would encode the value accordingly
# For simplicity, let's assume the method takes no parameters
parameters = "000000000000000000000000"

# Craft the data for the RPC call
data = function_signature + parameters

# Make the RPC call
result = web3.eth.call({
    "to": contract_address,
    "data": data,
})
print(f"Contract content: {result}")
