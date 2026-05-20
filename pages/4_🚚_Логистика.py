import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🚚 Логистика (Управление сроками)")

if "df" in st.session_state:
    df = st.session_state.df.copy()
    
    # Преобразуем даты
    date_cols_to_convert = ['Column1.hire_date', 'Column1.termination_date', 'Column1.status_change']
    for col in date_cols_to_convert:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    st.subheader("📅 Анализ временных сроков")
    
    # === Длительность занятости (для уволенных) ===
    if 'Column1.hire_date' in df.columns and 'Column1.termination_date' in df.columns:
        df['employment_duration'] = (df['Column1.termination_date'] - df['Column1.hire_date']).dt.days
        
        # Фильтруем только уволенных
        terminated = df[df['employment_duration'] > 0].copy()
        
        if len(terminated) > 0:
            st.subheader("⏱️ Длительность занятости (уволенные сотрудники)")
            
            avg_duration = terminated['employment_duration'].mean()
            min_duration = terminated['employment_duration'].min()
            max_duration = terminated['employment_duration'].max()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Средняя длительность", f"{avg_duration:.0f} дн")
            with col2:
                st.metric("Минимум", f"{min_duration:.0f} дн")
            with col3:
                st.metric("Максимум", f"{max_duration:.0f} дн")
            with col4:
                st.metric("Всего уволено", len(terminated))
            
            # Гистограмма длительности
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(terminated['employment_duration'], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_xlabel("Длительность занятости (дни)")
            ax.set_ylabel("Количество")
            ax.set_title("Распределение длительности занятости")
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
    
    # === Распределение по статусам и срокам ===
    if 'Column1.status' in df.columns and 'Column1.hire_date' in df.columns:
        st.subheader("📊 Статусы и сроки найма")
        
        status_counts = df['Column1.status'].value_counts().dropna()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        status_counts.plot(kind='bar', ax=ax, color=['green', 'red'])
        ax.set_ylabel("Количество")
        ax.set_title("Распределение по статусам")
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Сроки найма по статусам
        if 'Column1.hire_date' in df.columns:
            st.subheader("📅 Динамика по статусам")
            
            for status in df['Column1.status'].unique():
                if pd.notna(status):
                    status_df = df[df['Column1.status'] == status]
                    hires = status_df['Column1.hire_date'].dropna().dt.to_period('M').value_counts().sort_index()
                    
                    if len(hires) > 0:
                        st.write(f"**{status}**: {len(status_df)} сотрудников")
    
    # === Информация о датах ===
    st.subheader("📋 Информация об основных датах")
    
    col_info = {}
    for col in ['Column1.hire_date', 'Column1.termination_date', 'Column1.status_change']:
        if col in df.columns:
            valid_dates = df[col].dropna()
            if len(valid_dates) > 0:
                col_info[col] = {
                    'min': valid_dates.min(),
                    'max': valid_dates.max(),
                    'count': len(valid_dates)
                }
    
    for col, info in col_info.items():
        st.write(f"**{col}:**")
        st.write(f"  - От {info['min']} до {info['max']}")
        st.write(f"  - Заполнено: {info['count']} значений")
    
    st.subheader("📊 Таблица данных")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Загрузите данные для анализа.")