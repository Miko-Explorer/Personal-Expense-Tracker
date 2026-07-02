import streamlit as st
from database import run_query

def show_reports():
    st.header("Expense Reports")

    views = {
        "high_expense_based_cat": "Highest Amount Spent per Category (by User)",
        "low_expense_based_cat": "Lowest Amount Spent per Category (by User)",
        "high_amount_paid_based_paymethod": "Highest Amount Paid per Payment Method (by User)",
        "low_amount_paid_based_paymethod": "Lowest Amount Paid per Payment Method (by User)",
        "latest_created_expense": "10 Most Recent Expenses (created_at)",
        "outdated_created_expense": "30 Oldest Expenses (created_at)",
        "recently_updated_expense": "Most Recently Updated Expenses",
        "not_updated_expense": "Expenses Never Updated (oldest first)",
        "total_amount_spent": "Total Amount Spent (by User)",
        "average_amount_spent_based_cat": "Average Amount Spent per Category (by User)",
        "average_amount_spent_based_paymethod": "Average Amount Paid per Payment Method (by User)",
        "total_amount_paid_based_paymethod": "Total Amount Paid per Payment Method (by User)",
        "total_amount_spent_based_cat": "Total Amount Spent per Category (by User)",
        "total_entries": "Total Number of Expense Entries"
    }

    views_with_user_id = {
        "high_expense_based_cat",
        "low_expense_based_cat",
        "high_amount_paid_based_paymethod",
        "low_amount_paid_based_paymethod",
        "total_amount_spent",
        "average_amount_spent_based_cat",
        "average_amount_spent_based_paymethod",
        "total_amount_paid_based_paymethod",
        "total_amount_spent_based_cat",
    }

    # Group views into tabs
    view_names = list(views.keys())
    tab_groups = [view_names[i:i + 4] for i in range(0, len(view_names), 4)]
    tabs = st.tabs([f"Reports {i + 1}" for i in range(len(tab_groups))])

    for tab, group in zip(tabs, tab_groups):
        with tab:
            for view_name in group:
                st.subheader(views[view_name])

                # Build query: if view has user_id, join with users to get username
                if view_name in views_with_user_id:
                    # Get column names from the view to avoid ambiguous columns
                    # We'll select all columns from the view and add username
                    query = f"""
                        SELECT v.*, u.username
                        FROM {view_name} v
                        LEFT JOIN users u ON v.user_id = u.id
                        ORDER BY v.user_id
                    """
                else:
                    query = f"SELECT * FROM {view_name}"

                df = run_query(query)
                if df is not None and not df.empty:
                    # If the view had user_id and we joined, we might want to reorder columns
                    # to show username first. We'll just display as is.
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No data available for this report.")
                st.divider()