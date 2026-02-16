import networkx as nx

def create_graph():
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


def find_related_entities(graph, start_node):
    if start_node not in graph:
        return []
    return list(graph.neighbors(start_node))
