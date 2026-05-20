import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

st.set_page_config(page_title="Отчёты", layout="wide")
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
        "Классика": ['steelblue', 'mediumpurple', 'coral', 'lightgreen'],
        "Яркая": ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3'],
        "Пастель": ['#FFB3B3', '#B3D9FF', '#FFD9B3', '#D4FFB3']
    }
    colors = color_map[color_scheme]

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
                    
                    fig, ax = plt.subplots(figsize=(12, max(5, len(value_counts) * 0.25)))
                    
                    if chart_type == "Горизонтальная":
                        value_counts.plot(kind='barh', ax=ax, color=colors[0])
                        ax.set_xlabel("Количество")
                    elif chart_type == "Вертикальная":
                        value_counts.plot(kind='bar', ax=ax, color=colors[0])
                        ax.set_ylabel("Количество")
                        plt.xticks(rotation=45, ha='right')
                    else:
                        fig, ax = plt.subplots(figsize=(10, 8))
                        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
                        ax.set_title(f"Распределение {selected_col}")
                    
                    if chart_type != "Круговая":
                        ax.set_title(f"Распределение {selected_col}")
                        ax.grid(alpha=0.3)
                        if show_values:
                            for i, v in enumerate(value_counts):
                                if chart_type == "Горизонтальная":
                                    ax.text(v, i, f' {v}', va='center')
                    
                    st.pyplot(fig)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Значений", len(value_counts))
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
                fig, ax = plt.subplots(figsize=(12, max(5, len(stack_counts) * 0.3)))
                bars = ax.barh(range(len(stack_counts)), stack_counts.values, color=colors[1])
                ax.set_yticks(range(len(stack_counts)))
                ax.set_yticklabels(stack_counts.index)
                ax.set_xlabel("Количество")
                ax.set_title("Стеки технологий")
                ax.grid(axis='x', alpha=0.3)
                
                if show_values:
                    for i, (bar, v) in enumerate(zip(bars, stack_counts.values)):
                        ax.text(v, i, f' {v}', va='center')
                
                st.pyplot(fig)
                st.divider()
                for stack, count in stack_counts.items():
                    st.write(f"- **{stack}**: {count} ({count/len(df)*100:.1f}%)")

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
            
            hires.index = hires.index.astype(str)
            
            fig, ax = plt.subplots(figsize=(14, 5))
            ax.plot(range(len(hires)), hires.values, marker='o', linewidth=3, markersize=8, color=colors[2])
            ax.fill_between(range(len(hires)), hires.values, alpha=0.3, color=colors[2])
            ax.set_xticks(range(len(hires)))
            ax.set_xticklabels(hires.index, rotation=45, ha='right')
            ax.set_ylabel("Нанято")
            ax.set_title(f"Найм по {period.lower()}")
            ax.grid(True, alpha=0.3)
            
            if show_values:
                for i, v in enumerate(hires.values):
                    ax.text(i, v, f'{int(v)}', ha='center', va='bottom')
            
            st.pyplot(fig)
            
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Всего", len(df['Column1.hire_date'].dropna()))
            with col2:
                st.metric("Пик", f"{hires.idxmax()} ({hires.max()})")
            with col3:
                st.metric("Среднее", f"{hires.mean():.1f}")

    # TAB 4: Кросс-анализ
    with tab4:
        st.subheader("Кросс-анализ")
        
        analysis = st.radio("Тип", ["Stack vs Role", "Role vs Grade", "Status vs Stack"], horizontal=True, key="tab4_type")
        
        if analysis == "Stack vs Role" and 'Column1.stack' in df.columns and 'Column1.role' in df.columns:
            crosstab = pd.crosstab(df['Column1.role'].dropna(), df['Column1.stack'].dropna())
            fig, ax = plt.subplots(figsize=(12, max(5, len(crosstab) * 0.3)))
            crosstab.plot(kind='barh', ax=ax, color=colors)
            ax.set_xlabel("Количество")
            ax.set_title("Role по Stack")
            ax.legend(title='Stack', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        elif analysis == "Role vs Grade" and 'Column1.role' in df.columns and 'Column1.grade' in df.columns:
            crosstab = pd.crosstab(df['Column1.role'].dropna(), df['Column1.grade'].dropna())
            fig, ax = plt.subplots(figsize=(12, max(5, len(crosstab) * 0.3)))
            crosstab.plot(kind='bar', ax=ax, stacked=True, color=colors)
            ax.set_ylabel("Количество")
            ax.set_title("Grade по Role")
            ax.legend(title='Grade', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        
        elif analysis == "Status vs Stack" and 'Column1.status' in df.columns and 'Column1.stack' in df.columns:
            crosstab = pd.crosstab(df['Column1.status'].dropna(), df['Column1.stack'].dropna())
            fig, ax = plt.subplots(figsize=(12, 5))
            crosstab.plot(kind='bar', ax=ax, color=colors)
            ax.set_ylabel("Количество")
            ax.set_title("Статусы по Stack")
            ax.legend(title='Stack', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

    # TAB 5: Статистика
    with tab5:
        st.subheader("Статистика")
        
        stat_type = st.selectbox("Тип", ["Числовые данные", "Сводная таблица", "Корреляции"], key="tab5_select")
        
        if stat_type == "Числовые данные":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                selected_num = st.selectbox("Столбец", numeric_cols, key="tab5_num")
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
                
                ax1.hist(df[selected_num].dropna(), bins=20, color=colors[0], edgecolor='black', alpha=0.7)
                ax1.set_title(f"Распределение {selected_num}")
                ax1.grid(axis='y', alpha=0.3)
                
                ax2.boxplot(df[selected_num].dropna(), vert=True)
                ax2.set_title(f"Box plot {selected_num}")
                ax2.grid(axis='y', alpha=0.3)
                
                st.pyplot(fig)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mean", f"{df[selected_num].mean():.2f}")
                with col2:
                    st.metric("Median", f"{df[selected_num].median():.2f}")
                with col3:
                    st.metric("Min", f"{df[selected_num].min():.2f}")
                with col4:
                    st.metric("Max", f"{df[selected_num].max():.2f}")
        
        elif stat_type == "Сводная таблица":
            st.write("**Описательная статистика:**")
            st.dataframe(df.describe(), use_container_width=True)
        
        elif stat_type == "Корреляции":
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 1:
                corr = numeric_df.corr()
                fig, ax = plt.subplots(figsize=(8, 6))
                im = ax.imshow(corr, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
                ax.set_xticks(range(len(corr.columns)))
                ax.set_yticks(range(len(corr.columns)))
                ax.set_xticklabels(corr.columns, rotation=45, ha='right')
                ax.set_yticklabels(corr.columns)
                plt.colorbar(im, ax=ax)
                ax.set_title("Корреляции")
                st.pyplot(fig)
            else:
                st.info("Мало числовых столбцов")

    # TAB 6: Таблица
    with tab6:
        st.subheader("Таблица данных")
        
        col_search, col_sort = st.columns([2, 1])
        
        with col_search:
            search_term = st.text_input("🔍 Поиск", "")
        
        with col_sort:
            if len(df.columns) > 0:
                sort_col = st.selectbox("Сортировка", df.columns, key="tab6_sort")
            else:
                sort_col = None
        
        if search_term:
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            df_display = df[mask]
            st.info(f"Найдено {len(df_display)} из {len(df)}")
        else:
            df_display = df
        
        if sort_col:
            df_display = df_display.sort_values(by=sort_col, ascending=True)
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        if st.button("📥 CSV", use_container_width=True):
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="Загрузить",
                data=csv,
                file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

else:
    st.info("👈 Загрузите данные на главной странице")