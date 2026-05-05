# =================================================================
# PIGLINK CONFIGURATION FILE
# This file stores the "brain" of the application settings.
# 1. CONTRACT_ADDRESS: The unique ID of our program on the blockchain.
# 2. CONTRACT_ABI: The list of rules and functions the app can talk to.
# 3. RPC_URL: The bridge that connects this app to the Ethereum network.
# 4. UI_TEXT: Friendly names and descriptions for non-technical users.
# =================================================================

# The official address of the PigLink contract on the Sepolia Testnet
CONTRACT_ADDRESS = "0xc0324b2cf64501b8d5cc69B781549EE40F5228da"

# The Public Node used to read data from the blockchain
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

# Application Identity
APP_NAME = "PigLink"
TAGLINE = "Connecting Farmers & Retailers for a Greener Future"
DESCRIPTION = "A transparent blockchain platform for redistributing surplus food to local pig farmers."

# Human-readable labels for technical status codes (Enums)
ORDER_STATUS = {
    0: "Listed",
    1: "Ordered",
    2: "Paid",
    3: "In Transit",
    4: "Delivered",
    5: "Refunded"
}

# The Application Binary Interface (ABI) derived from the Solidity code
# This tells Python how to interact with the smart contract functions
CONTRACT_ABI = [
	{"inputs": [], "stateMutability": "view", "type": "constructor"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "address", "name": "farmer", "type": "address"}], "name": "DeliveryConfirmed", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "address", "name": "logistics", "type": "address"}], "name": "DeliveryStarted", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "productId", "type": "uint256"}, {"indexed": False, "internalType": "address", "name": "farmer", "type": "address"}], "name": "OrderPlaced", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}, {"indexed": False, "internalType": "address", "name": "farmer", "type": "address"}], "name": "PaymentMade", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "productId", "type": "uint256"}, {"indexed": False, "internalType": "address", "name": "retailer", "type": "address"}, {"indexed": False, "internalType": "string", "name": "description", "type": "string"}, {"indexed": False, "internalType": "uint256", "name": "price", "type": "uint256"}], "name": "ProductListed", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "orderId", "type": "uint256"}, {"indexed": False, "internalType": "address", "name": "farmer", "type": "address"}], "name": "RefundIssued", "type": "event"},
	{"anonymous": False, "inputs": [{"indexed": False, "internalType": "address", "name": "user", "type": "address"}, {"indexed": False, "internalType": "string", "name": "role", "type": "string"}], "name": "UserRegistered", "type": "event"},
	{"inputs": [], "name": "admin", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "_orderId", "type": "uint256"}], "name": "confirmDelivery", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "_orderId", "type": "uint256"}], "name": "issueRefund", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "string", "name": "_description", "type": "string"}, {"internalType": "uint256", "name": "_price", "type": "uint256"}], "name": "listProduct", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "_orderId", "type": "uint256"}], "name": "makePayment", "outputs": [], "stateMutability": "payable", "type": "function"},
	{"inputs": [], "name": "nextOrderId", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
	{"inputs": [], "name": "nextProductId", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "orders", "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "uint256", "name": "productId", "type": "uint256"}, {"internalType": "address", "name": "farmer", "type": "address"}, {"internalType": "address", "name": "retailer", "type": "address"}, {"internalType": "address", "name": "logistics", "type": "address"}, {"internalType": "uint256", "name": "price", "type": "uint256"}, {"internalType": "enum PigLink.OrderStatus", "name": "status", "type": "uint8"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "_productId", "type": "uint256"}], "name": "placeOrder", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "products", "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}, {"internalType": "string", "name": "description", "type": "string"}, {"internalType": "uint256", "name": "price", "type": "uint256"}, {"internalType": "address", "name": "retailer", "type": "address"}, {"internalType": "bool", "name": "available", "type": "bool"}], "stateMutability": "view", "type": "function"},
	{"inputs": [{"internalType": "address", "name": "_user", "type": "address"}, {"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "bool", "name": "_isFarmer", "type": "bool"}, {"internalType": "bool", "name": "_isRetailer", "type": "bool"}, {"internalType": "bool", "name": "_isLogistics", "type": "bool"}, {"internalType": "bool", "name": "_isRegulator", "type": "bool"}], "name": "registerUser", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "uint256", "name": "_orderId", "type": "uint256"}], "name": "startDelivery", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
	{"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "users", "outputs": [{"internalType": "string", "name": "name", "type": "string"}, {"internalType": "bool", "name": "isFarmer", "type": "bool"}, {"internalType": "bool", "name": "isRetailer", "type": "bool"}, {"internalType": "bool", "name": "isLogistics", "type": "bool"}, {"internalType": "bool", "name": "isRegulator", "type": "bool"}, {"internalType": "bool", "name": "verified", "type": "bool"}], "stateMutability": "view", "type": "function"}
]