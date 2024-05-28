import streamlit as st
import pandas as pd
from collections import Counter
import scipy as ss
import xlsxwriter
import openpyxl


st.set_page_config(page_title="Дипломная работа")
st.title("Data analyzer 📈 📊")
st.write(" ")
hide_st_style="""

<style>
.stDeployButton {visibility:hidden}
</style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)


uploded_file = st.file_uploader(label="Выберите Excel файл  : ", type=["xlsx", "xls"],)
if uploded_file:
    try:
        df = pd.read_excel(uploded_file)
        st.markdown("---")


        deleted_data_list= st.multiselect("Выберите столбцы, которые нужно удалить : ", df.columns)
        df=df.drop(deleted_data_list,axis=1)
        column_names=df.columns
        st.sidebar.header("Действия")
        show_btn = st.sidebar.button("Посмотреть таблицу")
        if show_btn:
            st.subheader(" Таблица данных для анализа")
            st.dataframe(df)
    except Exception as e:
        st.warning(f"Ошибка с читением или показанием : {e}")

    button_emp = st.sidebar.button("Эмпирическое описание")
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
                    st.success("Достаточный объем информации для раскрытия сложного")
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
                st.warning("Значильно для системы")
            else:
                st.write("Они очень много")
    except Exception as e:
        st.warning(f"Эмпирическая ошибка : {e}")

    try:
        constant_columns = df.columns[df.nunique() == 1]
        button_port = st.sidebar.button("Статистический портрет ")
        minzn=[]
        maxzn=[]
        srzn=[]
        stdd=[]
        notanof=[]
        nijniy=[]
        verxnay=[]
        median=[]
        razm=[]
        moda=[]
        for i in df:
            minzn.append(min(df[i]))
            maxzn.append(max(df[i]))
            srzn.append(df[i].mean())
            stdd.append(df[i].std())
            notanof.append(df[i].notna().sum())
            nijniy.append(df[i].quantile(0.25))
            verxnay.append(df[i].quantile(0.75))
            median.append(df[i].median())
            razm.append(max(df[i])-min(df[i]))
            moda.append(df[i].mode(1))

        dictportstat={"Показатели":column_names,
                      "мин. знач":minzn,
                      "Нижняя квартиль": nijniy,
                      "Медиана": median,
                      "станд. отклонение":stdd,
                      "Верхняя квартиль": verxnay,
                      "мах. знач": maxzn,
                      }
        diccy={"Показатели":column_names,
               "Объем выборки":notanof,
               "ср. знач": srzn,
               "Размах":razm,
               # "Мода":moda,

               }
        framestat=pd.DataFrame(dictportstat)
        framestat2=pd.DataFrame(diccy)
        min_vib=0
        max_vib=0
        for i in column_names:
            if df[i].notna().sum() < min_vib:
                min_vib=df[i].notna().sum()
            if df[i].notna().sum() >max_vib:
                max_vib=df[i].notna().sum()
        if button_port:
            st.markdown("---")
            st.header("Статистический портрет системы")
            st.subheader("Представительность в изменчивости показателей")
            a1,a2,a3=0,0,0
            for i in column_names:
                if df[i].notna().sum()<=row_nums//4:
                    a1+=1
                elif df[i].notna().sum()<=row_nums//2:
                    a2+=1
                elif df[i].notna().sum()<=3*row_nums//4:
                    a3+=1
            a4=col_nums - (a1 + a2 + a3)
            frame1=pd.DataFrame({"минимальный : ":[min_vib],
            "максимальный : ":[ max_vib]})
            st.write("Объемы выборок : ",frame1)
            if row_nums < 4:
                st.write(f"от 0 до {row_nums} : ", col_nums)
            else:
                frame2=pd.DataFrame([(str(f"от 0 до {row_nums //4} : "),a1),
                                     (str(f"{row_nums // 4} от  до {row_nums // 2} : "), a2),
                                     (str(f"{row_nums // 2} от  до {3 * row_nums // 4} : "), a3),
                                     (str(f"{3 * row_nums // 4} от  до {row_nums} : "), a4)],
                                    columns=("диапазон","количество показателей"))
                st.write("Распределение показателей по объему выборки : ",frame2)
                st.bar_chart(frame2.set_index("диапазон"),color= "#A7C7E7")
            st.write(f"Показателы с неизменяющимися значениями:",constant_columns)
            st.subheader("Таблица Квантили распределения")
            st.write(framestat)
            st.subheader("Таблица Дескриптивных статистик")
            st.write(framestat2)
            st.header("Заключение")
            st.subheader("Полнота таблицы наблюдений :")
            try :
                if a1 > a2 + a3 + a4 or a2> a1+a3+a4 or a3>a1+a2+a4 or a4 > a1+a2+a3:
                    st.warning("недостаточная. ")
                else:
                    st.success("достаточная.")

            except:
                pass
            st.subheader("Представительность таблицы наблюдений :")
            if col_nums > 50:
                st.success("достаточная.")
            else:
                st.warning("недостаточная. ")

    except Exception as e:
        st.warning(f"Статистическая ошибка : {e}")

    try:
        st.sidebar.title("Экспертиза слов")
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

        razmax= dict()
        maks=dict()
        xarakter=dict()

        for i in df:
            ls=[]
            meann=df[i].mean()
            stdd=df[i].std()
            bigls=df[i].tolist()
            try:
                for j in range(len(bigls)):
                    if  bigls[j]> meann - 4 *stdd and  bigls[j]<meann + 4 *stdd :
                        ls.append((bigls[j]-meann)/stdd)
                razmax[i]=max(ls)-min(ls)
                maks[i]=max(abs(max(ls)),abs(min(ls)))
                if len(bigls)!=len(ls):
                    xarakter[i]=1
                else:
                    xarakter[i]=2
            except:
                pass

        # st.write(razmax)
        # st.write(maks)
        # st.write(xarakter)

        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False
        def callback():
            st.session_state.button_clicked = True
        def anticallback():
            st.session_state.button_clicked = False
        pred_btn = st.sidebar.button("Представительность",on_click=callback)
        dictt = {"Вар_0": sorted_obyom_rang.keys(),
                 "Объем-ранг": sorted_obyom_rang.values(),
                 "Вар_1": sorted_dol_raz_sos.keys(),
                 "Доля разн.знач.": sorted_dol_raz_sos.values(),
                 "Вар_2": sorted_res_max_sovpad.keys(),
                 "Макс.совпад.": sorted_res_max_sovpad.values(),
                 "Вар_3": sorted_sr_sovpad.keys(),
                 "Ср.Совпад": sorted_sr_sovpad.values()
                 }
        dataa = pd.DataFrame(dictt)

        if pred_btn or st.session_state.button_clicked:
            st.title("Таблица разнообразия:")
            st.write(dataa)
            st.title("Таблица изменчивость")
            st.subheader("Масштабность ")
            st.write("Размах нормированного распределения : ---")
            st.subheader("Характерность значений")
            st.write("Характерность значений : ---")
            st.subheader("Непропорциональность")
            st.write("Интенсивность вариации : --- ")


            def converter_matrix(dictionary, type_sort):
                returned_dict = {}
                if type_sort:
                    for i, y in enumerate(dictionary.keys()):
                        returned_dict[y] = ss.stats.rankdata(list(dictionary.values()))[i]
                else:
                    for i, y in enumerate(dictionary.keys()):
                        returned_dict[y] = len(ss.stats.rankdata(list(dictionary.values()))) - \
                                           ss.stats.rankdata(list(dictionary.values()))[i] + 1
                return returned_dict


            st.subheader("Разнообразие")
            sorted_obyom_rang_matrix = converter_matrix(sorted_obyom_rang, False)
            sorted_dol_raz_sos_matrix = converter_matrix(sorted_dol_raz_sos, False)
            sorted_res_max_sovpad_matrix = converter_matrix(sorted_res_max_sovpad, True)
            sorted_sr_sovpad_matrix = converter_matrix(sorted_sr_sovpad, True)

            matrix_obyom_po_colum = {}
            matrix_dol_raz_sos_po_colum = {}
            matrix_res_max_sovpad_po_colum = {}
            matrix_sr_sovpad_po_colum = {}
            for i in column_names:
                matrix_obyom_po_colum[i] = sorted_obyom_rang_matrix[i]
                matrix_dol_raz_sos_po_colum[i] = sorted_dol_raz_sos_matrix[i]
                matrix_res_max_sovpad_po_colum[i] = sorted_res_max_sovpad_matrix[i]
                matrix_sr_sovpad_po_colum[i] = sorted_sr_sovpad_matrix[i]

            dictt_1 = {"Показатели": column_names,
                       "Объем-ранг": matrix_obyom_po_colum.values(),
                       "Доля разн.знач.": matrix_dol_raz_sos_po_colum.values(),
                       "Макс.совпад.": matrix_res_max_sovpad_po_colum.values(),
                       "Ср.Совпад": matrix_sr_sovpad_po_colum.values()
                       }
            dataa_1 = pd.DataFrame(dictt_1)
            dataa_1["сумма"] = dataa_1[dataa_1.columns[1:]].sum(axis=1)
            # ozgartish garak
            M = 4
            A = M * (col_nums + 1) / 2
            S = sum([(A - i) ** 2 for i in dataa_1["сумма"]])
            W = (12 * S) / (M ** 2 * col_nums * (col_nums ** 2 - 1))
            st.write(dataa_1)
            dictt_2 = {"Показатели": column_names,
                       "Объем-ранг": [col_nums - i for i in list(matrix_obyom_po_colum.values())],
                       "Доля разн.знач.": [col_nums - i for i in list(matrix_dol_raz_sos_po_colum.values())],
                       "Макс.совпад.": [col_nums - i for i in list(matrix_res_max_sovpad_po_colum.values())],
                       "Ср.Совпад": [col_nums - i for i in list(matrix_sr_sovpad_po_colum.values())]
                       }
            dataa_2 = pd.DataFrame(dictt_2)
            dataa_2["summa"] = dataa_2[dataa_2.columns[1:]].sum(axis=1)
            summa_2 = dataa_2["summa"].sum(axis=0)
            dataa_2["вес"] = [i / summa_2 for i in dataa_2["summa"]]
            st.write(dataa_2)
            st.write("Коэффициент Конкордации (Согласованность) : ", W)

            file_name=st.text_input("Чтобы сохранить в виде ексель файл, просто введите имя файла:")
            dataa.to_excel(f"C:/Users/dadaxon9830/Desktop/{file_name}.xlsx", index=True)
            anticallback()
            if file_name:

                st.success(f"Таблица успешно сохранен в рабочем столе с названием <-{file_name}->")





            st.title("Равномерность")
            st.subheader("Группируемость")
            st.write("Число групп : ---")
            st.subheader("Гладкость")
            st.write("Среднее отклонение частности : ---")
            st.subheader("Рельефность")
            st.write("Максимальное отклонение частности")


    except Exception as e:
        st.warning(f"Предствителная ошибка : {e}")
    box2 = st.sidebar.button("Представительность типичного и особенного")

    if box2:
        pass



    # ("Неравномерность величин",
    #  "Многозначность", "Правильность", "Уклонение",
    #  "Типичность", "Фигурность", "Отпадение",
    #  "Изменяемость", "Центрированность", "Расположенность")

