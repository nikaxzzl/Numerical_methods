# compare_15_tasks.py
# Запуск: python compare_15_tasks.py
# Требуется: pip install numpy
# Все задачи 1–15: два решения, замеры, проверка результатов и краткие выводы.

import math
import time
import sys
import numpy as np


rng = np.random.default_rng(42)


def measure(fn, x, repeat=3):
    """Возвращает результат последнего прогона и лучшее время."""
    best = float("inf")
    result = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = fn(x)
        best = min(best, time.perf_counter() - t0)
    return result, best


def report(name, r_loop, t_loop, r_numpy, t_numpy, correct):
    speedup = t_loop / t_numpy if t_numpy > 0 else float("inf")
    print(f"\n{name}")
    print(f"  Python: {t_loop * 1000:10.3f} мс")
    print(f"  NumPy:  {t_numpy * 1000:10.3f} мс")
    print(f"  Ускорение: {speedup:.2f}x")
    print(f"  Результаты совпадают: {correct}")
    return speedup


def section(title):
    print("\n" + "=" * 76)
    print(title)
    print("=" * 76)


# print("ЗАДАЧА 1. Сумма массива")


# def loop_sum(a):
#     s = 0.0
#     for x in a:
#         s += x
#     return s


# def numpy_sum(a):
#     return a.sum()


# print(f"{'n':>12} | {'Python, мс':>12} | {'NumPy, мс':>12} | {'ускорение':>11}")
# print("-" * 58)
# for n in (10**5, 10**6, 10**7):
#     a = rng.normal(size=n)
#     r1, t1 = measure(loop_sum, a)
#     r2, t2 = measure(numpy_sum, a)
#     print(f"{n:12,d} | {t1*1000:12.3f} | {t2*1000:12.3f} | {t1/t2:10.2f}x")
#     print(f"  Проверка np.isclose: {np.isclose(r1, r2)}")
# print("Вывод: NumPy обычно выигрывает на больших массивах, потому что основная")
# print("работа выполняется в скомпилированном коде, а не в Python-цикле.")


# # ---------------------------------------------------------------------------
# # ЗАДАЧА 2. Среднее и стандартное отклонение
# # ---------------------------------------------------------------------------
# print("ЗАДАЧА 2. Среднее и стандартное отклонение")

# a = rng.normal(size=10**6)


# def loop_mean_std(a):
#     s = 0.0
#     sq = 0.0
#     for x in a:
#         s += x
#         sq += x * x
#     mean = s / len(a)
#     # Формула через разность квадратов менее устойчива численно.
#     variance = sq / len(a) - mean * mean
#     return mean, math.sqrt(max(variance, 0.0))


# def numpy_mean_std(a):
#     return a.mean(), a.std()


# r1, t1 = measure(loop_mean_std, a)
# r2, t2 = measure(numpy_mean_std, a)
# report("n=1 000 000", r1, t1, r2, t2,
#        np.allclose(r1, r2, rtol=1e-12, atol=1e-12))
# print("Вывод: NumPy-код короче. Его std обычно устойчивее формулы E[x²]−E[x]²,")
# print("поскольку дисперсия вычисляется через отклонения от среднего; точность")
# print("всё равно зависит от данных и допуска сравнения.")


# # ---------------------------------------------------------------------------
# # ЗАДАЧА 3. y = sin(x) + x^2
# # ---------------------------------------------------------------------------
# # section("ЗАДАЧА 3. Поэлементное преобразование")

# a = rng.normal(size=10**6)


# def loop_transform(a):
#     out = []
#     for x in a:
#         out.append(math.sin(x) + x * x)
#     return out


# def numpy_transform(a):
#     return np.sin(a) + a**2


