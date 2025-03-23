import streamlit as st
import requests
import json


# API Endpoint
PROFILE_URL = "http://127.0.0.1:8000/profile"
UPDATE_PROFILE_URL = "http://127.0.0.1:8000/users/update"
UPDATE_PASSWORD_URL = "http://127.0.0.1:8000/users/update-password"
DELETE_ACCOUNT_URL = "http://127.0.0.1:8000/users/delete"

def profile():
    st.title("👤 User Profile")
    st.write("Manage your account settings below.")

    # Get token from session
    token = st.session_state.get("token")
    if not token:
        st.error("⚠️ Please log in first!")
        return

    # Fetch user profile from API
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(PROFILE_URL, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        st.subheader("📌 User Details")
        st.write(f"**Username:** {user_data['username']}")
        st.write(f"**Email:** {user_data['email']}")
       
    else:
        st.error("❌ Failed to fetch profile details")
        st.write("🔍 Debug Response:", response.status_code, response.text)


    action = st.radio("Select an action:", ["Update Profile", "Update Password", "Delete Account"], index=None)

    
    if action == "Update Profile":
        update_profile()
    elif action == "Update Password":
        update_password()
    elif action == "Delete Account":
        delete_account()
        # 🔹 Add Logout Button
    if st.button("➡️ Logout"):
        st.session_state.token = None
        st.session_state.page = "Login"
        st.rerun()
 
def update_profile():
    st.subheader("🔄 Update Profile")

    # Get current profile details
    token = st.session_state.get("token")
    if not token:
        st.error("⚠️ Please log in first!")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(PROFILE_URL, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        username = st.text_input("New Username", value=user_data.get("username", ""))
        email = st.text_input("New Email", value=user_data.get("email", ""))
    else:
        st.error("❌ Failed to fetch current profile details")
        st.write("🔍 Debug Response:", response.status_code, response.text)
        return  # Stop execution if fetching fails

    if st.button("Save Changes"):
        data = {"username": username, "email": email}
        update_response = requests.put(UPDATE_PROFILE_URL, headers=headers, json=data)

        if update_response.status_code == 200:
            st.success("✅ Profile updated successfully!")

            # 🔹 Clear session & force re-login
            st.session_state.token = None
            st.session_state.page = "Login"
            st.warning("🔄 Please log in again to apply changes.")
            st.rerun()  # Redirect user to login page

        else:
            st.error("❌ Failed to update profile")
            st.write("🔍 Debug Response:", update_response.status_code, update_response.text)
        
def update_password():
    st.subheader("🔒 Update Password")
    old_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    
    if st.button("Change Password"):
        token = st.session_state.get("token")
        if not token:
            st.error("⚠️ Please log in first!")
            return
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"old_password": old_password, "new_password": new_password}
        response = requests.put(UPDATE_PASSWORD_URL, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            st.success("✅ Password updated successfully!")
        else:
            st.error("❌ Failed to update password")
            st.write("Debug Response:", response.status_code, response.text)


def delete_account():
    st.subheader("⚠️ Delete Account")
    st.warning("Once deleted, you will need to register again to access the system.")
    password = st.text_input("Enter your password to confirm", type="password")
    
    if st.button("Delete My Account", help="This action cannot be undone!"):
        token = st.session_state.get("token")
        if not token:
            st.error("⚠️ Please log in first!")
            return
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"password": password}
        response = requests.delete(DELETE_ACCOUNT_URL, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            st.success("✅ Account deleted successfully!")
            st.session_state.clear()
            st.warning("You have been logged out.")
        else:
            st.error("❌ Failed to delete account")
            st.write("Debug Response:", response.status_code, response.text)
        st.session_state.token = None
        st.session_state.page = "Login"
        st.rerun()