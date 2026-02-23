import networkx as nx
from models import TourEntity 

def create_graph():
    G = nx.Graph()

    # --- Создаем объекты (ООП подход) ---
    turkey = TourEntity("Турция", attributes=["Без визы"])
    italy = TourEntity("Италия", attributes=["Нужна виза"])
    uae = TourEntity("ОАЭ", attributes=["Без визы"])

    antalya = TourEntity("Анталия", attributes=["Пляж", "wifi"], price=500.0)
    rome = TourEntity("Рим", attributes=["Экскурсии"], price=700.0)
    dubai = TourEntity("Дубай", attributes=["Шопинг", "pool", "wifi"], price=850.0)

    # --- Добавляем объекты в граф правильно ---
    entities = [turkey, italy, uae, antalya, rome, dubai]
    for ent in entities:
        G.add_node(ent.name, data=ent)

    # --- Связи (просто по именам) ---
    G.add_edges_from([
        ("Анталия", "Турция"),
        ("Рим", "Италия"),
        ("Дубай", "ОАЭ"),
        ("Турция", "Без визы"),
        ("Италия", "Нужна виза"),
        ("ОАЭ", "Без визы")
    ])

    return G