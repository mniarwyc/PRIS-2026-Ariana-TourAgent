import json
import os
from models import TourEntity

def load_rules():
    path = os.path.join("data", "rules.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def check_rules(entity: TourEntity):
    rules = load_rules()
    if not rules: return ["⚠️ Правила не найдены"]
    
    reports = []
    max_price = rules["thresholds"]["max_value"]
    needed_tags = rules["lists"]["whitelist"]

    # Проверка цены
    if entity.price > max_price:
        reports.append(f"❌ Дорого: {entity.price}$ (лимит {max_price}$)")
    else:
        reports.append(f"✅ Цена в пределах нормы")

    # Проверка тегов
    found_tags = [t.lower() for t in entity.attributes]
    for tag in needed_tags:
        if tag.lower() not in found_tags:
            reports.append(f"⚠️ Нет услуги: {tag}")
    
    return reports

def process_text_message(text, graph):
    text = text.strip()
    if text in graph.nodes:
        node_data = graph.nodes[text].get("data")
        
        if isinstance(node_data, TourEntity):
            res = f"### 📍 {text}\n"
            if node_data.price > 0: res += f"**Цена:** {node_data.price}$\n"
            res += f"**Теги:** {', '.join(node_data.attributes)}\n\n"
            
            # Экспертиза
            res += "🤖 **Анализ:**\n"
            for v in check_rules(node_data):
                res += f"- {v}\n"
            return res
        return f"Узел '{text}' найден (информационный)."
    
    return "Я не нашел такой город или страну. Попробуй: Анталия, Рим или Дубай."