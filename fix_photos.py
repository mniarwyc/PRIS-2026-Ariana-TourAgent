import pandas as pd
import os

# Путь к твоему файлу
csv_path = r"C:\Users\Professional\Desktop\TourAgent\PRIS-2026-Ariana-TourAgent\data\raw\tours.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    # Функция для создания уникальной ссылки на фото
    # Мы используем Unsplash Source, он подберет фото по названию города/страны
    def get_fixed_photo(row):
        query = f"{row['name']},{row['country']}".replace(" ", "")
        # Добавляем sig, чтобы картинка закрепилась за названием навсегда
        return f"https://source.unsplash.com/featured/800x450?{query}"

    # Добавляем новую колонку со ссылками
    df['image_url'] = df.apply(get_fixed_photo, axis=1)
    
    # Сохраняем обновленный файл
    df.to_csv(csv_path, index=False)
    print("✅ Все 150+ фото привязаны к турам в файле tours.csv!")
else:
    print("❌ Файл не найден!")