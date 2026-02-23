# src/main.py
import streamlit as st
from logic import process_text_message
from knowledge_graph import create_graph, find_related_entities
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide")
st.title("Tour Knowledge Graph & Chat 🌍🤖")

# --- Инициализация истории чата ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Кэшируем граф в session_state ---
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()
G = st.session_state.graph

# --- Разделяем экран на колонки: чат | граф ---
chat_col, graph_col = st.columns([2, 3])

with chat_col:
    st.subheader("💬 Чат")

    # --- Поле ввода всегда доступно ---
    user_input = st.chat_input("Введите ваш запрос...")

    # --- Кнопки быстрого теста ---
    if st.button("Привет"):
        user_input = "привет"
    elif st.button("Проверить объект"):
        user_input = "проверить объект"

    # --- Обрабатываем новое сообщение ---
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        bot_response = process_text_message(user_input, G)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # --- Отображение истории сообщений ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with graph_col:
    st.subheader("📊 Визуализация графа")

    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)  # фиксируем layout для стабильности
    nx.draw(
        G, pos,
        with_labels=True,
        node_color='lightblue',
        edge_color='gray',
        node_size=2500,
        font_size=10,
        ax=ax
    )
    st.pyplot(fig)