import streamlit as st
from pathlib import Path
import sqlite3
from small_talk import talk
from sql import sql_chain
from faq import faq_chain, load_faq_data
from router import router

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
# Adjust path relative to main.py
DB_PATH = Path(__file__).parent / 'database.db'

# Check if database exists
if not DB_PATH.exists():
    st.error("Database not found! Make sure 'database.db' is in the app folder.")
    st.stop()  # stop app if no DB

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# If sql_chain uses connection, pass it:
sql_chain.set_connection(conn)  # <-- you need to adjust sql_chain.py to accept this

# -----------------------------
# FAQ DATA
# -----------------------------
faqs_path = Path(__file__).parent / 'resources/faq_data.csv'
load_faq_data(faqs_path)

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def ask(query):
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)  # now sql_chain can use the connection
    elif route == 'small_talk':
        return talk(query)
    else:
        return f'Route {route} not implemented yet'

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title('E-commerce Chatbot')

query = st.chat_input('Write your query')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message('user'):
        st.markdown(query)
    st.session_state.messages.append({'role': 'user', 'content': query})

    response = ask(query)

    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
