# src/test_rules.py

from mock_data import test_entity
from logic import check_rules

# Несколько вариантов тестовых данных
test_cases = [
    {"metric_value": 5, "is_verified": True, "category_text": test_entity["category_text"], "tags_list": test_entity["tags_list"]},
    {"metric_value": 50, "is_verified": False, "category_text": test_entity["category_text"], "tags_list": test_entity["tags_list"]},
    {"metric_value": 50, "is_verified": True, "category_text": test_entity["category_text"], "tags_list": ["bad_tag_1"]},
    {"metric_value": 50, "is_verified": True, "category_text": test_entity["category_text"], "tags_list": ["tag_a"]},
]

print("=== Тестирование Rule-Based логики ===\n")

for i, case in enumerate(test_cases, start=1):
    result = check_rules(case)
    print(f"Тест #{i}: {case}")
    print(f"Результат: {result}\n")
