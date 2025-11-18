import streamlit as st
from pathlib import Path
import sqlite3
from small_talk import talk
from sql import sql_chain, set_connection
from faq import faq_chain, load_faq_data
from router import router

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
DB_PATH = Path(__file__).parent / 'db.sqlite'  # matches your current DB filename

if not DB_PATH.exists():
    st.error("Database not found! Make sure 'db.sqlite' is in the app folder.")
    st.stop()  # stop app if DB missing

conn = sqlite3.connect(DB_PATH)
set_connection(conn)  # pass connection to sql_chain

# -----------------------------
# LOAD FAQ DATA
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
        return sql_chain(query)  # uses the connection we set
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
