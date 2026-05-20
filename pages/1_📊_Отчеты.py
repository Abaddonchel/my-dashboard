import streamlit as st
import pandas as pd

st.title("📊 Отчёты")

if "df" in st.session_state:
    df = st.session_state.df
    st.write("### Данные")
    st.dataframe(df)

    # Авто-график по числовым столбцам
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        st.write("### Линейный график")
        st.line_chart(df.set_index(df.columns[0]) if df.dtypes.iloc[0] not in ['int64', 'float64'] else df[numeric_cols])
    
    # Гистограммы
    st.write("### Гистограммы")
    for col in numeric_cols:
        st.write(f"**{col}**")
        st.bar_chart(df[col])
else:
    st.info("Загрузите данные на главной странице.")