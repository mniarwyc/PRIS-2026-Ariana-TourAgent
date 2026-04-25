import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Импортируем твои обновленные модули
from knowledge_graph import create_graph
from logic import process_text_message

st.set_page_config(page_title="Ariana TourAgent", layout="wide")

## 🌍 Интеллектуальный поиск туров Ariana

# 1. Загрузка данных с защитой от ошибок
@st.cache_resource
def get_data():
    try:
        return create_graph()
    except Exception as e:
        st.error(f" Ошибка при создании графа: {e}")
        return nx.Graph() # Возвращаем пустой граф, чтобы приложение не упало

graph = get_data()

# Сайдбар с инфо
with st.sidebar:
    st.header("📊 Статистика базы")
    if graph.number_of_nodes() > 0:
        st.success(f"✅ Узлов в графе: {graph.number_of_nodes()}")
    else:
        st.warning("⚠️ Граф пуст. Проверьте tours.csv")
    st.info("Поиск работает на основе связей между странами и атрибутами туров.")

# 2. ВИЗУАЛИЗАЦИЯ ГРАФА
st.subheader("🗺️ Интерактивная карта туров")

def visualize_graph(G):
    # Берем топ-70 узлов для плавности работы
    nodes_to_show = list(G.nodes())[:70]
    subG = G.subgraph(nodes_to_show)
    
    net = Network(height="450px", width="100%", bgcolor="#1a1a1a", font_color="white")
    net.toggle_physics(False) # Чтобы не лагало
    
    for node, data in subG.nodes(data=True):
        # Проверяем, есть ли данные тура в узле
        tour = data.get('data')
        if tour:
            label = f"{tour.name}\n({tour.price}$)"
            net.add_node(node, label=label, title=f"Страна: {tour.country}", color="#00ffcc", size=20)
        else:
            # Если это узел страны или атрибута
            net.add_node(node, label=node, color="#ffcc00", size=15)
    
    for edge in subG.edges():
        net.add_edge(edge[0], edge[1], color="#444444")

    # Сохранение и вывод
    path = "graph_temp.html"
    net.save_graph(path)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    components.html(html, height=470)

# Рисуем облегченный граф
if graph.number_of_nodes() > 0:
    visualize_graph(graph)
else:
    st.info("Визуализация недоступна: граф не содержит данных.")

st.write("---")

# 3. ПОИСКОВЫЙ ИНТЕРФЕЙС
if "messages" not in st.session_state:
    st.session_state.messages = []

# История чата
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Строка поиска
if prompt := st.chat_input("Куда отправимся? Напишите страну, город или тип отдыха"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Вызов логики
    with st.chat_message("assistant"):
        with st.spinner("Ищу лучшие предложения..."):
            response = process_text_message(prompt, graph)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})