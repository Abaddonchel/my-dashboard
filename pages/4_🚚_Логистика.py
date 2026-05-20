import streamlit as st
import pandas as pd

st.title("🚚 Логистика")

if "df" in st.session_state:
    df = st.session_state.df
    
    # Ищем столбцы с датами и сроками
    date_cols = df.select_dtypes(include="datetime64").columns.tolist()
    if not date_cols:
        # Или попробуем текстовые
        for col in df.columns:
            if "дата" in col.lower() or "date" in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols.append(col)
                except:
                    pass
    
    if date_cols:
        st.subheader("Временные метки")
        st.write(f"Найдены столбцы дат: {date_cols}")
        for col in date_cols:
            st.write(f"- {col}: от {df[col].min()} до {df[col].max()}")
    
    delay_col = None
    for col in df.columns:
        if "срок" in col.lower() or "дней" in col.lower() or "время" in col.lower():
            if df[col].dtype in ['int64', 'float64']:
                delay_col = col
                break
    
    if delay_col:
        avg_days = df[delay_col].mean()
        st.metric("Средний срок", f"{avg_days:.1f} дней")
        st.bar_chart(df[delay_col].value_counts())
    else:
        st.info("Нет явных столбцов со сроками доставки.")
    
    st.dataframe(df)
else:
    st.info("Загрузите данные для анализа.")