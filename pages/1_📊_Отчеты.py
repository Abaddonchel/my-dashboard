import streamlit as st
import pandas as pd

st.title("📊 Отчёты")
st.write("Эта страница показывает основные отчёты.")

# Подключение к Google Sheets (можно импортировать из основного app.py)
# Пока просто заглушка
if "df" in st.session_state:
    df = st.session_state.df
    st.dataframe(df)
    
    if df.select_dtypes(include="number").columns.tolist():
        st.line_chart(df.set_index(df.columns[0]) if df.dtypes.iloc[0] not in ['int64', 'float64'] else None)
else:
    st.info("Данные не загружены. Перейдите на вкладку \"Загрузка данных\".")