# r1, t1 = measure(loop_transform, a)
# r2, t2 = measure(numpy_transform, a)
# report("n=1 000 000", r1, t1, r2, t2, np.allclose(r1, r2))
# print(f"  ndarray float64, результат: {r2.nbytes / 1024**2:.2f} MiB")
# print(f"  Python list: ориентировочно {sys.getsizeof(r1) + sum(sys.getsizeof(x) for x in r1[:1000]) * (len(r1)/1000) / 1024**2:.2f} MiB")
# print("  В выражении np.sin(a) + a**2 создаются два промежуточных массива")
# print("  (sin(a) и a**2) и итоговый массив. Для экономии памяти можно применять out=.")


# # ---------------------------------------------------------------------------
# # ЗАДАЧА 4. Clipping
# # ---------------------------------------------------------------------------
# section("ЗАДАЧА 4. Условная замена (clipping)")

# a = rng.normal(size=10**6)


# def loop_clip(a):
#     out = []
#     for x in a:
#         if x < 0:
#             out.append(0.0)
#         elif x > 1:
#             out.append(1.0)
#         else:
#             out.append(x)
#     return out


# def numpy_clip(a):
#     return np.clip(a, 0, 1)


# r1, t1 = measure(loop_clip, a)
# r2, t2 = measure(numpy_clip, a)
# report("n=1 000 000", r1, t1, r2, t2, np.allclose(r1, r2))
# changed = np.sum((a < 0) | (a > 1))
# print("  Изменено элементов:", int(changed))
# print("Вывод: np.clip выражает всю операцию одной функцией, без явных if и for.")


# # ---------------------------------------------------------------------------
# # ЗАДАЧА 5. Сумма по строкам матрицы
# # ---------------------------------------------------------------------------
# section("ЗАДАЧА 5. Сумма по строкам матрицы")

# m = rng.normal(size=(100_000, 10))


# def loop_sum_rows(mat):
#     result = [0.0] * mat.shape[0]
#     for i in range(mat.shape[0]):
#         s = 0.0
#         for j in range(mat.shape[1]):
#             s += mat[i, j]
#         result[i] = s
#     return result


# def numpy_sum_rows(mat):
#     return mat.sum(axis=1)


# r1, t1 = measure(loop_sum_rows, m)
# r2, t2 = measure(numpy_sum_rows, m)
# report("matrix=(100000, 10)", r1, t1, r2, t2, np.allclose(r1, r2))
# print("Вывод: axis=1 прямо обозначает суммирование по строкам. NumPy легче читать")
# print("и поддерживать: не нужно вручную управлять индексами и счётчиками.")


# # # ---------------------------------------------------------------------------
# # # ЗАДАЧА 6. Среднее по столбцам и нормировка (центрирование)
# # # ---------------------------------------------------------------------------
# print("ЗАДАЧА 6. Среднее по столбцам и центрирование")

# m = rng.normal(size=(100_000, 10))


# def loop_center_columns(mat):
#     n, p = mat.shape
#     means = [0.0] * p
#     for j in range(p):
#         s = 0.0
#         for i in range(n):
#             s += mat[i, j]
#         means[j] = s / n

#     result = [[0.0] * p for _ in range(n)]
#     for i in range(n):
#         for j in range(p):
#             result[i][j] = mat[i, j] - means[j]
#     return result


# def numpy_center_columns(mat):
#     return mat - mat.mean(axis=0)


# r1, t1 = measure(loop_center_columns, m)
# r2, t2 = measure(numpy_center_columns, m)
# report("matrix=(100000, 10)", r1, t1, r2, t2, np.allclose(r1, r2))
# print("  Средние после центрирования:", np.max(np.abs(r2.mean(axis=0))))
# print("  SLOC: NumPy — 1 строка выражения; цикл требует отдельных проходов и индексов.")
# print("Вывод: broadcasting автоматически вычитает среднее каждого столбца.")


# # # ---------------------------------------------------------------------------
# # # ЗАДАЧА 7. Максимум и индекс; поведение с NaN
# # # ---------------------------------------------------------------------------
# # section("ЗАДАЧА 7. Максимум и индекс")

# a = rng.normal(size=10**6)


# def loop_max_index(a):
#     max_val = a[0]
#     max_idx = 0
#     for i in range(1, len(a)):
#         if a[i] > max_val:
#             max_val = a[i]
#             max_idx = i
#     return max_val, max_idx


