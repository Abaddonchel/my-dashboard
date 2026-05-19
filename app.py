import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Дашборд с Excel", layout="wide")
st.title("📊 Аналитический дашборд")

st.write("Загрузите Excel-файл, чтобы начать анализ.")

# Загрузка файла
uploaded_file = st.file_uploader("Выберите Excel-файл", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Чтение Excel-файла
        df = pd.read_excel(uploaded_file)

        st.success("Файл успешно загружен!")
        st.write(f"Размер данных: {df.shape[0]} строк, {df.shape[1]} столбцов")

        # Отображение первых строк
        st.subheader("Первые 10 строк данных")
        st.dataframe(df.head(10))

        # Показать типы данных
        st.subheader("Типы данных")
        st.write(df.dtypes)

        # Простая визуализация (если есть числовые столбцы)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            st.subheader("График по числовым столбцам")
            st.line_chart(df[numeric_cols])
        else:
            st.info("Нет числовых данных для построения графика.")

    except Exception as e:
        st.error(f"Ошибка при чтении файла: {e}")
else:
    st.info("Ожидание загрузки файла...")