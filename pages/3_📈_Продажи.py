import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Анализ продаж")

if "df" in st.session_state:
    df = st.session_state.df
    
    st.subheader("📊 Анализ распределения по ролям и компетенциям")
    
    # === Анализ по Role (должности) ===
    if 'Column1.role' in df.columns:
        st.subheader("Распределение сотрудников по ролям")
        role_counts = df['Column1.role'].value_counts().dropna()
        
        fig, ax = plt.subplots(figsize=(10, max(5, len(role_counts) * 0.3)))
        role_counts.plot(kind='barh', ax=ax, color='coral')
        ax.set_xlabel("Количество сотрудников")
        ax.set_title("Распределение по ролям")
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
        
        st.metric("Всего ролей", len(role_counts))
        st.metric("Самая популярная роль", f"{role_counts.index[0]} ({role_counts.iloc[0]} чел.)")
    
    # === Анализ Grade (уровень) ===
    if 'Column1.grade' in df.columns:
        st.subheader("Распределение по уровню (Grade)")
        grade_counts = df['Column1.grade'].value_counts().dropna()
        
        if len(grade_counts) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            grade_counts.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_ylabel("Количество")
            ax.set_title("Распределение по Grade")
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    # === Анализ по CFO (подразделению) ===
    if 'Column1.cfo' in df.columns:
        st.subheader("Распределение по подразделениям (CFO)")
        cfo_counts = df['Column1.cfo'].value_counts().dropna()
        
        if len(cfo_counts) > 0:
            fig, ax = plt.subplots(figsize=(10, max(5, len(cfo_counts) * 0.3)))
            cfo_counts.plot(kind='barh', ax=ax, color='lightgreen')
            ax.set_xlabel("Количество сотрудников")
            ax.set_title("Распределение по подразделениям")
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("Загрузите данные на главной странице.")