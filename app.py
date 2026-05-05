# pip install streamlit web3 streamlit-js-eval
import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os

# ---------------- WEB3 SETUP ----------------
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# ---------------- SAFE LAYER ----------------
def clean_address(addr):
    if not addr:
        return None
    return Web3.to_checksum_address(addr.strip())

def safe_nonce(addr):
    return w3.eth.get_transaction_count(clean_address(addr))

def safe_tx_params(user_address):
    addr = clean_address(user_address)
    return {
        "from": addr,
        "nonce": safe_nonce(addr),
        "gas": 300000
    }

# ---------------- THEME (LIGHT UI) ----------------
st.markdown("""
<style>

.stApp {
    background-color: #FFFFFF;
    color: #1B1B1B;
}

section[data-testid="stSidebar"] {
    background-color: #F5F7F5;
    border-right: 2px solid #2E7D32;
}

h1, h2, h3 {
    color: #1B5E20;
}

.stButton > button {
    background-color: #2E7D32;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1B5E20;
}

input, textarea {
    background-color: #FFFFFF !important;
    color: #1B1B1B !important;
    border: 1.5px solid #A5D6A7 !important;
    border-radius: 8px !important;
}

[data-testid="stMetric"] {
    background-color: #F1F8F1;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #C8E6C9;
}

.streamlit-expanderHeader {
    background-color: #F1F8F1;
    border: 1px solid #C8E6C9;
    border-radius: 8px;
}

.stSuccess {
    background-color: #E8F5E9;
    border-left: 5px solid #2E7D32;
}
.stError {
    background-color: #FFEBEE;
    border-left: 5px solid #C62828;
}

.stInfo {
    background-color: #F1F8F1;
    border-left: 5px solid #2E7D32;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
def render_header():
    LOGO_PATH = "logo.png"

    try:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=200)

        st.title(config.APP_NAME)

    except Exception:
        st.title(config.APP_NAME)

    st.caption(config.TAGLINE)
    st.write(config.DESCRIPTION)

# ---------------- TRANSACTION HELPER ----------------
def send_tx(tx_data, user_address):
    js_code = f"""
    window.ethereum.request({{
        method: 'eth_sendTransaction',
        params: [{{
            from: '{clean_address(user_address)}',
            to: '{config.CONTRACT_ADDRESS}',
            data: '{tx_data["data"] if isinstance(tx_data, dict) and "data" in tx_data else tx_data}',
            value: '0x0'
        }}],
    }}).then(txHash => {{
        window.alert('Transaction Sent: ' + txHash);
    }}).catch(err => {{
        window.alert('Error: ' + err.message);
    }});
    """
    streamlit_js_eval(js_expressions=js_code, key="tx_send")

# ---------------- OVERVIEW ----------------
def page_overview():
    st.header("Network Dashboard")

    try:
        total_products = contract.functions.nextProductId().call()
        total_orders = contract.functions.nextOrderId().call()
        admin_addr = clean_address(contract.functions.admin().call())

        col1, col2 = st.columns(2)
        col1.metric("Available Listings", total_products)
        col2.metric("Total Orders", total_orders)

        st.info(f"Admin: {admin_addr}")
        st.success("Connected to Sepolia Testnet")

    except Exception as e:
        st.error(f"Dashboard error: {str(e)}")

# ---------------- RETAILER ----------------
def page_retailer(user_address):
    st.header("Retailer Portal")

    with st.expander("List New Food"):
        with st.form("list_food"):
            desc = st.text_input("Food Description")
            price_eth = st.number_input("Price (ETH)", min_value=0.0, format="%.4f")

            submitted = st.form_submit_button("List Product")

            if submitted:
                try:
                    user_address = clean_address(user_address)
                    price_wei = w3.to_wei(price_eth, "ether")

                    tx = contract.functions.listProduct(
                        desc,
                        price_wei
                    ).build_transaction(safe_tx_params(user_address))

                    send_tx(tx, user_address)

                except Exception as e:
                    st.error(str(e))

# ---------------- FARMER ----------------
def page_farmer(user_address):
    st.header("Farmer Marketplace")

    tab1, tab2 = st.tabs(["Browse Food", "My Orders"])

    with tab1:
        product_id = st.number_input("Product ID", min_value=0, step=1)

        if st.button("Place Order"):
            try:
                tx = contract.functions.placeOrder(product_id).build_transaction(
                    safe_tx_params(user_address)
                )
                send_tx(tx, user_address)

            except Exception as e:
                st.error(str(e))

    with tab2:
        order_id = st.number_input("Order ID", min_value=0, step=1)

        col1, col2 = st.columns(2)

        if col1.button("Make Payment"):
            try:
                order = contract.functions.orders(order_id).call()

                tx = contract.functions.makePayment(order_id).build_transaction({
                    **safe_tx_params(user_address),
                    "value": order[5]
                })

                send_tx(tx, user_address)

            except Exception as e:
                st.error(str(e))

        if col2.button("Confirm Delivery"):
            try:
                tx = contract.functions.confirmDelivery(order_id).build_transaction(
                    safe_tx_params(user_address)
                )
                send_tx(tx, user_address)

            except Exception as e:
                st.error(str(e))

# ---------------- WALLET ----------------
def wallet_manager():
    st.sidebar.markdown("---")
    st.sidebar.subheader("Wallet Connection")

    if "wallet_address" not in st.session_state:
        st.session_state.wallet_address = None

    wallet = streamlit_js_eval(
        js_expressions="window.localStorage.getItem('piglink_wallet')",
        key="read_wallet"
    )

    if wallet:
        st.session_state.wallet_address = clean_address(wallet)

    if st.sidebar.button("Connect MetaMask"):
        streamlit_js_eval(
            js_expressions="""
            window.ethereum.request({ method: "eth_requestAccounts" })
            .then(accounts => {
                window.localStorage.setItem("piglink_wallet", accounts[0]);
            });
            """,
            key="connect_wallet"
        )

    if not st.session_state.wallet_address:
        st.sidebar.warning("Connect your wallet")
        return None

    st.sidebar.success(
        f"Wallet Connected ✅ {st.session_state.wallet_address[:6]}...{st.session_state.wallet_address[-4:]}"
    )

    return st.session_state.wallet_address

# ---------------- LOGISTICS ----------------
def page_logistics_admin(user_address):
    st.header("Logistics & Admin")

    ship_id = st.number_input("Order ID", min_value=0, step=1)

    if st.button("Mark In Transit"):
        try:
            tx = contract.functions.startDelivery(ship_id).build_transaction(
                safe_tx_params(user_address)
            )
            send_tx(tx, user_address)

        except Exception as e:
            st.error(str(e))

    st.markdown("---")

    with st.expander("Register User"):
        with st.form("reg_user"):
            addr = st.text_input("Wallet Address")
            name = st.text_input("Name")
            role = st.selectbox("Role", ["Farmer", "Retailer", "Logistics", "Regulator"])

            submitted = st.form_submit_button("Register")

            if submitted:
                try:
                    addr = clean_address(addr)

                    tx = contract.functions.registerUser(
                        addr,
                        name,
                        role == "Farmer",
                        role == "Retailer",
                        role == "Logistics",
                        role == "Regulator"
                    ).build_transaction(safe_tx_params(user_address))

                    send_tx(tx, user_address)

                except Exception as e:
                    st.error(str(e))

# ---------------- MAIN ----------------
def main():
    st.set_page_config(page_title=config.APP_NAME, layout="wide")

    render_header()

    user_address = wallet_manager()
    if not user_address:
        st.stop()

    menu = ["Overview", "Retailer Portal", "Farmer Marketplace", "Logistics & Admin"]
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Overview":
        page_overview()
    elif choice == "Retailer Portal":
        page_retailer(user_address)
    elif choice == "Farmer Marketplace":
        page_farmer(user_address)
    elif choice == "Logistics & Admin":
        page_logistics_admin(user_address)

if __name__ == "__main__":
    main()