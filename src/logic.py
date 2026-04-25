import csv
import re
import io
import streamlit as st
from models import Tour

def load_tours_from_csv(filepath):
    content = ""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        try:
            with open(filepath, 'r', encoding='cp1251', errors='replace') as f:
                content = f.read()
        except Exception as e:
            st.sidebar.error(f"🚨 Файл невозможно открыть: {e}")
            return []

    if not content.strip():
        return []

    first_line = content.split('\n')[0]
    delimiter = ';' if ';' in first_line else ','

    tours = []
    try:
        reader = csv.DictReader(io.StringIO(content), delimiter=delimiter)
        if reader.fieldnames:
            reader.fieldnames = [str(col).strip().lower().replace('\ufeff', '') for col in reader.fieldnames]

        for row in reader:
            try:
                tours.append(Tour(
                    name=row.get('name', 'Без названия'),
                    country=row.get('country', 'Неизвестно'),
                    price=row.get('price', 0),
                    rating=row.get('rating', 0),
                    description=row.get('description', ''),
                    attributes=row.get('attributes', ''),
                    duration=row.get('duration', ''),
                    included=row.get('included', ''),
                    image_url=row.get('image_url', ''),
                    hotel_stars=row.get('hotel_stars', ''),
                    season=row.get('season', ''),
                    visa=row.get('visa', '')
                ))
            except Exception:
                continue 
                
    except Exception as e:
        return []

    return tours

def get_recommendations(tours, query):
    query = query.lower()
    
    # 1. Цена
    numbers = re.findall(r'\d+', query)
    has_budget = False
    max_price = float('inf')
    if numbers and int(max(numbers)) > 100:
        max_price = float(max([int(n) for n in numbers]))
        has_budget = True

    # 2. Виза
    visa_filter = None
    if "без виз" in query or "виза не нужна" in query: visa_filter = "нет"
    elif "с визой" in query or "нужна виза" in query: visa_filter = "да"

    # 3. Сезон
    season_filter = None
    if "лет" in query: season_filter = "лето"
    elif "зим" in query: season_filter = "зима"
    elif "весн" in query: season_filter = "весна"
    elif "осен" in query: season_filter = "осень"

    # Проверяем, ввел ли пользователь хоть один фильтр
    has_any_filter = has_budget or bool(visa_filter) or bool(season_filter)
    
    # Разбиваем запрос на слова, чтобы "бебеб" не цеплялся за случайные буквы
    query_words = set(re.findall(r'[а-яa-z]+', query))

    results = []
    for t in tours:
        if t.price > max_price: continue
        if visa_filter and visa_filter != t.visa.lower(): continue
        if season_filter and season_filter not in t.season.lower(): continue

        score = t.rating * 10 
        matched_text = False
        
        # Проверка страны
        if t.country.lower() in query and len(t.country) > 2:
            score += 40
            matched_text = True
        
        # Проверка тегов
        attr_words = set(re.findall(r'[а-яa-z]+', t.attributes.lower()))
        if query_words.intersection(attr_words):
            score += 20
            matched_text = True
        
        # ⛔ ЗАЩИТА ОТ МУСОРА:
        # Если в запросе нет ни цены, ни сезона, ни визы, и слова не совпали ни с одной страной или тегом - пропускаем!
        if not has_any_filter and not matched_text:
            continue
            
        match_perc = min(99, int(score + 10))
        results.append({"tour": t, "score": match_perc})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:5]