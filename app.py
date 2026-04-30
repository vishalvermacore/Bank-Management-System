import streamlit as st
from main import Bank

bank = Bank()

st.set_page_config(page_title="Bank System", page_icon="🏦", layout="centered")

st.title("🏦 Bank Management System")
st.markdown("Secure • Simple • Fast")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Check Details",
        "Update Account",
        "Delete Account"
    ]
)

# ---------------- CREATE ----------------
if menu == "Create Account":
    st.subheader("🆕 Create Account")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create Account"):
        if age < 18:
            st.error("Must be 18+")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be 4 digits")
        else:
            acc = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "account_number": bank._Bank__generate_account_number(),
                "balance": 0
            }

            Bank.data.append(acc)
            Bank._Bank__update()

            st.success("Account Created Successfully!")
            st.info(f"Account Number: {acc['account_number']}")

# ---------------- DEPOSIT ----------------
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Deposit"):
        account = Bank._Bank__find_account(acc, int(pin)) if pin else None

        if not account:
            st.error("Invalid credentials")
        elif amt <= 0 or amt > 10000:
            st.error("Invalid amount")
        else:
            account['balance'] += amt
            Bank._Bank__update()
            st.success(f"Balance: ₹{account['balance']}")

# ---------------- WITHDRAW ----------------
elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", min_value=0.0)

    if st.button("Withdraw"):
        account = Bank._Bank__find_account(acc, int(pin)) if pin else None

        if not account:
            st.error("Invalid credentials")
        elif amt > account['balance']:
            st.error("Insufficient funds")
        else:
            account['balance'] -= amt
            Bank._Bank__update()
            st.success(f"Balance: ₹{account['balance']}")

# ---------------- CHECK ----------------
elif menu == "Check Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Check"):
        account = Bank._Bank__find_account(acc, int(pin)) if pin else None

        if not account:
            st.error("Invalid credentials")
        else:
            st.json(account)

# ---------------- UPDATE ----------------
elif menu == "Update Account":
    st.subheader("✏️ Update Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    account = Bank._Bank__find_account(acc, int(pin)) if pin else None

    if account:
        option = st.selectbox("What to update?", ["Name", "Email", "PIN"])

        if option == "Name":
            new = st.text_input("New Name")
            if st.button("Update"):
                if new.strip():
                    account['name'] = new
                    Bank._Bank__update()
                    st.success("Name updated")

        elif option == "Email":
            new = st.text_input("New Email")
            if st.button("Update"):
                if new.strip():
                    account['email'] = new
                    Bank._Bank__update()
                    st.success("Email updated")

        elif option == "PIN":
            new = st.text_input("New PIN", type="password")
            if st.button("Update"):
                if len(new) == 4 and new.isdigit():
                    account['pin'] = int(new)
                    Bank._Bank__update()
                    st.success("PIN updated")
                else:
                    st.error("Invalid PIN")

    elif st.button("Load Account"):
        st.error("Invalid credentials")

# ---------------- DELETE ----------------
elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        account = Bank._Bank__find_account(acc, int(pin)) if pin else None

        if not account:
            st.error("Invalid credentials")
        else:
            Bank.data.remove(account)
            Bank._Bank__update()
            st.success("Account deleted successfully")