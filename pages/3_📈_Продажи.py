import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Анализ продаж")

if "df" in st.session_state:
    df = st.session_state.df
    
    # Предположим, что есть столбцы: 'Дата', 'Продажи', 'Регион'
    if 'Продажи' in df.columns:
        st.subheader("Общие продажи")
        st.bar_chart(df['Продажи'])
        
        if 'Регион' in df.columns:
            st.subheader("Продажи по регионам")
            region_sales = df.groupby('Регион')['Продажи'].sum()
            fig, ax = plt.subplots()
            region_sales.plot(kind='pie', ax=ax, title="Доля продаж по регионам")
            st.pyplot(fig)
    else:
        st.warning("Столбец 'Продажи' не найден в данных.")
else:
    st.info("Загрузите данные на вкладке \"Загрузка данных\".")