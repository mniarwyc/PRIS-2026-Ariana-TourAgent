import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'rules.json')

def load_rules():
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_rules(data):
    rules = load_rules()
    
    # 1. Хард-фильтры
    if rules['critical_rules']['must_be_verified'] and not data['is_verified']:
        return "⛔️ Критическая ошибка: Объект не прошел первичную проверку"
    
    # 2. Проверка числового диапазона
    if data['metric_value'] < rules['thresholds']['min_value']:
        return "❌ Отказ: Значение ниже допустимого порога"
    
    # 3. Проверка черного списка
    for tag in data['tags_list']:
        if tag in rules['lists']['blacklist']:
            return f"⚠️ Предупреждение: Найден запрещенный элемент ({tag})"
    
    return f"✅ Успех: Объект соответствует сценарию '{rules['scenario_name']}'"
