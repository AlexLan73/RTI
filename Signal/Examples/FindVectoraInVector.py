import numpy as np
import json

def LoadData():
    str ="/home/alanin/Python/Data/OUT/FM/000/tfpMSeqSigns.json"
    with open(str, 'r') as file:
        data = json.load(file)
    return data


def find_repeated_sequence(vector, sequence_length=3):
    # Создаем матрицу со скользящим окном
    window_size = sequence_length
    num_windows = len(vector) - window_size + 1
    windows = np.lib.stride_tricks.as_strided(
        vector, shape=(num_windows, window_size), strides=(vector.strides[0], vector.strides[0])
    )

    # Ищем повторяющиеся последовательности
    repeated_sequences = []
    _count = num_windows
    for i in range(num_windows):
        for j in range(i + 1, num_windows):
            if np.all(windows[i] == windows[j]):
                repeated_sequences.append((i, j))
        _count-=1
        print(_count)

    # Возвращаем позиции повторяющихся последовательностей
    return repeated_sequences

# Пример использования
vector = np.array([70, 69, 72, 52, 6, 65, 65, 51, 60, 92, 56, 6, 72, 38, 21, 30, 51, 60, 92, 56, 21, 4, 84, 31])
sequence_length = 3

positions = find_repeated_sequence(vector, sequence_length)

if positions:
    print(f"Повторяющиеся последовательности найдены в позициях:")
    for start, end in positions:
        print(f"Последовательность: {vector[start:start+sequence_length]}, Позиции: {start} и {end}")
else:
    print("Повторяющихся последовательностей не найдено.")



"""
Объяснение

    Создание матрицы со скользящим окном: Используем функцию np.lib.stride_tricks.as_strided, чтобы создать матрицу, где каждая строка представляет собой последовательность из sequence_length элементов исходного вектора.

    Поиск повторяющихся последовательностей: Итерируем по всем окнам и сравниваем каждое окно с остальными. Если окна совпадают, это означает, что последовательность повторяется.

    Возвращение позиций: Возвращаем позиции начала повторяющихся последовательностей в исходном векторе.

Этот код позволяет найти все повторяющиеся последовательности заданной длины в векторе и выделить их позиции.

"""