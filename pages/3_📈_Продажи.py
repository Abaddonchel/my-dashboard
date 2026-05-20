import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Анализ продаж")

if "df" in st.session_state:
    df = st.session_state.df
    
    # Попробуем угадать столбцы
    sales_col = None
    for col in df.columns:
        if "продаж" in col.lower() or "выручка" in col.lower() or "доход" in col.lower():
            sales_col = col
            break
    
    if sales_col:
        st.subheader("Общие продажи")
        st.line_chart(df[sales_col])

        # Группировка по первому нечисловому столбцу (например, категория, регион)
        cat_col = None
        for col in df.columns:
            if df[col].dtype == "object" and col != sales_col:
                cat_col = col
                break
        
        if cat_col:
            st.subheader(f"Продажи по {cat_col}")
            grouped = df.groupby(cat_col)[sales_col].sum()
            fig, ax = plt.subplots()
            grouped.plot(kind='bar', ax=ax)
            st.pyplot(fig)
    else:
        st.warning("Не найден столбец с продажами. Попробуйте страницу \"Отчёты\".")
else:
    st.info("Загрузите данные на главной странице.")