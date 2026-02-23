import json

def check_rules(data):
    """
    Проверяет словарь данных по правилам (Lab2)
    """
    # Для примера можно оставить простой проверочный блок
    min_val = 10
    max_val = 100
    metric = data.get("metric_value", 0)

    if metric < min_val:
        return f"❌ Отказ: Значение {metric} ниже минимального {min_val}"
    if metric > max_val:
        return f"❌ Отказ: Значение {metric} выше максимального {max_val}"

    if not data.get("is_verified", True):
        return "⛔️ Критическая ошибка: Объект не прошел проверку"

    tags = data.get("tags_list", [])
    if "forbidden" in tags:
        return f"⚠️ Предупреждение: Найден запрещенный тег ({', '.join(tags)})"

    return "✅ Объект соответствует правилам"

def process_text_message(text, graph):
    """
    Принимает текст пользователя и ищет узел в графе.
    Если узел найден — выводим его характеристики.
    Если нет — стандартный ответ.
    """
    text = text.strip()

    if not graph:
        return "Граф пока не загружен."

    # --- Проверяем узел в графе ---
    if text in graph.nodes:
        node_data = graph.nodes[text].get("data")
        response = f"✅ Я нашел '{text}' в базе!\n"
        neighbors = list(graph.neighbors(text))
        if node_data:
            # Добавляем атрибуты
            if hasattr(node_data, "attributes") and node_data.attributes:
                response += f"- Атрибуты: {', '.join(node_data.attributes)}\n"
            # Добавляем цену
            if hasattr(node_data, "price") and node_data.price > 0:
                response += f"- Цена: {node_data.price}$\n"
        if neighbors:
            # Выводим соседей
            response += f"- Связано с: {', '.join(neighbors)}"
        else:
            response += "- Связей нет"
        return response

    # --- Проверка ключевых слов ---
    lowered = text.lower()
    if "правило" in lowered or "проверить объект" in lowered:
        sample_data = {"metric_value": 50, "is_verified": True, "tags_list": ["tour", "hotel"]}
        return check_rules(sample_data)

    if "привет" in lowered or "здравствуй" in lowered:
        return "Привет! Я готов помочь. Напиши название объекта."

    return "Я не знаю такого термина. Попробуй ввести узел графа или ключевое слово."