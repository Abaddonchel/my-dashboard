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

st.title("📈 Анализ продаж")

if "df" in st.session_state:
    df = st.session_state.df
    
    # === Анализ по Role (должности) ===
    if 'Column1.role' in df.columns:
        st.subheader("👥 Распределение сотрудников по ролям")
        role_counts = df['Column1.role'].value_counts().dropna()
        
        fig, ax = plt.subplots(figsize=(13, max(5.5, len(role_counts) * 0.32)))
        bars = ax.barh(range(len(role_counts)), role_counts.values, color=sns.color_palette("husl", len(role_counts)), 
                       edgecolor='white', linewidth=1.5)
        ax.set_yticks(range(len(role_counts)))
        ax.set_yticklabels(role_counts.index, fontsize=11)
        
        # Добавить значения и проценты
        for i, (bar, v) in enumerate(zip(bars, role_counts.values)):
            ax.text(v + 0.5, i, f'{int(v)} ({v/len(df)*100:.1f}%)', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel("Количество сотрудников", fontsize=11)
        ax.set_title("Распределение по ролям", fontsize=13, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.2)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Всего ролей", len(role_counts))
        with col2:
            st.metric("Самая популярная", role_counts.index[0])
        with col3:
            st.metric("Кол-во в топе", role_counts.iloc[0])
    
    st.divider()
    
    # === Анализ Grade (уровень) ===
    if 'Column1.grade' in df.columns:
        st.subheader("📊 Распределение по уровню (Grade)")
        grade_counts = df['Column1.grade'].value_counts().dropna()
        
        if len(grade_counts) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(range(len(grade_counts)), grade_counts.values, 
                         color=sns.color_palette("Set2", len(grade_counts)), 
                         edgecolor='white', linewidth=1.5)
            ax.set_xticks(range(len(grade_counts)))
            ax.set_xticklabels(grade_counts.index, rotation=45, ha='right', fontsize=11)
            
            # Добавить значения
            for bar, v in zip(bars, grade_counts.values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{int(v)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            ax.set_ylabel("Количество", fontsize=11)
            ax.set_title("Распределение по уровню (Grade)", fontsize=13, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.2)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
    
    st.divider()
    
    # === Анализ по CFO (подразделению) ===
    if 'Column1.cfo' in df.columns:
        st.subheader("🏢 Распределение по подразделениям (CFO)")
        cfo_counts = df['Column1.cfo'].value_counts().dropna()
        
        if len(cfo_counts) > 0:
            fig, ax = plt.subplots(figsize=(13, max(5.5, len(cfo_counts) * 0.32)))
            bars = ax.barh(range(len(cfo_counts)), cfo_counts.values, 
                          color=sns.color_palette("pastel", len(cfo_counts)), 
                          edgecolor='white', linewidth=1.5)
            ax.set_yticks(range(len(cfo_counts)))
            ax.set_yticklabels(cfo_counts.index, fontsize=11)
            
            # Добавить значения
            for i, (bar, v) in enumerate(zip(bars, cfo_counts.values)):
                ax.text(v + 0.5, i, f'{int(v)} ({v/len(df)*100:.1f}%)', va='center', fontsize=10, fontweight='bold')
            
            ax.set_xlabel("Количество сотрудников", fontsize=11)
            ax.set_title("Распределение по подразделениям", fontsize=13, fontweight='bold', pad=20)
            ax.grid(axis='x', alpha=0.2)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
    
    st.divider()
    st.subheader("📊 Таблица данных")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Загрузите данные на главной странице.")