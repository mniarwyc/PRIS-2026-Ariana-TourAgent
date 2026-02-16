import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from knowledge_graph import create_graph, find_related_entities

st.title("Tour Knowledge Graph 🌍")

G = create_graph()

all_nodes = list(G.nodes())
selected_node = st.selectbox("Выберите объект:", all_nodes)

if st.button("Показать связи"):
    results = find_related_entities(G, selected_node)
    st.success(f"{selected_node} связан с: {', '.join(results)}")

st.write("### Визуализация графа")

fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G)

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
