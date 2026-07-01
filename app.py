import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Настройка стиля Apple + Bilimtech
st.set_page_config(page_title="Bilimtech CRM", page_icon="🦅", layout="wide")

st.markdown("""
    <style>
    /* Фон и общие шрифты */
    .main { background-color: #F5F5F7; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    /* Стилизация карточек (Apple Style) */
    .apple-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        border: 1px solid rgba(0, 0, 0, 0.02);
    }
    
    /* Кнопки в фирменном синем цвете Bilimtech */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #005CB9 0%, #00A3E0 100%);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 92, 185, 0.3);
    }
    
    /* Кастомные баджи для статусов */
    .badge {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
    }
    .badge-active { background-color: #E1F5FE; color: #005CB9; }
    .badge-success { background-color: #E8F5E9; color: #2E7D32; }
    .badge-neutral { background-color: #F5F5F7; color: #6E6E73; }
    </style>
    """, unsafe_allow_html=True)

# 2. Инициализация демо-данных (Имитация базы данных)
if 'crm_db' not in st.session_state:
    st.session_state.crm_db = pd.DataFrame([
        {
            "ФИО Родителя": "Айгуль Исмаилова", "Телефон": "+996555123456", "Ребенок": "Амир",
            "Олимпиады": "Участвовал", "Туры (Гарвард)": "Интересуется", "Курсы": "Обучается",
            "Заметки": "Просил перезвонить в понедельник", "Изменил(а)": "Наргиза", "Дата": "2026-07-01 12:00"
        },
        {
            "ФИО Родителя": "Бакыт Асанов", "Телефон": "+996700443322", "Ребенок": "Салима",
            "Олимпиады": "Не участвовал", "Туры (Гарвард)": "Оплатил", "Курсы": "Нет",
            "Заметки": "Документы готовы", "Изменил(а)": "Айбек", "Дата": "2026-07-01 14:30"
        }
    ])

# Список пользователей для авторизации (в будущем перенесем в Supabase Auth)
USERS_MOCK = {"nargiza@bilimtech.kg": "12345", "aibek@bilimtech.kg": "12345", "admin@bilimtech.kg": "12345"}
USER_NAMES = {"nargiza@bilimtech.kg": "Наргиза", "aibek@bilimtech.kg": "Айбек", "admin@bilimtech.kg": "Администратор"}

# 3. Логика авторизации
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""

if not st.session_state.logged_in:
    st.markdown('<div class="apple-card" style="max-width: 400px; margin: 100px auto; text-align: center;">', unsafe_allow_html=True)
    st.image("http://googleusercontent.com/generated_image_content/0", width=250)
    st.subheader("Вход в систему CRM")
    
    email = st.text_input("Email (Логин)")
    password = st.text_input("Пароль", type="password")
    login_btn = st.button("Войти")
    
    if login_btn:
        if email in USERS_MOCK and USERS_MOCK[email] == password:
            st.session_state.logged_in = True
            st.session_state.user_name = USER_NAMES[email]
            st.rerun()
        else:
            st.error("Неверный логин или пароль")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- ИНТЕРФЕЙС CRM ПОСЛЕ ВХОДА ---
    
    # Шапка приложения
    col_logo, col_user = st.columns([4, 1])
    with col_logo:
        st.image("http://googleusercontent.com/generated_image_content/0", width=180)
    with col_user:
        st.markdown(f"<p style='text-align: right; color: #6E6E73; margin-top: 10px;'>Пользователь: <b>{st.session_state.user_name}</b></p>", unsafe_allow_html=True)
        if st.button("Выйти", key="logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.title("Панель управления клиентами")
    
    # Поиск и фильтры
    db = st.session_state.crm_db
    search_query = st.text_input("🔍 Быстрый поиск по ФИО, телефону или ребенку:")
    
    filtered_db = db.copy()
    if search_query:
        filtered_db = filtered_db[
            filtered_db["ФИО Родителя"].str.contains(search_query, case=False) | 
            filtered_db["Телефон"].str.contains(search_query) |
            filtered_db["Ребенок"].str.contains(search_query, case=False)
        ]
    
    # Отображение таблицы
    st.dataframe(filtered_db, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Две колонки: Добавление и Изменение
    col_add, col_edit = st.columns(2)

    with col_add:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.subheader("➕ Добавить нового родителя")
        with st.form("add_form", clear_on_submit=True):
            name = st.text_input("ФИО Родителя*")
            phone = st.text_input("Телефон*")
            child = st.text_input("Имя ребенка")
            
            olymp = st.selectbox("Олимпиады", ["Не участвовал", "Заявка", "Участвовал"])
            tour = st.selectbox("Туры (Гарвард)", ["Не интересовался", "Интересуется", "Оплатил", "Участвовал"])
            courses = st.selectbox("Языковые курсы", ["Нет", "Тестирование", "Обучается", "Архив"])
            notes = st.text_area("Комментарий / Заметки")
            
            if st.form_submit_button("Создать запись"):
                if name and phone:
                    new_row = {
                        "ФИО Родителя": name, "Телефон": phone, "Ребенок": child,
                        "Олимпиады": olymp, "Туры (Гарвард)": tour, "Курсы": courses,
                        "Заметки": notes,
                        "Изменил(а)": st.session_state.user_name, # Авто-подпись!
                        "Дата": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.crm_db = pd.concat([db, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"Запись добавления подписана: {st.session_state.user_name}")
                    st.rerun()
                else:
                    st.error("Заполните ФИО и Телефон!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_edit:
        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.subheader("📝 Быстрое обновление статуса")
        if not db.empty:
            parent_to_edit = st.selectbox("Выберите родителя для редактирования:", db["ФИО Родителя"].tolist())
            idx = db[db["ФИО Родителя"] == parent_to_edit].index[0]
            
            with st.form("edit_form"):
                st.write(f"Редактируем карточку: **{parent_to_edit}**")
                e_phone = st.text_input("Телефон", value=db.at[idx, "Телефон"])
                e_olymp = st.selectbox("Олимпиады", ["Не участвовал", "Заявка", "Участвовал"], index=["Не участвовал", "Заявка", "Участвовал"].index(db.at[idx, "Олимпиады"]))
                e_tour = st.selectbox("Туры (Гарвард)", ["Не интересовался", "Интересуется", "Оплатил", "Участвовал"], index=["Не интересовался", "Интересуется", "Оплатил", "Участвовал"].index(db.at[idx, "Туры (Гарвард)"]))
                e_courses = st.selectbox("Языковые курсы", ["Нет", "Тестирование", "Обучается", "Архив"], index=["Нет", "Тестирование", "Обучается", "Архив"].index(db.at[idx, "Курсы"]))
                e_notes = st.text_area("Заметки", value=db.at[idx, "Заметки"])
                
                if st.form_submit_button("Сохранить изменения"):
                    st.session_state.crm_db.at[idx, "Телефон"] = e_phone
                    st.session_state.crm_db.at[idx, "Олимпиады"] = e_olymp
                    st.session_state.crm_db.at[idx, "Туры (Гарвард)"] = e_tour
                    st.session_state.crm_db.at[idx, "Курсы"] = e_courses
                    st.session_state.crm_db.at[idx, "Заметки"] = e_notes
                    st.session_state.crm_db.at[idx, "Изменил(а)"] = st.session_state.user_name # Авто-подпись при обновлении!
                    st.session_state.crm_db.at[idx, "Дата"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.success("Данные обновлены!")
                    st.rerun()
        else:
            st.write("База данных пуста.")
        st.markdown('</div>', unsafe_allow_html=True)
