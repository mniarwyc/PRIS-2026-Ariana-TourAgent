from src.knowledge_graph import create_graph
from src.logic import process_text_message

# 1. Загружаем твой гигантский граф
print("🚀 Загрузка графа из 150+ узлов...")
graph = create_graph()
print(f"✅ Граф готов! Узлов: {graph.number_of_nodes()}, Связей: {graph.number_of_edges()}")

# 2. Эмулируем чат
queries = [
    "Хочу в горы в Казахстане до 800$",
    "Покажи что-нибудь экзотическое с пляжем и pool",
    "Боровое",
    "Япония история и шопинг"
]

for q in queries:
    print(f"\n👤 Юзер: {q}")
    response = process_text_message(q, graph)
    print(f"🤖 Бот:\n{response}")
    print("-" * 50)