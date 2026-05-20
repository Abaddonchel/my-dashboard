import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import warnings
warnings.filterwarnings('ignore')

# === НАСТРОЙКА СТИЛЯ ===
st.set_page_config(page_title="Отчёты", layout="wide")
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Параметры matplotlib для современного вида
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.edgecolor': '#e0e0e0',
    'axes.linewidth': 0.8,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'font.size': 10,
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
})

st.title("📊 Отчёты")

# Инициализация session_state
if 'filter_applied' not in st.session_state:
    st.session_state.filter_applied = False
if 'export_count' not in st.session_state:
    st.session_state.export_count = 0

if "df" in st.session_state:
    df = st.session_state.df.copy()

    # === SIDEBAR ФИЛЬТРЫ И ПАРАМЕТРЫ ===
    with st.sidebar:
        st.header("🔧 Параметры и фильтры")
        
        # Фильтр по статусу
        if 'Column1.status' in df.columns:
            statuses = ['Все'] + df['Column1.status'].dropna().unique().tolist()
            selected_status = st.selectbox("Статус сотрудника", statuses)
            if selected_status != 'Все':
                df = df[df['Column1.status'] == selected_status]
                st.session_state.filter_applied = True
        
        # Фильтр по Stack
        if 'Column1.stack' in df.columns:
            stacks = ['Все'] + df['Column1.stack'].dropna().unique().tolist()
            selected_stack = st.selectbox("Технологический стек", stacks)
            if selected_stack != 'Все':
                df = df[df['Column1.stack'] == selected_stack]
                st.session_state.filter_applied = True
        
        # Фильтр по Role
        if 'Column1.role' in df.columns:
            roles = ['Все'] + df['Column1.role'].dropna().unique().tolist()
            selected_role = st.selectbox("Роль/Должность", roles)
            if selected_role != 'Все':
                df = df[df['Column1.role'] == selected_role]
                st.session_state.filter_applied = True
        
        st.divider()
        
        # Параметры визуализации
        st.subheader("⚙️ Параметры графиков")
        chart_style = st.radio("Стиль диаграмм", ["Вертикальные", "Горизонтальные"])
        show_values = st.checkbox("Показывать значения", value=True)
        color_scheme = st.selectbox("Цветовая схема", ["Классика", "Яркая", "Пастель"])
        
        st.divider()
        
        # Индикатор фильтрации
        if st.session_state.filter_applied:
            st.success(f"✅ Фильтры применены\n📊 Строк: {len(df)}")
        
        # Кнопки действий
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Сброс", use_container_width=True):
                st.session_state.filter_applied = False
                st.rerun()
        with col2:
            if st.button("💾 Экспорт", use_container_width=True):
                st.session_state.export_count += 1

    # === ВЫБОР ЦВЕТОВОЙ СХЕМЫ ===
    color_map = {
        "Классика": sns.color_palette("Set2", 4),
        "Яркая": sns.color_palette("husl", 4),
        "Пастель": sns.color_palette("pastel", 4)
    }
    colors = color_map[color_scheme]
    
    # === ФУНКЦИЯ СТИЛИЗАЦИИ ГРАФИКОВ ===
    def style_plot(ax, title="", xlabel="", ylabel=""):
        """Применить единый современный стиль к графику"""
        ax.set_title(title, fontsize=13, fontweight='bold', pad=20)
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=11)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=11)
        ax.tick_params(labelsize=10)
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        for spine in ax.spines.values():
            spine.set_edgecolor('#e0e0e0')
        return ax

    # === МЕТРИКИ В ШАПКЕ ===
    st.subheader("📈 Ключевые метрики")
    metric_cols = st.columns(5)
    
    with metric_cols[0]:
        st.metric("👥 Всего", len(df))
    
    with metric_cols[1]:
        active_count = len(df[df['Column1.status'] == 'Активный']) if 'Column1.status' in df.columns else 0
        percentage = (active_count / len(df) * 100) if len(df) > 0 else 0
        st.metric("✅ Активных", f"{active_count} ({percentage:.0f}%)")
    
    with metric_cols[2]:
        terminated_count = len(df[df['Column1.status'] == 'Уволен']) if 'Column1.status' in df.columns else 0
        st.metric("❌ Уволено", terminated_count)
    
    with metric_cols[3]:
        if 'Column1.grade' in df.columns:
            lead_count = len(df[df['Column1.grade'].str.contains('Lead', case=False, na=False)])
            st.metric("👨‍💼 Lead", lead_count)
    
    with metric_cols[4]:
        if 'Column1.hire_date' in df.columns:
            df['Column1.hire_date'] = pd.to_datetime(df['Column1.hire_date'], errors='coerce')
            recent = len(df[df['Column1.hire_date'] > pd.Timestamp.now() - pd.DateOffset(months=3)])
            st.metric("🆕 За 3мес", recent)

    st.divider()

    # === ВКЛАДКИ ===
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Категории", "💻 Стек", "📅 Найм", "🔗 Кросс", "📈 Статистика", "📋 Таблица"
    ])

    # TAB 1: Выбор столбца
    with tab1:
        st.subheader("Анализ категориальных данных")
        
        cat_cols = [col for col in df.columns if df[col].dtype == 'object']
        
        if cat_cols:
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                selected_col = st.selectbox("Выберите столбец", cat_cols, 
                    index=cat_cols.index('Column1.role') if 'Column1.role' in cat_cols else 0, key="tab1")
            
            with col_right:
                min_items = st.slider("Min элементов", 1, 20, 1)
            
            if selected_col:
                value_counts = df[selected_col].value_counts().dropna()
                value_counts = value_counts[value_counts >= min_items]
                
                if len(value_counts) > 0:
                    chart_type = st.radio("Тип", ["Горизонтальная", "Вертикальная", "Круговая"], horizontal=True, key="tab1_chart")
                    
                    if chart_type == "Горизонтальная":
                        fig, ax = plt.subplots(figsize=(13, max(5, len(value_counts) * 0.28)))
                        bars = ax.barh(range(len(value_counts)), value_counts.values, color=colors[0], edgecolor='white', linewidth=1.5)
                        ax.set_yticks(range(len(value_counts)))
                        ax.set_yticklabels(value_counts.index, fontsize=10)
                        
                        # Добавить значения на бары
                        if show_values:
                            for i, (bar, v) in enumerate(zip(bars, value_counts.values)):
                                ax.text(v + 0.5, i, f'{int(v)}', va='center', fontsize=9, fontweight='bold')
                        
                        style_plot(ax, title=f"Распределение {selected_col}", xlabel="Количество")
                        fig.tight_layout()
                    
                    elif chart_type == "Вертикальная":
                        fig, ax = plt.subplots(figsize=(13, 6))
                        bars = ax.bar(range(len(value_counts)), value_counts.values, color=colors[0], edgecolor='white', linewidth=1.5)
                        ax.set_xticks(range(len(value_counts)))
                        ax.set_xticklabels(value_counts.index, rotation=45, ha='right', fontsize=10)
                        
                        # Добавить значения на бары
                        if show_values:
                            for bar, v in zip(bars, value_counts.values):
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                                       f'{int(v)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
                        
                        style_plot(ax, title=f"Распределение {selected_col}", ylabel="Количество")
                        fig.tight_layout()
                    
                    else:  # Круговая
                        fig, ax = plt.subplots(figsize=(11, 8))
                        wedges, texts, autotexts = ax.pie(value_counts, labels=value_counts.index, 
                                                           autopct='%1.1f%%', startangle=90,
                                                           colors=colors, textprops={'fontsize': 10})
                        for autotext in autotexts:
                            autotext.set_color('white')
                            autotext.set_fontweight('bold')
                            autotext.set_fontsize(10)
                        ax.set_title(f"Распределение {selected_col}", fontsize=13, fontweight='bold', pad=20)
                        fig.tight_layout()
                    
                    st.pyplot(fig, use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Уникальных", len(value_counts))
                    with col2:
                        st.metric("Топ", f"{value_counts.index[0]}")
                    with col3:
                        st.metric("Среднее", f"{value_counts.mean():.1f}")

    # TAB 2: Stack
    with tab2:
        st.subheader("Анализ стека технологий")
        
        if 'Column1.stack' in df.columns:
            stack_counts = df['Column1.stack'].value_counts().dropna()
            
            if len(stack_counts) > 0:
                fig, ax = plt.subplots(figsize=(13, max(5.5, len(stack_counts) * 0.32)))
                bars = ax.barh(range(len(stack_counts)), stack_counts.values, color=colors[1], edgecolor='white', linewidth=1.5)
                ax.set_yticks(range(len(stack_counts)))
                ax.set_yticklabels(stack_counts.index, fontsize=11)
                
                if show_values:
                    for i, (bar, v) in enumerate(zip(bars, stack_counts.values)):
                        ax.text(v + 0.5, i, f'{int(v)} ({v/len(df)*100:.1f}%)', va='center', fontsize=10, fontweight='bold')
                
                style_plot(ax, title="Распределение по технологическому стеку", xlabel="Количество сотрудников")
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                fig.tight_layout()
                
                st.pyplot(fig, use_container_width=True)
                
                st.divider()
                # Текстовая статистика в две колонки
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Всего стеков", len(stack_counts))
                    st.metric("Самый популярный", stack_counts.index[0])
                with col2:
                    st.metric("В самом популярном", f"{stack_counts.iloc[0]} ({stack_counts.iloc[0]/len(df)*100:.1f}%)")
                    st.metric("Среднее на стек", f"{stack_counts.mean():.1f}")

    # TAB 3: Найм
    with tab3:
        st.subheader("Анализ найма по датам")
        
        if 'Column1.hire_date' in df.columns:
            df['Column1.hire_date'] = pd.to_datetime(df['Column1.hire_date'], errors='coerce')
            
            period = st.radio("Период", ["Месяцам", "Кварталам", "Годам"], horizontal=True, key="tab3_period")
            
            if period == "Месяцам":
                hires = df['Column1.hire_date'].dropna().dt.to_period('M').value_counts().sort_index()
            elif period == "Кварталам":
                hires = df['Column1.hire_date'].dropna().dt.to_period('Q').value_counts().sort_index()
            else:
                hires = df['Column1.hire_date'].dropna().dt.to_period('Y').value_counts().sort_index()
            
            hires_labels = hires.index.astype(str)
            
            fig, ax = plt.subplots(figsize=(15, 6))
            
            # Линия графика
            line = ax.plot(range(len(hires)), hires.values, marker='o', linewidth=3.5, 
                          markersize=10, color=colors[2], markerfacecolor='white', 
                          markeredgewidth=2.5, markeredgecolor=colors[2], label='Найм')
            
            # Заполнение под линией
            ax.fill_between(range(len(hires)), hires.values, alpha=0.15, color=colors[2])
            
            # Улучшенное форматирование оси X
            ax.set_xticks(range(len(hires)))
            ax.set_xticklabels(hires_labels, rotation=45, ha='right', fontsize=11)
            
            style_plot(ax, title=f"Динамика найма по {period.lower()}", ylabel="Количество нанятых")
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            
            # Добавить значения на точки
            if show_values:
                for i, v in enumerate(hires.values):
                    ax.text(i, v + 0.8, f'{int(v)}', ha='center', va='bottom', 
                           fontsize=10, fontweight='bold', color=colors[2])
            
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            
            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Всего нанято", len(df['Column1.hire_date'].dropna()))
            with col2:
                st.metric("Пиковый период", hires.idxmax())
            with col3:
                st.metric("Макс в период", int(hires.max()))
            with col4:
                st.metric("Среднее", f"{hires.mean():.1f}")

    # TAB 4: Кросс-анализ
    with tab4:
        st.subheader("Кросс-анализ")
        
        analysis = st.radio("Тип", ["Stack vs Role", "Role vs Grade", "Status vs Stack"], horizontal=True, key="tab4_type")
        
        if analysis == "Stack vs Role" and 'Column1.stack' in df.columns and 'Column1.role' in df.columns:
            crosstab = pd.crosstab(df['Column1.role'].dropna(), df['Column1.stack'].dropna())
            fig, ax = plt.subplots(figsize=(13, max(5.5, len(crosstab) * 0.32)))
            crosstab.plot(kind='barh', ax=ax, color=colors, edgecolor='white', linewidth=1.5)
            ax.set_xlabel("Количество", fontsize=11)
            ax.set_ylabel("Role", fontsize=11)
            ax.set_title("Распределение ролей по технологическому стеку", fontsize=13, fontweight='bold', pad=20)
            ax.legend(title='Stack', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
            ax.grid(axis='x', alpha=0.2)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        elif analysis == "Role vs Grade" and 'Column1.role' in df.columns and 'Column1.grade' in df.columns:
            crosstab = pd.crosstab(df['Column1.role'].dropna(), df['Column1.grade'].dropna())
            fig, ax = plt.subplots(figsize=(13, 6))
            crosstab.plot(kind='bar', ax=ax, stacked=True, color=colors, edgecolor='white', linewidth=1.5)
            ax.set_ylabel("Количество", fontsize=11)
            ax.set_xlabel("Role", fontsize=11)
            ax.set_title("Распределение уровней (Grade) по ролям", fontsize=13, fontweight='bold', pad=20)
            ax.legend(title='Grade', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
            ax.grid(axis='y', alpha=0.2)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.xticks(rotation=45, ha='right', fontsize=10)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        elif analysis == "Status vs Stack" and 'Column1.status' in df.columns and 'Column1.stack' in df.columns:
            crosstab = pd.crosstab(df['Column1.status'].dropna(), df['Column1.stack'].dropna())
            fig, ax = plt.subplots(figsize=(13, 6))
            crosstab.plot(kind='bar', ax=ax, color=colors, edgecolor='white', linewidth=1.5)
            ax.set_ylabel("Количество", fontsize=11)
            ax.set_xlabel("Статус", fontsize=11)
            ax.set_title("Распределение статусов по технологическому стеку", fontsize=13, fontweight='bold', pad=20)
            ax.legend(title='Stack', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
            ax.grid(axis='y', alpha=0.2)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.xticks(rotation=45, ha='right', fontsize=10)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)

    # TAB 5: Статистика
    with tab5:
        st.subheader("Статистика")
        
        stat_type = st.selectbox("Тип", ["Числовые данные", "Сводная таблица", "Корреляции"], key="tab5_select")
        
        if stat_type == "Числовые данные":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                selected_num = st.selectbox("Столбец", numeric_cols, key="tab5_num")
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                # Гистограмма
                ax1.hist(df[selected_num].dropna(), bins=20, color=colors[0], edgecolor='white', linewidth=1.5, alpha=0.8)
                style_plot(ax1, title=f"Распределение {selected_num}", xlabel="Значение", ylabel="Частота")
                ax1.grid(axis='y', alpha=0.2)
                
                # Box plot
                bp = ax2.boxplot(df[selected_num].dropna(), vert=True, patch_artist=True,
                               boxprops=dict(facecolor=colors[1], alpha=0.7, edgecolor='white', linewidth=1.5),
                               whiskerprops=dict(color='#555', linewidth=1.5),
                               capprops=dict(color='#555', linewidth=1.5),
                               medianprops=dict(color='white', linewidth=2))
                style_plot(ax2, title=f"Box plot {selected_num}", ylabel="Значение")
                ax2.grid(axis='y', alpha=0.2)
                
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Среднее", f"{df[selected_num].mean():.2f}")
                with col2:
                    st.metric("Медиана", f"{df[selected_num].median():.2f}")
                with col3:
                    st.metric("Мин", f"{df[selected_num].min():.2f}")
                with col4:
                    st.metric("Макс", f"{df[selected_num].max():.2f}")
        
        elif stat_type == "Сводная таблица":
            st.write("**Описательная статистика:**")
            st.dataframe(df.describe().T, use_container_width=True)
        
        elif stat_type == "Корреляции":
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr = numeric_df.corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                im = ax.imshow(corr, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
                ax.set_xticks(range(len(corr.columns)))
                ax.set_yticks(range(len(corr.columns)))
                ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=10)
                ax.set_yticklabels(corr.columns, fontsize=10)
                
                # Добавить значения корреляции в ячейки
                for i in range(len(corr.columns)):
                    for j in range(len(corr.columns)):
                        text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                                     ha="center", va="center", color="black", fontsize=9, fontweight='bold')
                
                cbar = plt.colorbar(im, ax=ax)
                cbar.set_label('Корреляция', fontsize=10)
                ax.set_title("Матрица корреляций", fontsize=13, fontweight='bold', pad=20)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("Недостаточно числовых столбцов")

    # TAB 6: Таблица
    with tab6:
        st.subheader("Таблица данных")
        
        col_search, col_sort = st.columns([2, 1])
        
        with col_search:
            search_term = st.text_input("🔍 Поиск", "", placeholder="Введите текст для поиска...")
        
        with col_sort:
            if len(df.columns) > 0:
                sort_col = st.selectbox("Сортировка по", df.columns, key="tab6_sort")
            else:
                sort_col = None
        
        if search_term:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            df_display = df[mask]
            st.success(f"✅ Найдено {len(df_display)} результатов из {len(df)}")
        else:
            df_display = df
        
        if sort_col:
            df_display = df_display.sort_values(by=sort_col, ascending=True)
        
        st.dataframe(df_display, use_container_width=True, height=500)
        
        st.divider()
        
        if st.button("📥 Скачать CSV", use_container_width=True, type="primary"):
            csv = df_display.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Загрузить файл",
                data=csv,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

else:
    st.info("👈 Загрузите данные на главной странице")