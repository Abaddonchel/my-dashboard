import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

# === Отладка: покажем структуру проекта ===
st.write("🔍 Отладка: файлы в проекте")

# Покажем, что видно в корне
root_files = os.listdir(".")
st.write("📂 Корневые файлы:", root_files)

# Покажем, есть ли папка `pages`
if "pages" in root_files:
    page_files = os.listdir("pages")
    st.write("📄 Файлы в `pages/`:", page_files)
else:
    st.warning("❌ Папка `pages/` не найдена!")

st.markdown("---")

# Кнопки навигации (временно)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Главная"):
        st.rerun()
with col2:
    if st.button("📊 Отчёты"):
        st.markdown("[Перейти](/pages/1_%F0%9F%93%8A_%D0%9E%D1%82%D1%87%D0%B5%D1%82%D1%8B.py)")
        st.stop()
with col3:
    if st.button("📥 Загрузка"):
        st.markdown("[Перейти](/pages/2_%F0%9F%93%A5_%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.py)")
        st.stop()
with col4:
    if st.button("📈 Продажи"):
        st.markdown("[Перейти](/pages/3_%F0%9F%93%88_%D0%9F%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D0%B8.py)")
        st.stop()

# Продолжение основного кода...

# Настройка страницы
st.set_page_config(page_title="Мой дашборд", layout="wide")
st.title("🏠 Главная панель")
st.write("Выберите таблицу и лист для анализа.")

# === Загрузка секретов ===
try:
    client_email = st.secrets["GOOGLE_SHEETS_CLIENT_EMAIL"]
    private_key = st.secrets["GOOGLE_SHEETS_PRIVATE_KEY"]
    table_config = st.secrets["tables"]
except KeyError as e:
    st.error(f"❌ Не найден секрет: {e}")
    st.stop()

@st.cache_resource
def connect_to_google_sheets():
    try:
        private_key_clean = private_key.strip("'").strip('"').replace('\\n', '\n')
        credentials_info = {
            "type": "service_account",
            "project_id": "your-project-id",
            "private_key_id": "none",
            "private_key": private_key_clean,
            "client_email": client_email,
            "client_id": "none",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email.replace('@', '%40')}"
        }
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        return gspread.authorize(credentials)
    except Exception as e:
        st.error(f"❌ Ошибка подключения: {e}")
        return None

# === Выбор таблицы ===
if table_config:
    table_names = list(table_config.keys())
    selected_table = st.selectbox("Выберите таблицу", table_names)
    sheet_id = table_config[selected_table]

    # === Получение листов ===
    client = connect_to_google_sheets()
    if client:
        try:
            sheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title for ws in sheet.worksheets()]
            selected_sheet = st.selectbox("Выберите лист", worksheet_names)
        except Exception as e:
            st.error(f"❌ Ошибка загрузки листов: {e}")
            st.stop()
    else:
        st.stop()

    if st.button("Загрузить данные"):
        with st.spinner("Чтение данных из Google Sheets..."):
            try:
                worksheet = sheet.worksheet(selected_sheet)
                data = worksheet.get_all_records()
                df = pd.DataFrame(data)
                
                # Сохраняем в session_state
                st.session_state.df = df
                st.session_state.sheet_id = sheet_id
                st.session_state.selected_table = selected_table
                
                st.success(f"✅ Загружено {len(df)} строк")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"❌ Ошибка чтения: {e}")
else:
    st.error("❌ Нет доступных таблиц в secrets.")

st.markdown("---")
st.write("👉 Перейдите на другие вкладки через меню слева (☰) или используйте кнопки выше.")