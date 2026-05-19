import streamlit as st
import pandas as pd

st.title("Мой BI Dashboard")

df = pd.DataFrame({
    "Имя": ["Анна", "Иван"],
    "Часы": [40, 35]
})

st.dataframe(df)

st.bar_chart(df.set_index("Имя"))