import streamlit as st
from logic import process_text_message
from knowledge_graph import create_graph
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide")
st.title("Tour Knowledge Graph & Chat 🌍🤖")

# --- Инициализация истории чата ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Инициализация графа (кэшируем) ---
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()

G = st.session_state.graph

# --- Разделяем экран на колонки: чат | граф ---
chat_col, graph_col = st.columns([2, 3])

with chat_col:
    st.subheader("💬 Чат")

    # --- Поле ввода всегда видно ---
    user_input = st.chat_input("Введите ваш запрос...")

    if user_input:
        # Добавляем сообщение пользователя
        st.session_state.messages.append({"role": "user", "content": user_input})

    # Отображаем историю сообщений
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Если есть новое сообщение от пользователя
    if user_input:
        bot_response = process_text_message(user_input, G)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

with graph_col:
    st.subheader("📊 Визуализация графа")

    def draw_graph(G):
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)  # фиксируем layout для стабильности
        node_colors = []
        for n in G.nodes:
            node_data = G.nodes[n].get("data")
            if node_data and node_data.price > 0:
                node_colors.append("lightgreen")  # города с ценой
            else:
                node_colors.append("lightblue")
        nx.draw(
            G, pos,
            with_labels=True,
            labels={n: n for n in G.nodes()},
            node_color=node_colors,
            edge_color='gray',
            node_size=2500,
            font_size=10,
            ax=ax
        )
        return fig

    fig = draw_graph(G)
    st.pyplot(fig)