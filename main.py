# main.py
import streamlit as st
from users import show_users
from expenses import show_expenses
from reports import show_reports

st.set_page_config(
    page_title="Personal Expense Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #0e1117, #1a1c2e, #12141c, #1e2230);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar background – change the color below */
    section[data-testid="stSidebar"] {
        background: #1E1E24 !important;    /* <-- CHANGE THIS COLOR */
        backdrop-filter: blur(14px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Glass morphism containers */
    .glass {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Logo */
    .logo-container {
        text-align: center;
        padding: 10px 0 20px 0;
    }
    .logo-icon {
        font-size: 48px;
        font-weight: 700;
        color: #ffffff;
        background: rgba(255, 255, 255, 0.06);
        width: 80px;
        height: 80px;
        line-height: 80px;
        border-radius: 50%;
        display: inline-block;
        border: 2px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 0 30px rgba(74, 140, 255, 0.2);
        margin-bottom: 10px;
    }
    .logo-text {
        font-size: 22px;
        font-weight: 600;
        color: #e0e4eb;
        letter-spacing: 2px;
    }
    .logo-sub {
        font-size: 13px;
        color: #8892a8;
        margin-top: -5px;
    }

    /* Navigation */
    .stRadio > div {
        background: transparent !important;
    }
    .stRadio label {
        color: #c0c6d4 !important;
        font-weight: 400;
        padding: 8px 12px;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stRadio label:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    .stRadio [data-baseweb="radio"] {
        accent-color: #4a8cff;
    }

    /* Other UI elements */
    .stButton > button {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #f0f2f6;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: #4a8cff;
        color: white;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #f0f2f6;
        border-radius: 8px;
    }
    .stDataFrame {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stSuccess, .stInfo, .stWarning, .stError {
        backdrop-filter: blur(4px);
        background: rgba(0,0,0,0.3);
    }
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
with st.sidebar:
    # Optional: extra style inside sidebar for extra reliability
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                background: #1a1a2e !important;
                backdrop-filter: blur(14px) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">$</div>
            <div class="logo-text">PET</div>
            <div class="logo-sub">Personal Expense Tracker</div>
        </div>
        <hr>
    """, unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["Users", "Expenses", "Reports"],
        index=0,
        label_visibility="collapsed"
    )
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.caption("Data Analyst Portfolio Project")

# ---- Routing ----
if page == "Users":
    show_users()
elif page == "Expenses":
    show_expenses()
elif page == "Reports":
    show_reports()