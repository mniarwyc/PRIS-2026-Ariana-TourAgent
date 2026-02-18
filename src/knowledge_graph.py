import networkx as nx

def load_graph():   
    G = nx.Graph()

    # --- Узлы ---
    countries = ["Турция", "Италия", "ОАЭ"]
    cities = ["Анталия", "Рим", "Дубай"]
    vacation_types = ["Пляж", "Экскурсии", "Шопинг"]
    visa = ["Нужна виза", "Без визы"]

    G.add_nodes_from(countries, type="country")
    G.add_nodes_from(cities, type="city")
    G.add_nodes_from(vacation_types, type="vacation")
    G.add_nodes_from(visa, type="visa")

    # --- Связи ---
    relationships = [
        ("Анталия", "Турция"),
        ("Рим", "Италия"),
        ("Дубай", "ОАЭ"),

        ("Анталия", "Пляж"),
        ("Рим", "Экскурсии"),
        ("Дубай", "Шопинг"),

        ("Турция", "Без визы"),
        ("Италия", "Нужна виза"),
        ("ОАЭ", "Без визы"),
    ]

    G.add_edges_from(relationships)

    return G


def find_related_entities(graph, user_input):
    if not user_input:
        return []

    user_input = user_input.strip().lower()

    # создаём словарь: нижний регистр -> реальное имя узла
    nodes_lower = {node.lower(): node for node in graph.nodes}

    if user_input in nodes_lower:
        real_node = nodes_lower[user_input]
        return list(graph.neighbors(real_node))

    return []
