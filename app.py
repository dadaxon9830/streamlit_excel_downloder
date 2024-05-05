import streamlit as st
import pandas as pd
from collections import Counter
import xlsxwriter
import openpyxl


st.set_page_config(page_title="Дипломная работа")
st.title("Data analyzer 📈 📊")
st.write(" ")

uploded_file = st.file_uploader("Выберите Excel файл  : ", type=["xlsx", "xls"])
if uploded_file:
    try:
        df = pd.read_excel(uploded_file)
        st.markdown("---")

        deleted_data_list= st.multiselect("Удалить ненужный (неколичественный) показатель : ", df.columns)
        df=df.drop(deleted_data_list,axis=1)
        column_names=df.columns
        st.sidebar.header("Действия")
        show_btn = st.sidebar.button("Посмотреть дата")
        if show_btn:
            st.subheader(" Таблица данных для анализа")
            st.dataframe(df)
    except Exception as e:
        st.warning(f"Ошибка с читением или показанием : {e}")

    button_emp = st.sidebar.button("Эмпирическое описание для системы")
    try:
        col_nums = df.shape[1]
        row_nums = df.shape[0]
        summa = 0
        for i, j in enumerate(df):
            summa += df[j].isna().sum()
        per = summa / (row_nums * col_nums) * 100
        if button_emp:
            st.header("Эмпирическое описание системы ")
            st.write("Все показателы системы : ", column_names)
            st.write("Число наблюдений : ", row_nums)
            st.write("Число показателей : ", col_nums)
            st.write("Обшие количество пропусктов  : ", summa)
            st.write("Количество полних данных : ", row_nums * col_nums - summa)
            st.header("Заключение : ")
            st.subheader("Полноты и представительности системы данных : ")
            if 0 <= row_nums < 100:
                if 0 <= col_nums < 50:
                    st.write("Мало данных")
                elif 50 <= col_nums < 1000:
                    st.write("Недостаточно данных для верификации")
                else:
                    st.write("Недостаточная представительность данных")
            elif 100 <= row_nums < 500:
                if 0 <= col_nums < 50:
                    st.write("Мало показателей для раскрытия сложного")
                elif 50 <= col_nums < 1000:
                    st.write("Достаточный объем информации для раскрытия сложного")
                else:
                    st.write("Недостаточная представительность данных")
            elif 500 <= row_nums < 2000:
                if 0 <= col_nums < 50:
                    st.write("Мало показателей для раскрытия сложного")
                elif 50 <= col_nums < 1000:
                    st.write("Оптимальный объем информации для раскрытия сложного и верификации")
                else:
                    st.write("Недостаточная представительность данных")
            else:
                st.write("Усложнение анализа ввиду заметного проявления в данных несущественного и особенного ")
            st.subheader("Количество пропусков : ")
            if per <= 5:
                st.write("Незначильно для системы")
            elif per < 20:
                st.write("Значильно для системы")
            else:
                st.write("Они очень много")
    except Exception as e:
        st.warning(f"Эмпирическая ошибка : {e}")

    try:
        button_port = st.sidebar.button("Статистический портрет системы")
        info_desc = df.describe()
        if button_port:
            st.header("Статистический портрет системы")
            st.write(info_desc)
    except Exception as e:
        st.warning(f"Статистическая ошибка : {e}")

    try:
        st.sidebar.title("Слова и Понятия")
        obyom_rang = dict()
        dol_raz_sostoyaniy = dict()
        max_sovpad = dict()
        sr_sovpad = dict()
        for i in df:
            obyem_viborki = df[i].notna().sum()
            koef1 = obyem_viborki / len(df)
            if koef1 < 0.25:
                ko = 1
            elif koef1 < 0.5:
                ko = 2
            elif koef1 < 0.75:
                ko = 3
            else:
                ko = 4
            obyom_rang[i] = ko
            dol_raz_sostoyaniy[i] = df[i].nunique() / len(df)
            counter = Counter(df[i].values)
            max_frequency = max(counter.values())
            res_max_freq = (max_frequency - 1) / (obyem_viborki - 1)
            max_sovpad[i] = res_max_freq
            srsovpad_val = df[i].nunique()
            sr_sovpad[i] = 1 / df[i].nunique() if df[i].nunique() > 0 else 0

        sorted_obyom_rang = dict(sorted(obyom_rang.items(), key=lambda x: x[1], reverse=True))
        sorted_dol_raz_sos = dict(sorted(dol_raz_sostoyaniy.items(), key=lambda x: x[1], reverse=True))
        sorted_res_max_sovpad = dict(sorted(max_sovpad.items(), key=lambda x: x[1], reverse=False))
        sorted_sr_sovpad = dict(sorted(sr_sovpad.items(), key=lambda x: x[1], reverse=False))
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False
        def callback():
            st.session_state.button_clicked = True
        def anticallback():
            st.session_state.button_clicked = False
        pred_btn = st.sidebar.button("Представительность",on_click=callback)
        if pred_btn or st.session_state.button_clicked:
            st.title("Таблица разнообразия:")
            dictt={"Вар_0":sorted_obyom_rang.keys(),
                   "Объем-ранг":sorted_obyom_rang.values(),
                   "Вар_1":sorted_dol_raz_sos.keys(),
                   "Доля разн.знач.":sorted_dol_raz_sos.values(),
                   "Вар_2": sorted_res_max_sovpad.keys(),
                   "Макс.совпад.":sorted_res_max_sovpad.values(),
                   "Вар_3":sorted_sr_sovpad.keys(),
                   "Ср.Совпад":sorted_sr_sovpad.values()
            }
            dataa= pd.DataFrame(dictt)
            st.write(dataa)
            file_name=st.text_input("Чтобы сохранить в виде ексель файл, просто введите имя файла:")
            dataa.to_excel(f"C:/Users/dadaxon9830/Desktop/{file_name}.xlsx", index=False)
            if file_name:
                st.success(f"Таблица успешно сохранен в рабочем столе с названием <-{file_name}->")
                anticallback()


            st.title("Изменчивость")
            st.subheader("Масштабность ")
            st.write("Размах нормированного распределения : ---")
            st.subheader("Характерность значений")
            st.write("Характерность значений : ---")
            st.subheader("Непропорциональность")
            st.write("Интенсивность вариации : --- ")

            st.title("Равномерность")
            st.subheader("Группируемость")
            st.write("Число групп : ---")
            st.subheader("Гладкость")
            st.write("Среднее отклонение частности : ---")
            st.subheader("Рельефность")
            st.write("Максимальное отклонение частности")
    except Exception as e:
        st.warning(f"Предствителная ошибка : {e}")

    st.sidebar.title("Представительность типичного и особенного")
    box2 = st.sidebar.selectbox("xonn",
                                ("Неравномерность величин",
                                 "Многозначность", "Правильность", "Уклонение",
                                 "Типичность", "Фигурность", "Отпадение",
                                 "Изменяемость", "Центрированность", "Расположенность")
                                )


