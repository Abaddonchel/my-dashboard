import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("📊 Отчёты")

if "df" in st.session_state:
    df = st.session_state.df

    # === Преобразуем даты ===
    if 'Column1.hire_date' in df.columns:
        df['Column1.hire_date'] = pd.to_datetime(df['Column1.hire_date'], errors='coerce')

    # === 1. Выбор столбца для гистограммы ===
    st.subheader("Распределение по категориям")
    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    selected_col = st.selectbox("Выберите столбец для анализа", cat_cols)
    
    if selected_col:
        value_counts = df[selected_col].value_counts().dropna()
        st.bar_chart(value_counts)

    # === 2. Распределение по Stack ===
    if 'Column1.stack' in df.columns:
        st.subheader("Распределение по стеку")
        stack_counts = df['Column1.stack'].value_counts().dropna()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        stack_counts.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_xlabel("Количество")
        ax.set_title("Разработчики по стеку")
        st.pyplot(fig)

    # === 3. Наймы по датам ===
    if 'Column1.hire_date' in df.columns:
        st.subheader("Наймы по датам")
        hires_by_date = df['Column1.hire_date'].dropna().dt.to_period('M').value_counts().sort_index()
        hires_by_date.index = hires_by_date.index.astype(str)
        
        st.line_chart(hires_by_date)

    # === 4. Таблица данных ===
    st.subheader("Данные")
    st.dataframe(df)
else:
    st.info("Загрузите данные на главной странице.")