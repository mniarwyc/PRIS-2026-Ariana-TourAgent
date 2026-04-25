import pandas as pd
import networkx as nx
import io
import os

class TourEntity:
    def __init__(self, **kwargs):
        # Приводим все ключи к нижнему регистру для надежности
        d = {str(k).lower().strip(): v for k, v in kwargs.items()}
        
        self.name = d.get('name', 'Без названия')
        self.country = d.get('country', 'Не указана')
        self.price = d.get('price', 0)
        self.rating = d.get('rating', 0)
        self.description = d.get('description', '')
        
        # --- ИСПРАВЛЕНИЕ ОШИБКИ 'attributes' ---
        # Превращаем строку "озеро, горы" в список ['озеро', 'горы']
        attr_string = str(d.get('attributes', ''))
        self.attributes = [a.strip() for a in attr_string.split(',') if a.strip()]
        
        self.duration = d.get('duration', '')
        self.included = d.get('included', '')
        self.image_url = d.get('image_url', '')
        self.hotel_stars = d.get('hotel_stars', '')
        self.season = d.get('season', '')

def create_graph():
    G = nx.Graph()
    
    # Путь к файлу (учитывая твою структуру папок)
    possible_paths = [
        os.path.join('data', 'raw', 'tours.csv'),
        'tours.csv',
        os.path.join('..', 'data', 'raw', 'tours.csv')
    ]
    
    file_path = next((p for p in possible_paths if os.path.exists(p)), None)

    if not file_path:
        print("❌ Файл tours.csv не найден!")
        return G

    try:
        # Читаем бинарно для обхода проблем с кодировкой (0x98)
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        clean_text = raw_data.decode('utf-8', errors='replace').replace('\ufffd', ' ')
        
        # Читаем с защитой от "кривой" строки 128
        df = pd.read_csv(
            io.StringIO(clean_text), 
            on_bad_lines='skip', 
            engine='python',
            sep=','
        )
        
        # Чистим заголовки
        df.columns = df.columns.str.lower().str.strip()
        
        for index, row in df.iterrows():
            tour_data = row.to_dict()
            tour = TourEntity(**tour_data)
            
            node_id = str(tour.name).strip()
            if node_id and node_id != 'nan':
                # Сохраняем объект тура в узле
                G.add_node(node_id, data=tour, type='tour')
                
                # Создаем связь со страной
                country = str(tour.country).strip()
                if country and country != 'nan':
                    G.add_node(country, type='country')
                    G.add_edge(node_id, country)

        print(f"✅ Граф успешно собран! Узлов: {G.number_of_nodes()}")
            
    except Exception as e:
        print(f"❌ Критическая ошибка в create_graph: {e}")
        
    return G