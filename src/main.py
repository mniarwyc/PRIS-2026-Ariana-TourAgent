import streamlit as st
from mock_data import test_entity as default_data
from logic import check_rules

st.title("Rule-Based System Debugger 🛠")
st.write("### Настройка входящих данных")

user_number = st.sidebar.number_input("Введите рейтинг отеля:", value=default_data["metric_value"])
user_bool = st.sidebar.checkbox("Отель проверен", value=default_data["is_verified"])

if st.button("Запустить проверку"):
    current_test_data = {
        "metric_value": user_number,
        "is_verified": user_bool,
        "category_text": default_data["category_text"],
        "tags_list": default_data["tags_list"]
    }
    
    result = check_rules(current_test_data)
    
    if "✅" in result:
        st.success(result)
    elif "⛔️" in result:
        st.error(result)
    else:
        st.warning(result)
