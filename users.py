# users.py
import streamlit as st
import pandas as pd
from database import run_query

def show_users():
    st.header("User Management")

    df_users = run_query("SELECT * FROM users ORDER BY id")
    if df_users is not None and not df_users.empty:
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    else:
        st.info("No users found. Add a new user below.")

    # ---- Add new user ----
    with st.expander("Add New User", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            username = st.text_input("Username", placeholder="Required field")
            email = st.text_input("Email", placeholder="Required field")
            password = st.text_input("Password", type="password", placeholder="Required field")
            submitted = st.form_submit_button("Add User")
            if submitted:
                if not username or not email or not password:
                    st.warning("All fields are required.")
                else:
                    query = """
                        INSERT INTO users (username, email, passwords)
                        VALUES (%s, %s, %s)
                    """
                    rows = run_query(query, (username, email, password), fetch=False)
                    if rows is not None:
                        st.success(f"User '{username}' added successfully!")
                        st.rerun()

    # ---- Edit / Delete ----
    if df_users is not None and not df_users.empty:
        st.subheader("Edit or Delete User")
        user_options = {row['username']: row['id'] for _, row in df_users.iterrows()}
        selected_user = st.selectbox("Select a user to edit/delete", options=list(user_options.keys()))
        user_id = user_options[selected_user]

        # ---- Delete ----
        st.warning("Deletion is permanent. Check the box below to confirm.")
        confirm_delete = st.checkbox("I confirm deletion of this user")
        if st.button("Delete Selected User"):
            if confirm_delete:
                rows = run_query("DELETE FROM users WHERE id = %s", (user_id,), fetch=False)
                if rows is not None:
                    st.success(f"User '{selected_user}' deleted successfully.")
                    st.rerun()
            else:
                st.error("Please confirm deletion by checking the box.")

        # ---- Edit ----
        with st.expander("Edit Selected User", expanded=False):
            with st.form("edit_user_form"):
                new_username = st.text_input("New Username", value=selected_user, placeholder="Required field")
                new_email = st.text_input("New Email", value=df_users[df_users['id'] == user_id]['email'].iloc[0], placeholder="Required field")
                new_password = st.text_input("New Password (leave blank to keep unchanged)", type="password", placeholder="Optional")
                submitted_edit = st.form_submit_button("Update User")
                if submitted_edit:
                    updates = []
                    params = []
                    if new_username and new_username != selected_user:
                        updates.append("username = %s")
                        params.append(new_username)
                    if new_email:
                        updates.append("email = %s")
                        params.append(new_email)
                    if new_password:
                        updates.append("passwords = %s")
                        params.append(new_password)
                    if updates:
                        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
                        params.append(user_id)
                        rows = run_query(query, tuple(params), fetch=False)
                        if rows is not None:
                            st.success("User updated successfully.")
                            st.rerun()
                    else:
                        st.warning("No changes to update.")