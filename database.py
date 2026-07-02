import mysql.connector
import streamlit as st
import pandas as pd

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"].get("port", 3306)
        )
        if conn.is_connected():
            return conn
        else:
            st.error("Database connection is not active. Please check your credentials.")
            return None
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None
    except KeyError:
        st.error("Missing MySQL configuration in secrets.toml. Please set host, user, password, and database.")
        return None

def run_query(query, params=None, fetch=True):
    conn = get_db_connection()
    if conn is None:
        st.warning("Cannot connect to database. Please check your settings and try again.")
        return None if fetch else 0

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            df = pd.DataFrame(result) if result else pd.DataFrame()
            return df
        else:
            conn.commit()
            return cursor.rowcount
    except mysql.connector.Error as e:
        st.error(f"Query error: {e}")
        return None if fetch else 0
    finally:
        if cursor:
            cursor.close()