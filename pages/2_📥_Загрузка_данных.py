import streamlit as st

st.title("📥 Статус данных")

if "df" in st.session_state:
    df = st.session_state.df
    st.success(f"✅ Данные загружены: {len(df)} строк, {len(df.columns)} столбцов")
    st.write("**Источник:** Google Sheets")
    if "selected_table" in st.session_state:
        st.write(f"**Таблица:** {st.session_state.selected_table}")
    
    st.dataframe(df)
else:
    st.info("Данные не загружены. Перейдите на главную и нажмите \"Загрузить данные\".")