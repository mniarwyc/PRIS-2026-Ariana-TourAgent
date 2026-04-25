import streamlit as st
import torch
from torchvision import models, transforms
from PIL import Image
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

from logic import load_tours_from_csv, get_recommendations

st.set_page_config(page_title="Ariana TourAgent Pro", layout="wide")

# --- ЗАГРУЗКА БАЗЫ ---
current_dir = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(current_dir, "tours.csv")

@st.cache_resource
def get_data():
    return load_tours_from_csv(CSV_PATH)

tours_db = get_data()

# --- ЗАГРУЗКА ИИ (CV) ---
@st.cache_resource
def get_cv_model():
    # Загружаем веса новым способом
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    model.eval()
    return model

def classify_image(image, model):
    transform = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img_t = transform(image).unsqueeze(0)
    with torch.no_grad():
        out = model(img_t)
    _, index = torch.max(out, 1)
    return index.item()

cv_model = get_cv_model()

# --- ИНТЕРФЕЙС ---
st.title("🌍 Ariana TourAgent Pro")

# Сайдбар
with st.sidebar:
    st.header("📊 Статистика базы")
    if tours_db:
        st.success(f"✅ Загружено туров: {len(tours_db)}")
    else:
        st.error(f"⚠️ База пуста или не прочитана!")

    st.divider()

    st.header("📸 Угадай место (Stage 3: CV)")
    up_file = st.file_uploader("Загрузите фото для анализа", type=["jpg", "png", "jpeg"])
    if up_file:
        img = Image.open(up_file).convert('RGB')
        st.image(img)
        with st.spinner("ИИ сканирует пиксели..."):
            idx = classify_image(img, cv_model)
            
            # ТВОИ ОБНОВЛЕННЫЕ СПИСКИ ТУТ
            mountains = [970, 980, 688, 974, 971, 973] 
            beach = [972, 975, 979, 981, 372, 977, 978] 
            
            if idx in mountains: 
                label = "🏔 Горы / Природа"
            elif idx in beach: 
                label = "🏖 Пляж / Море"
            else: 
                label = "🏙 Архитектура / Разное"
            
            st.success(f"ИИ определил: **{label}**")

# --- STAGE 1: ГРАФ ЗНАНИЙ ---
if tours_db:
    st.subheader("🗺️ Интерактивная карта туров (Stage 1)")
    with st.expander("Показать граф связей", expanded=False):
        G = nx.Graph()
        for t in tours_db[:50]:
            G.add_node(t.name, label=f"{t.name}\n(${t.price})", title=t.country, color="#00ffcc", size=20)
            G.add_node(t.country, label=t.country, color="#ffcc00", size=15)
            G.add_edge(t.country, t.name, color="#444444")
            visa_node = f"Виза: {t.visa}"
            G.add_node(visa_node, label=visa_node, color="#ff5555", size=10)
            G.add_edge(t.name, visa_node, color="#444444")

        net = Network(height="450px", width="100%", bgcolor="#1a1a1a", font_color="white")
        net.toggle_physics(False)
        net.from_nx(G)
        
        path = "graph_temp.html"
        net.save_graph(path)
        with open(path, 'r', encoding='utf-8') as f:
            components.html(f.read(), height=470)

st.write("---")

# --- STAGE 2: ЧАТ И ПОИСК ---
st.subheader("🔎 Интеллектуальный поиск")

def render_tour_list(results):
    if not results:
        st.warning("⚠️ К сожалению, такого нет. Попробуйте написать по-другому (например, укажите страну, сезон или вид отдыха).")
        return
        
    st.success(f"🎯 Найдено вариантов: {len(results)}")
    for res in results:
        t = res["tour"]
        with st.container():
            st.markdown(f"### 📍 {t.name}, {t.country} — AI Совпадение: {res['score']}%")
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(t.image_url if t.image_url else "https://via.placeholder.com/150")
            with c2:
                st.write(f"**💰 Бюджет:** ${t.price} | **⭐ Рейтинг:** {t.rating}")
                v_col = "green" if t.visa.lower() == "нет" else "red"
                st.markdown(f"**🛂 Виза:** :{v_col}[{t.visa}] | **☀️ Сезон:** {t.season}")
                st.write(f"_{t.description}_")
                st.caption(f"🔖 Теги: {t.attributes}")
        st.divider()
    
    st.info("📞 **Понравился какой-то вариант?** Свяжитесь с нами по номеру **+7 (777) 123-45-67** или оставьте заявку для бронирования!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Куда бы ты хотел отправиться? (Например: 'Италия летом до 2000 без визы')", "results": None}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["content"]:
            st.markdown(msg["content"])
        if msg.get("results") is not None:
            render_tour_list(msg["results"])

if query := st.chat_input("Напишите ваш запрос..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
        
    with st.chat_message("assistant"):
        with st.spinner("Анализирую параметры..."):
            results = get_recommendations(tours_db, query)
            render_tour_list(results)
            st.session_state.messages.append({"role": "assistant", "content": None, "results": results})