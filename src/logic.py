def process_text_message(user_input, graph):
    user_input = user_input.strip().lower()

    # Приветствие
    if user_input in ["привет", "здравствуйте", "hello"]:
        return "Привет! Введи страну, город или тип отдыха 😊"

    # Ищем узел в графе (без учета регистра)
    for node in graph.nodes:
        if node.lower() == user_input:
            neighbors = list(graph.neighbors(node))
            
            if neighbors:
                return f"Связанные объекты: {', '.join(neighbors)}"
            else:
                return "У этого узла нет связей."

    return "Я не знаю такого термина. Попробуй ввести узел графа."
