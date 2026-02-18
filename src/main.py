import streamlit as st
from logic import process_text_message
from knowledge_graph import load_graph
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide")
st.title("Tour Knowledge Graph & Chat 🌍🤖")

# --- Инициализация истории чата ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Создаём граф ---
G = load_graph()

# --- Разделяем экран на колонки: чат | граф ---
chat_col, graph_col = st.columns([2, 3])

with chat_col:
    st.subheader("💬 Чат")
    
    # Кнопки быстрого теста
    if st.button("Привет"):
        user_input = "привет"
        st.session_state.messages.append({"role": "user", "content": user_input})
    elif st.button("Проверить объект"):
        user_input = "проверить объект"
        st.session_state.messages.append({"role": "user", "content": user_input})
    else:
        user_input = st.chat_input("Введите ваш запрос...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

    # Отображаем историю сообщений
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Если есть новое сообщение, получаем ответ бота
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        bot_response = process_text_message(st.session_state.messages[-1]["content"], G)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

with graph_col:
    st.subheader("📊 Визуализация графа")

    def draw_graph(G):
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
        return fig

    fig = draw_graph(G)
    st.pyplot(fig)
