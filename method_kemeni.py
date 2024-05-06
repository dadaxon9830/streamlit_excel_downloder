# data = [
#     ("NPlav", "tVud", 0.625),
#     ("NSl", "tKop", 0.5868),
#     ("MasSl", "tNagr", 0.5868),
#     # Ваш полный список данных здесь
# ]
#
# # Функция для вычисления коэффициента Кемени-Снелла для одной пары объектов
# def calculate_kemeny_snell(data_pair):
#     similarity = data_pair[2]
#     rank_difference = abs(rankings[data_pair[0]] - rankings[data_pair[1]])
#     return similarity * rank_difference
#
# # Словарь с рангами объектов
# rankings = {obj: rank for rank, (obj, _, _) in enumerate(data)}
#
# # Вычисляем коэффициент Кемени-Снелла для всех пар объектов
# kemeny_snell_coefficient = sum(calculate_kemeny_snell(pair) for pair in data)
#
# print("Коэффициент Кемени-Снелла для данных:", kemeny_snell_coefficient)
import numpy as np

# Данные ранжирования
import numpy as np

import numpy as np

# Данные ранжирования
data = [
    ["Mo_Pl", 4, "tOk", 0.0833, "tOk", 0.1185, "tOk", 0.0417],
    ["Si_Pl", 4, "Mo_Pl", 0.0486, "Mo_Pl", 0.2578, "Mo_Pl", 0.0714],
    ["tOk", 4, "Tp", 0.0486, "Tp", 0.2578, "Tp", 0.0714],
    ["Tp", 4, "Si_Pl", 0.0104, "Si_Pl", 0.9861, "Si_Pl", 0.3333],
]

# Создаем матрицу R
n = len(data)
R = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i == j:
            R[i, j] = 0  # Элементы по диагонали равны 0
        else:
            # Проверяем ранжирование
            if data[i][3] > data[j][3]:  # Первый элемент предпочтительнее второго
                R[i, j] = 1
            elif data[i][3] < data[j][3]:  # Второй элемент предпочтительнее первого
                R[i, j] = -1
            else:  # Элементы равны
                R[i, j] = 0

print("Матрица предпочтений R:")
print(R)