# def numpy_max_index(a):
#     idx = int(a.argmax())
#     return a.max(), idx


# r1, t1 = measure(loop_max_index, a)
# r2, t2 = measure(numpy_max_index, a)
# report("n=1 000 000", r1, t1, r2, t2, r1[0] == r2[0] and r1[1] == r2[1])

# a_nan = np.array([1.0, 5.0, np.nan, 3.0])
# print("  Пример с NaN:")
# print("  обычный цикл:", loop_max_index(a_nan))
# print("  np.nanmax:", np.nanmax(a_nan), "(индекс:)", np.nanargmax(a_nan))
# print("  Примечание: обычные max/argmax NumPy тоже не игнорируют NaN; для этого")
# print("  нужны именно nanmax/nanargmax. В реальном массиве NaN следует обрабатывать явно.")


# # ---------------------------------------------------------------------------
# # ЗАДАЧА 8. Фильтрация по порогу и оценка памяти
# # ---------------------------------------------------------------------------
# section("ЗАДАЧА 8. Фильтрация по порогу")

# a = rng.normal(size=10**6)


# def loop_filter(a):
#     return [x for x in a if x > 0]


# def numpy_filter(a):
#     return a[a > 0]


# r1, t1 = measure(loop_filter, a)
# r2, t2 = measure(numpy_filter, a)
# report("n=1 000 000", r1, t1, r2, t2, np.allclose(r1, r2))
# list_bytes_est = sys.getsizeof(r1) + sum(sys.getsizeof(x) for x in r1[:1000]) * (len(r1) / 1000)
# numpy_bytes = r2.nbytes
# print(f"  Память списка (приближённо): {list_bytes_est / 1024**2:.2f} MiB")
# print(f"  Память ndarray: {numpy_bytes / 1024**2:.2f} MiB")
# print(f"  Отношение: примерно {list_bytes_est / numpy_bytes:.1f}x")
# print("Вывод: ndarray хранит float64 компактно; список хранит ссылки и отдельные объекты.")


# # ---------------------------------------------------------------------------
# # ЗАДАЧА 9. In-place замена отрицательных на модуль
# # ---------------------------------------------------------------------------
# section("ЗАДАЧА 9. Замена по маске in-place")

# base = rng.normal(size=10**6)


# def loop_abs_inplace(a):
#     for i in range(len(a)):
#         if a[i] < 0:
#             a[i] = -a[i]
#     return a


# def numpy_abs_inplace(a):
#     np.abs(a, out=a)
#     return a


# # Для честного сравнения каждому способу выдаём собственную копию.
# a_loop = base.copy()
# a_numpy = base.copy()
# r1, t1 = measure(loop_abs_inplace, a_loop)
# r2, t2 = measure(numpy_abs_inplace, a_numpy)
# report("n=1 000 000 (in-place)", r1, t1, r2, t2,
#        np.allclose(r1, r2) and np.shares_memory(r1, a_loop) and np.shares_memory(r2, a_numpy))
# print("  Оба результата используют исходный массив соответствующего варианта.")
# print("Вывод: out=a позволяет не выделять отдельный массив результата, что важно")
# print("при обработке больших данных и ограниченной оперативной памяти.")

# print("ЗАДАЧА 10. Комбинированная маска")

# a = rng.normal(size=10**6)


# def loop_range_filter(a):
#     out = []
#     for x in a:
#         if -1 < x < 1:
#             out.append(x)
#     return out


# def numpy_range_filter(a):
#     return a[(a > -1) & (a < 1)]


# r1, t1 = measure(loop_range_filter, a)
# r2, t2 = measure(numpy_range_filter, a)
# report("n=1 000 000", r1, t1, r2, t2, np.allclose(r1, r2))
# # print("Вывод: скобки вокруг каждого сравнения обязательны. Оператор & имеет")
# print("другой приоритет, чем сравнения; конструкция a > -1 & a < 1 некорректна.")


