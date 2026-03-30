import streamlit as st
import pandas as pd
import os
from logic import process_text_message
from knowledge_graph import create_graph
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(layout="wide", page_title="TourAgent Data Intelligence", page_icon="📈")

if "graph" not in st.session_state:
    st.session_state.graph = create_graph()
if "messages" not in st.session_state:
    st.session_state.messages = []

G = st.session_state.graph

# --- SIDEBAR ---
with st.sidebar:
    st.title("📊 Система управления")
    st.write(f"Узлов в графе: {len(G.nodes())}")
    if st.button("🗑 Очистить чат"):
        st.session_state.messages = []
        st.rerun()

# --- ОСНОВНАЯ ЧАСТЬ (Вкладки) ---
tab_chat, tab_stats = st.tabs(["💬 Интеллектуальный чат", "📈 Аналитика датасета"])

with tab_chat:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        user_input = st.chat_input("Спросите: 'Топ отелей до 1000$'")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"): st.markdown(user_input)
            response = process_text_message(user_input, G)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"): st.markdown(response)

    with col2:
        st.subheader("🌐 Граф связей")
        fig, ax = plt.subplots(figsize=(6, 5))
        sub_nodes = list(G.nodes())[:25]
        sub_G = G.subgraph(sub_nodes)
        pos = nx.spring_layout(sub_G, seed=42)
        nx.draw(sub_G, pos, with_labels=True, node_color='orange', node_size=800, font_size=7, ax=ax)
        st.pyplot(fig)

with tab_stats:
    st.subheader("🔍 Глубокий анализ данных (Pandas Analytics)")
    csv_path = os.path.join("data", "tours.csv")
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        col_st1, col_st2 = st.columns(2)
        
        with col_st1:
            st.write("**💰 Распределение цен в датасете**")
            fig2, ax2 = plt.subplots()
            df['price'].hist(bins=10, color='skyblue', ax=ax2)
            ax2.set_xlabel("Цена ($)")
            ax2.set_ylabel("Количество туров")
            st.pyplot(fig2)
            
        with col_st2:
            st.write("**⭐ Топ-5 направлений по рейтингу**")
            top_df = df.nlargest(5, 'rating')[['name', 'rating', 'price']]
            st.table(top_df)
            
        st.write("**📂 Сырые данные (Dataset View):**")
        st.dataframe(df, use_container_width=True)