import streamlit as st
import json

FILE = "users.json"

# Load users
def load_users():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save users
def save_users(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

users = load_users()

st.title("🏦 Beginner ATM App")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

# LOGIN
if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        if username in users and users[username]["pin"] == pin:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or PIN")

# DASHBOARD
else:
    user = st.session_state.user
    st.subheader(f"Welcome {user} 👋")
    st.write("Balance:", users[user]["balance"])

    option = st.selectbox("Choose Action", ["Deposit", "Withdraw", "Logout"])

    if option == "Deposit":
        amount = st.number_input("Enter amount", min_value=0)
        if st.button("Deposit"):
            users[user]["balance"] += amount
            save_users(users)
            st.success("Money deposited!")

    if option == "Withdraw":
        amount = st.number_input("Enter amount", min_value=0)
        if st.button("Withdraw"):
            if amount > users[user]["balance"]:
                st.error("Insufficient balance!")
            else:
                users[user]["balance"] -= amount
                save_users(users)
                st.success("Money withdrawn!")

    if option == "Logout":
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""