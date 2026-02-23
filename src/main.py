import streamlit as st
from logic import process_text_message
from knowledge_graph import create_graph
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide")
st.title("TourAgent AI 🌍")

# Кэшируем граф
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

G = st.session_state.graph
chat_col, graph_col = st.columns([2, 3])

with chat_col:
    st.subheader("💬 Чат с агентом")
    
    # ВАЖНО: chat_input ВСЕГДА снаружи условий
    user_input = st.chat_input("Напишите название (например, Дубай)...")

    # Отображаем историю
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = process_text_message(user_input, G)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

with graph_col:
    st.subheader("📊 Граф знаний")
    fig, ax = plt.subplots()
    nx.draw(G, with_labels=True, node_color='lightblue', ax=ax)
    st.pyplot(fig)