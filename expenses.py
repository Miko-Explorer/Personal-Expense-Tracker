import streamlit as st
import pandas as pd
from database import run_query

def show_expenses():
    st.header("Expense Management")

    df_users = run_query("SELECT id, username FROM users")
    if df_users is None or df_users.empty:
        st.warning("Please create a user first in the User Management page.")
        return

    user_options = {row['username']: row['id'] for _, row in df_users.iterrows()}
    selected_user_name = st.selectbox("Filter by User", options=["All"] + list(user_options.keys()))
    user_id_filter = None if selected_user_name == "All" else user_options[selected_user_name]

    if user_id_filter:
        query = """
            SELECT e.*, u.username
            FROM expenses e
            JOIN users u ON e.user_id = u.id
            WHERE user_id = %s
            ORDER BY e.id DESC
        """
        df_exp = run_query(query, (user_id_filter,))
    else:
        query = """
            SELECT e.*, u.username
            FROM expenses e
            JOIN users u ON e.user_id = u.id
            ORDER BY e.id DESC
        """
        df_exp = run_query(query)

    if df_exp is not None and not df_exp.empty:
        st.dataframe(df_exp, use_container_width=True, hide_index=True)
    else:
        st.info("No expenses found for this user. Add a new expense below.")

    # ---- Add new expense ----
    with st.expander("Add New Expense", expanded=False):
        with st.form("add_expense_form", clear_on_submit=True):
            user = st.selectbox("User", options=list(user_options.keys()))
            amount = st.number_input("Amount Spent (Required)", min_value=0.0, max_value=50000.0, step=0.01)
            category = st.selectbox("Category", options=[
                "Food", "Transport", "Utilities", "Subscription",
                "Health", "Work", "School", "Entertainment", "Insurance", "Miscellaneous"
            ])
            description = st.text_area("Description (optional)", placeholder="Optional")
            date = st.date_input("Date")
            payment_method = st.selectbox("Payment Method", options=["Debit", "Credit", "Cash", "Online Payment"])
            location = st.text_input("Location (optional)", placeholder="Optional")

            submitted = st.form_submit_button("Add Expense")
            if submitted:
                if not user or amount <= 0:
                    st.warning("Please select a user and enter a valid amount.")
                else:
                    user_id = user_options[user]
                    query = """
                        INSERT INTO expenses (user_id, amount_spent, category, description, dates, payment_method, location)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    rows = run_query(query, (user_id, amount, category, description, date, payment_method, location), fetch=False)
                    if rows is not None:
                        st.success("Expense added successfully!")
                        st.rerun()

    # ---- Edit / Delete ----
    if df_exp is not None and not df_exp.empty:
        st.subheader("Edit or Delete Expense")
        expense_options = {f"{row['id']} - {row['description'][:30] if row['description'] else 'No description'}": row['id'] for _, row in df_exp.iterrows()}
        selected_exp_label = st.selectbox("Select an expense to edit/delete", options=list(expense_options.keys()))
        expense_id = expense_options[selected_exp_label]
        current = df_exp[df_exp['id'] == expense_id].iloc[0]

        # ---- Delete ----
        st.warning("Deletion is permanent. Check the box below to confirm.")
        confirm_delete = st.checkbox("I confirm deletion of this expense")
        if st.button("Delete Selected Expense"):
            if confirm_delete:
                rows = run_query("DELETE FROM expenses WHERE id = %s", (expense_id,), fetch=False)
                if rows is not None:
                    st.success("Expense deleted successfully.")
                    st.rerun()
            else:
                st.error("Please confirm deletion by checking the box.")

        # ---- Edit ----
        with st.expander("Edit Selected Expense", expanded=False):
            with st.form("edit_expense_form"):
                edit_user = st.selectbox("User", options=list(user_options.keys()), index=list(user_options.values()).index(current['user_id']))
                edit_amount = st.number_input("Amount Spent (Required)", min_value=0.0, max_value=50000.0, step=0.01, value=float(current['amount_spent']))
                edit_category = st.selectbox("Category", options=[
                    "Food", "Transport", "Utilities", "Subscription",
                    "Health", "Work", "School", "Entertainment", "Insurance", "Miscellaneous"
                ], index=["Food", "Transport", "Utilities", "Subscription", "Health", "Work", "School", "Entertainment", "Insurance", "Miscellaneous"].index(current['category']))
                edit_description = st.text_area("Description", value=current['description'] or "", placeholder="Optional")
                edit_date = st.date_input("Date", value=current['dates'])
                edit_payment = st.selectbox("Payment Method", options=["Debit", "Credit", "Cash", "Online Payment"], index=["Debit", "Credit", "Cash", "Online Payment"].index(current['payment_method']))
                edit_location = st.text_input("Location", value=current['location'] or "", placeholder="Optional")

                submitted_edit = st.form_submit_button("Update Expense")
                if submitted_edit:
                    user_id_edit = user_options[edit_user]
                    query = """
                        UPDATE expenses
                        SET user_id = %s, amount_spent = %s, category = %s, description = %s,
                            dates = %s, payment_method = %s, location = %s
                        WHERE id = %s
                    """
                    rows = run_query(query, (user_id_edit, edit_amount, edit_category, edit_description,
                                             edit_date, edit_payment, edit_location, expense_id), fetch=False)
                    if rows is not None:
                        st.success("Expense updated successfully.")
                        st.rerun()