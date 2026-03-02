import json
import os
import re
from models import TourEntity

def load_rules():
    """Загружает динамические правила из JSON"""
    path = os.path.join("data", "rules.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def check_rules(entity: TourEntity):
    """Экспертная проверка объекта по правилам (бюджет и др.)"""
    rules = load_rules()
    if not rules:
        return ["⚠️ Система правил (JSON) недоступна."]

    reports = []
    thresholds = rules.get("thresholds", {})
    
    # Сверяем цену объекта с лимитом из JSON
    max_allowed = thresholds.get("max_value", 1000)
    if entity.price > max_allowed:
        reports.append(f"❌ Превышен бюджет: {entity.price}$ > {max_allowed}$")
    else:
        reports.append(f"✅ Цена соответствует вашим правилам")

    return reports

def process_text_message(text, graph):
    """Основной процессор сообщений с семантическим поиском"""
    text = text.lower().strip()
    
    # --- 1. Извлечение цены через Регулярные Выражения (Regex) ---
    # Ищет конструкции типа "до 500", "меньше 1000", "бюджет 700"
    price_match = re.search(r'(?:до|меньше|дешевле|бюджет)\s*(\d+)', text)
    requested_limit = float(price_match.group(1)) if price_match else None

    # --- 2. Поиск по ключевым тегам ---
    keywords = ["пляж", "wifi", "шопинг", "экскурсии", "виза", "pool", "all inclusive"]
    found_tags = [k for k in keywords if k in text]

    # --- 3. Проверка на точное совпадение имени (например, "Дубай") ---
    for node in graph.nodes:
        if node.lower() == text:
            data = graph.nodes[node].get("data")
            if isinstance(data, TourEntity):
                res = f"### 📍 Объект: {node}\n"
                res += f"**Цена:** {data.price}$ | **Рейтинг:** ⭐{data.rating}\n"
                res += f"**Теги:** {', '.join(data.attributes)}\n"
                res += f"**Описание:** {data.description}\n\n"
                res += "🤖 **Экспертное заключение:**\n"
                for v in check_rules(data):
                    res += f"- {v}\n"
                return res

    # --- 4. Многокритериальный поиск (фильтрация всего графа) ---
    recommendations = []
    for node in graph.nodes:
        data = graph.nodes[node].get("data")
        # Пропускаем узлы без данных или страны (у них цена 0)
        if not data or not isinstance(data, TourEntity) or data.price == 0:
            continue

        # Условия фильтрации
        price_ok = True if not requested_limit else data.price <= requested_limit
        tag_ok = True if not found_tags else any(t in [a.lower() for a in data.attributes] for t in found_tags)

        if price_ok and tag_ok:
            recommendations.append(data)

    # Формируем интеллектуальный ответ
    if recommendations:
        # Сортировка по рейтингу (Data-driven подход)
        recommendations.sort(key=lambda x: x.rating, reverse=True)
        
        response = f"🎯 **Я нашел подходящие варианты ({len(recommendations)}):**\n\n"
        for r in recommendations:
            response += f"🔹 **{r.name}** — {r.price}$ (⭐{r.rating})\n"
            response += f"   _Теги: {', '.join(r.attributes)}_\n\n"
        return response

    # Если ничего не подошло
    if "привет" in text:
        return "Привет! Я TourAgent. Могу найти тур по названию или по критериям (например: 'пляж до 1000$')."
    
    return "🤔 К сожалению, ничего не нашлось. Попробуйте изменить бюджет или ключевые слова."