# src/knowledge_graph.py

import networkx as nx

class TourEntity:
    def __init__(self, name, attributes=None, price=0.0):
        self.name = name
        self.attributes = attributes or []
        self.price = price

    def __repr__(self):
        attr_str = ", ".join(self.attributes) if self.attributes else "Нет атрибутов"
        return f"{self.name} ({attr_str}) - {self.price}$"


def create_graph():
    G = nx.Graph()

    # --- Страны ---
    turkey = TourEntity("Турция")
    italy = TourEntity("Италия")
    uae = TourEntity("ОАЭ")

    # --- Города ---
    antalya = TourEntity("Анталия", attributes=["Пляж"], price=500.0)
    rome = TourEntity("Рим", attributes=["Экскурсии"], price=700.0)
    dubai = TourEntity("Дубай", attributes=["Шопинг"], price=800.0)

    # --- Виза ---
    visa_needed = TourEntity("Нужна виза")
    visa_free = TourEntity("Без визы")

    # --- Добавляем все объекты в граф ---
    nodes = [turkey, italy, uae, antalya, rome, dubai, visa_needed, visa_free]
    for node in nodes:
        G.add_node(node.name, data=node)

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
    """
    Возвращает список связанных узлов.
    Если узел — объект TourEntity с ценой, показываем цену.
    """
    if start_node not in graph:
        return []

    neighbors = list(graph.neighbors(start_node))
    result = []
    for n in neighbors:
        node_data = graph.nodes[n].get("data")
        if node_data:
            info = n
            if hasattr(node_data, "price") and node_data.price > 0:
                info += f" (цена: {node_data.price}$)"
            result.append(info)
        else:
            result.append(n)
    return result