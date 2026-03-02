import streamlit as st
from logic import process_text_message
from knowledge_graph import create_graph
import matplotlib.pyplot as plt
import networkx as nx

# Настройка страницы
st.set_page_config(layout="wide", page_title="TourAgent Pro AI", page_icon="🌍")

# 1. Инициализация Графа Знаний в сессии (чтобы не перегружать память)
if "graph" not in st.session_state:
    st.session_state.graph = create_graph()

# 2. Инициализация истории сообщений
if "messages" not in st.session_state:
    st.session_state.messages = []

G = st.session_state.graph

# --- БОКОВАЯ ПАНЕЛЬ (Sidebar) ---
with st.sidebar:
    st.title("⚙️ Управление AI")
    st.markdown("---")
    st.markdown("""
    **TourAgent v2.0**
    Интеллектуальная система на основе:
    - Графа знаний (NetworkX)
    - Базы правил (JSON)
    - NLP-фильтрации (Regex)
    """)
    
    if st.button("🗑 Очистить чат"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    st.caption("Разработано в рамках ЛР №6 по дисциплине ПРИС")

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
chat_col, graph_col = st.columns([1, 1])

with chat_col:
    st.subheader("💬 Чат с агентом")
    
    # Контейнер для истории (чтобы чат прокручивался)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ПОЛЕ ВВОДА (Всегда на виду внизу колонки)
    user_input = st.chat_input("Напишите: 'пляж до 900$' или 'Дубай'...")

    if user_input:
        # Отображаем сообщение пользователя
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Логика ответа бота
        with st.spinner('Анализирую базу знаний...'):
            response = process_text_message(user_input, G)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

with graph_col:
    st.subheader("📊 Визуализация базы знаний")
    
    # Настройка отрисовки графа
    fig, ax = plt.subplots(figsize=(7, 5))
    pos = nx.spring_layout(G, seed=42) # Фиксируем узлы
    
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_color='skyblue', 
        edge_color='#bbbbbb', 
        node_size=1800, 
        font_size=9, 
        font_weight='bold',
        ax=ax
    )
    
    st.pyplot(fig)
    st.write("💡 *Граф отображает связи между странами, городами и условиями въезда.*")