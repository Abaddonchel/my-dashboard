import streamlit as st

st.title("🚚 Логистика")

if "df" in st.session_state:
    df = st.session_state.df
    st.write("### Данные по логистике")
    st.dataframe(df)
    
    if 'Срок_доставки' in df.columns:
        st.subheader("Средний срок доставки")
        avg_days = df['Срок_доставки'].mean()
        st.metric("Средний срок", f"{avg_days:.1f} дней")
    else:
        st.info("Нет данных о сроках доставки.")
else:
    st.info("Загрузите данные для анализа логистики.")