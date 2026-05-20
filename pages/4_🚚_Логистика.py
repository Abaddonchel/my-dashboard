import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import warnings
warnings.filterwarnings('ignore')

# === НАСТРОЙКА СТИЛЯ ===
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.edgecolor': '#e0e0e0',
    'axes.linewidth': 0.8,
    'grid.alpha': 0.3,
    'font.size': 10,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

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
            fig, ax = plt.subplots(figsize=(13, 6))
            ax.hist(terminated['employment_duration'], bins=25, color=sns.color_palette("husl", 1)[0], 
                   edgecolor='white', linewidth=1.5, alpha=0.8)
            ax.set_xlabel("Длительность занятости (дни)", fontsize=11)
            ax.set_ylabel("Количество", fontsize=11)
            ax.set_title("Распределение длительности занятости", fontsize=13, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.2)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
    
    # === Распределение по статусам и срокам ===
    if 'Column1.status' in df.columns and 'Column1.hire_date' in df.columns:
        st.subheader("📊 Статусы и сроки найма")
        
        status_counts = df['Column1.status'].value_counts().dropna()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_status = sns.color_palette("Set2", len(status_counts))
        bars = ax.bar(range(len(status_counts)), status_counts.values, color=colors_status, 
                     edgecolor='white', linewidth=1.5)
        ax.set_xticks(range(len(status_counts)))
        ax.set_xticklabels(status_counts.index, fontsize=11)
        ax.set_ylabel("Количество", fontsize=11)
        ax.set_title("Распределение по статусам", fontsize=13, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.2)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # Добавить значения
        for bar, v in zip(bars, status_counts.values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{int(v)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        # Сроки найма по статусам
        if 'Column1.hire_date' in df.columns:
            st.subheader("📅 Статистика по статусам")
            
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
    
    if col_info:
        cols = st.columns(len(col_info))
        for idx, (col, info) in enumerate(col_info.items()):
            with cols[idx]:
                col_name = col.split('.')[-1].replace('_', ' ').title()
                st.metric(
                    col_name,
                    f"{info['count']}",
                    delta=f"От {info['min'].strftime('%d.%m.%Y')} до {info['max'].strftime('%d.%m.%Y')}"
                )
    
    st.divider()
    st.subheader("📊 Таблица данных")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Загрузите данные для анализа.")