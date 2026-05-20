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
    st.subheader("📊 Распределение по категориям")
    cat_cols = [col for col in df.columns if df[col].dtype == 'object']
    selected_col = st.selectbox("Выберите столбец для анализа", cat_cols, index=cat_cols.index('Column1.role') if 'Column1.role' in cat_cols else 0)
    
    if selected_col:
        value_counts = df[selected_col].value_counts().dropna()
        
        # Используем matplotlib для лучшего контроля
        fig, ax = plt.subplots(figsize=(10, max(5, len(value_counts) * 0.3)))
        value_counts.plot(kind='barh', ax=ax, color='steelblue')
        ax.set_xlabel("Количество")
        ax.set_ylabel(selected_col)
        ax.set_title(f"Распределение по {selected_col}")
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
        
        # Статистика
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Всего значений", len(value_counts))
        with col2:
            st.metric("Самое частое", value_counts.index[0])
        with col3:
            st.metric("Кол-во для топ значения", value_counts.iloc[0])

    # === 2. Распределение по Stack ===
    if 'Column1.stack' in df.columns:
        st.subheader("💻 Распределение по стеку")
        stack_counts = df['Column1.stack'].value_counts().dropna()
        
        fig, ax = plt.subplots(figsize=(10, max(5, len(stack_counts) * 0.3)))
        stack_counts.plot(kind='barh', ax=ax, color='mediumpurple')
        ax.set_xlabel("Количество сотрудников")
        ax.set_title("Разработчики по технологическому стеку")
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)

    # === 3. Наймы по датам ===
    if 'Column1.hire_date' in df.columns:
        st.subheader("📅 Динамика найма по датам")
        
        # Линейная диаграмма нарастающего числа наймов
        hires_by_date = df['Column1.hire_date'].dropna().dt.to_period('M').value_counts().sort_index()
        hires_by_date.index = hires_by_date.index.astype(str)
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(range(len(hires_by_date)), hires_by_date.values, marker='o', linewidth=2, markersize=6, color='green')
        ax.set_xticks(range(len(hires_by_date)))
        ax.set_xticklabels(hires_by_date.index, rotation=45, ha='right')
        ax.set_ylabel("Количество нанятых")
        ax.set_title("Количество нанятых сотрудников по месяцам")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    # === 4. Кросс-анализ Stack vs Role ===
    if 'Column1.stack' in df.columns and 'Column1.role' in df.columns:
        st.subheader("🔗 Связь между Stack и Role")
        
        crosstab = pd.crosstab(df['Column1.role'].dropna(), df['Column1.stack'].dropna())
        
        fig, ax = plt.subplots(figsize=(10, max(6, len(crosstab) * 0.3)))
        crosstab.plot(kind='barh', ax=ax, stacked=False)
        ax.set_xlabel("Количество")
        ax.set_title("Распределение Role по Stack")
        ax.legend(title='Stack', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)

    # === 5. Кросс-анализ Stack vs Hire Date (по годам) ===
    if 'Column1.stack' in df.columns and 'Column1.hire_date' in df.columns:
        st.subheader("📈 Найм по Stack и году")
        
        df_temp = df.copy()
        df_temp['hire_year'] = df_temp['Column1.hire_date'].dt.year
        
        crosstab_year = pd.crosstab(df_temp['hire_year'].dropna(), df_temp['Column1.stack'].dropna())
        
        fig, ax = plt.subplots(figsize=(10, 5))
        crosstab_year.plot(kind='bar', ax=ax)
        ax.set_xlabel("Год найма")
        ax.set_ylabel("Количество")
        ax.set_title("Найм по технологическому стеку по годам")
        ax.legend(title='Stack')
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # === 6. Таблица данных ===
    st.subheader("📋 Исходные данные")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Загрузите данные на главной странице.")