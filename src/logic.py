# src/logic.py

import json
import os

# Автоматическое определение пути к файлу rules.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'rules.json')

def load_rules():
    """Загружает правила из JSON"""
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_rules(data):
    """
    Проверяет словарь данных data по правилам из JSON.
    Возвращает строковый вердикт.
    """
    rules = load_rules()
    
    # --- 1. Критические проверки (Hard Filters) ---
    if rules['critical_rules'].get('must_be_verified', False) and not data.get('is_verified', False):
        return "⛔️ Критическая ошибка: Объект не прошел первичную проверку"

    # --- 2. Проверка числового диапазона (Thresholds) ---
    min_val = rules['thresholds'].get('min_value', float('-inf'))
    max_val = rules['thresholds'].get('max_value', float('inf'))
    metric = data.get('metric_value', 0)

    if metric < min_val:
        return f"❌ Отказ: Значение {metric} ниже минимального {min_val}"
    if metric > max_val:
        return f"❌ Отказ: Значение {metric} выше максимального {max_val}"

    # --- 3. Проверка запрещённых и разрешённых элементов (Blacklist / Whitelist) ---
    blacklist = set(rules['lists'].get('blacklist', []))
    whitelist = set(rules['lists'].get('whitelist', []))
    tags = set(data.get('tags_list', []))

    # Если есть запрещённые теги
    blocked = tags & blacklist
    if blocked:
        return f"⚠️ Предупреждение: Найден запрещенный элемент ({', '.join(blocked)})"

    # Если есть whitelist, убедимся, что хотя бы один элемент есть в списке
    if whitelist and not (tags & whitelist):
        return f"❌ Отказ: Нет обязательных элементов из whitelist ({', '.join(whitelist)})"

    # Всё прошло
    return f"✅ Успех: Объект соответствует сценарию '{rules.get('scenario_name', 'Без имени')}'"
