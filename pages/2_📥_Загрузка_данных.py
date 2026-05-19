import streamlit as st

st.title("📥 Загрузка данных из Google Sheets")

if "sheet_id" in st.session_state:
    st.success(f"Текущая таблица: {st.session_state.selected_table}")
    st.write(f"ID: `{st.session_state.sheet_id}`")
    if "df" in st.session_state:
        st.dataframe(st.session_state.df)
else:
    st.info("Данные ещё не загружены. Выберите таблицу на главной странице.")

st.markdown("---")
st.write("*Здесь можно добавить ручную перезагрузку или смену таблицы.*")