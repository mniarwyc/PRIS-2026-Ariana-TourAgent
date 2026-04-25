import networkx as nx
import re

def process_text_message(prompt, G):
    prompt_lower = prompt.lower()
    found_tours = []

    # 1. ПЫТАЕМСЯ ВЫДЕЛИТЬ ЦЕНУ ИЗ ЗАПРОСА (например, "до 1000")
    max_price_limit = None
    # Ищем все числа в строке
    numbers = re.findall(r'\d+', prompt)
    if numbers:
        # Если нашли число и рядом есть слова-ограничители
        if any(word in prompt_lower for word in ["до", "дешевле", "меньше", "бюджет"]):
            max_price_limit = int(numbers[0])

    # 2. ПОИСК ТУРОВ В ГРАФЕ
    for node, data in G.nodes(data=True):
        if data.get('type') == 'tour':
            tour = data.get('data')
            if not tour:
                continue
            
            # Проверка по словам (страна или море/горы)
            match_country = tour.country.lower() in prompt_lower
            match_attr = any(attr.lower() in prompt_lower for attr in tour.attributes)
            
            # ЕСЛИ НАШЛИ ПО СЛОВАМ, ПРОВЕРЯЕМ ЦЕНУ
            if match_country or match_attr:
                # Если пользователь указал лимит по цене, а тур дороже — пропускаем его
                if max_price_limit and int(tour.price) > max_price_limit:
                    continue
                    
                found_tours.append(tour)

    # 3. ФОРМИРОВАНИЕ ОТВЕТА
    if not found_tours:
        return (
            "🔍 **К сожалению, я не нашла подходящих туров.**\n\n"
            "Возможно, стоит немного увеличить бюджет или выбрать другое направление.\n"
            "📞 **Свяжитесь с нами:** +7 (xxx) xxx-xx-xx, и мы найдем для вас горящее предложение! ✨"
        )

    count = len(found_tours)
    response = f"🚀 **Ариана подобрала для вас {count} подходящих вариантов:**\n\n"
    response += "---\n"

    for i, tour in enumerate(found_tours, 1):
        response += f"### {i}. {tour.name}, {tour.country}\n"
        response += f"💰 **Цена:** {tour.price}$ | ⭐ **Рейтинг:** {tour.rating}\n\n"
        response += f"_{tour.description}_\n\n"
        
        if tour.image_url and "http" in tour.image_url:
            response += f"![Tour Image]({tour.image_url})\n\n"
        
        response += "---\n"

    response += "\n✨ **Заинтересовал какой-то из этих вариантов?**\n"
    response += "Если у вас возникли вопросы, просто свяжитесь с нами. Мы поможем всё оформить! \n\n"
    response += "📞 **Наш телефон:** +7 (xxx) xxx-xx-xx"

    return response