import networkx as nx
import pandas as pd
import os
from models import TourEntity 

def create_graph():
    """
    Создает интеллектуальный граф знаний на основе CSV-датасета.
    Использует Pandas для обработки данных и NetworkX для построения связей.
    """
    G = nx.Graph()
    
    # Путь к нашему расширенному датасету (40+ записей)
    csv_path = os.path.join("data", "tours.csv")
    
    if os.path.exists(csv_path):
        # 1. Читаем датасет через PANDAS
        df = pd.read_csv(csv_path)
        
        for _, row in df.iterrows():
            # 2. Создаем объект TourEntity из строки таблицы (ООП подход)
            ent = TourEntity(
                name=str(row['name']),
                # Превращаем строку "Пляж;wifi" в список ["Пляж", "wifi"]
                attributes=str(row['attributes']).split(';'), 
                price=float(row['price']),
                rating=float(row['rating']),
                description=str(row['description'])
            )
            
            # 3. Добавляем город в граф как узел с данными
            G.add_node(ent.name, data=ent, type='city')
            
            # 4. Обработка страны: создаем узел, если его еще нет
            country_name = str(row['country'])
            if country_name not in G:
                # Узел страны (технический узел для группировки)
                country_ent = TourEntity(name=country_name, attributes=["Страна"])
                G.add_node(country_name, data=country_ent, type='country')
            
            # 5. Создаем связь между городом и его страной
            G.add_edge(ent.name, country_name)
    
    # --- 6. Добавление логических связей (Визовый режим) ---
    # Группируем страны по визовым правилам для экспертной оценки
    no_visa_countries = ["Турция", "ОАЭ", "Таиланд", "Япония", "Индонезия", "Корея", "Чехия"]
    visa_required_countries = ["Италия", "Франция", "Испания", "Германия", "США", "Австрия", "Англия"]

    for country in no_visa_countries:
        if country in G:
            G.add_edge(country, "Без визы")
            
    for country in visa_required_countries:
        if country in G:
            G.add_edge(country, "Нужна виза")

    return G