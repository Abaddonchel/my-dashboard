import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
import json

# Настройка страницы
st.set_page_config(page_title="Google Sheets Дашборд", layout="wide")
st.title("📊 Аналитика из Google Таблицы")

# Попробуем загрузить секреты: сначала st.secrets, потом .env
try:
    # 1. Попробуем получить из st.secrets (Streamlit Cloud)
    client_email = st.secrets["GOOGLE_SHEETS_CLIENT_EMAIL"]
    private_key = st.secrets["GOOGLE_SHEETS_PRIVATE_KEY"]
    st.write("🔑 Секреты загружены из `st.secrets` (например, Streamlit Cloud)")
except KeyError:
    # 2. Если нет — загружаем из .env (локально)
    load_dotenv()
    client_email = os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL")
    private_key = os.getenv("GOOGLE_SHEETS_PRIVATE_KEY")
    if client_email and private_key:
        st.write("🔑 Секреты загружены из `.env` (локально)")
    else:
        st.error("❌ Не найдены секреты ни в `st.secrets`, ни в `.env`.")
        st.stop()

@st.cache_resource
def connect_to_google_sheets():
    """Создаёт подключение к Google Sheets"""
    try:
        # Очищаем ключ
        private_key_clean = private_key.strip("'").strip('"').replace('\\n', '\n')

        # Создаём учётные данные
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
        client = gspread.authorize(credentials)
        st.success("✅ Подключено к Google Sheets")
        return client
    except Exception as e:
        st.error(f"❌ Ошибка аутентификации: {e}")
        return None

@st.cache_data(ttl=600)
def load_data_from_sheet(sheet_id: str, sheet_name: str = None):
    """Загружает данные из Google Таблицы"""
    client = connect_to_google_sheets()
    if not client:
        return None
    
    try:
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(sheet_name) if sheet_name else sheet.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ Ошибка чтения таблицы: {e}")
        return None

# Ввод ID таблицы
sheet_id = st.text_input(
    "Введите ID Google Таблицы", 
    placeholder="1aBcD...eFgH"
)

if sheet_id:
    sheet_name = st.text_input("Имя листа (опционально)", "Лист1")
    
    with st.spinner("Загружаем данные..."):
        df = load_data_from_sheet(sheet_id, sheet_name if sheet_name else None)
    
    if df is not None and not df.empty:
        st.success(f"Загружено {len(df)} строк")
        st.dataframe(df)
        
        # Пример визуализации
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.subheader("График")
            st.line_chart(df.set_index(df.columns[0]) if df.columns[0] not in numeric_cols else df[numeric_cols])
    else:
        st.info("Таблица пуста или не найдена.")
else:
    st.info("Введите ID таблицы выше.")