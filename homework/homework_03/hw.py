# Задача 1. Инвентаризация массива.
# Создайте массив np.arange(60).reshape(3, 4, 5). Выведите shape, ndim, size, dtype, strides, C_CONTIGUOUS. Объясните в 2–3 предложениях, что означает каждое число в strides и почему size = 60.
import numpy as np
mas = np.arange(60).reshape(3,4,5)
shape_mas = mas.shape
ndim_mas = mas.ndim
size_mas = mas.size
dtype_mas = mas.dtype
strides_mas =mas.strides
mas_C_CONTIGUOUS = mas.flags['C_CONTIGUOUS']
print(f"shape: {shape_mas}\nndim: {ndim_mas}\nsize: {size_mas}\ndtype: {dtype_mas}\nstrides: {strides_mas}\nC_CONTIGUOUS: {mas_C_CONTIGUOUS}")
print("\nПояснение: Значения strides (160, 40, 8) задают величину шага в байтах, которую надо выполнить для перехода дальше по каждой из трех осей. Так как один из элементов весит 8 байт, следовательно шаг к соседнему числу в строке составляет 8 бай, шаг на новую троку (из 5 чисел) - 40 бфайт. А переход к следующей таблице размером 4 на 5 -160. Size = 60, так как он содержит всего 60 чисел (3*4*5 = 60)")


# # Задача 2. int vs float — тихая ловушка.
# # Создайте a = np.array([1, 2, 3, 4]). Выполните a / 2, a // 2, a / 2.0, a.dtype, (a / 2).dtype, (a // 2).dtype. Затем создайте b = np.array([1, 2, 3], dtype=np.int8), прибавьте 127 и выведите результат и dtype. Объясните: почему a / 2 не меняет a, а b + 127 даёт странный результат, и почему NumPy не падает с ошибкой.
a = np.array([1, 2, 3, 4])
n_1 = a/2
n_2 = a//2
n_3 = a / 2.0
a_dtype = a.dtype
a_dtype_2 =(a / 2).dtype
a_dtype_3 = (a // 2).dtype

b = np.array([1, 2, 3], dtype=np.int8)
b_res = b + 127

print(f"a / 2: {n_1}\na // 2: {n_2}\na / 2.0: {n_3}\na.dtype: {a_dtype}\n(a / 2).dtype: {a_dtype_2}\n(a // 2).dtype: {a_dtype_3}\nb: {b}\nb + 127 = {b_res}\n(b + 127).dtype: {b_res.dtype}")
print("\nПояснение: a / 2 не меняет a, потому что NumPy по умолчанию создаёт новый массив, а не изменяет. b+ 127 дает такой результат из-за переполнения. Так как 128 выходит за пределы. Ошибки нет, потому что NumPy делает все ради скорости  ")

# Задача 3. float32 vs float64 — реальная точность.
# Сравните np.float32(0.1) - np.float32(0.1) не поможет; сделайте иначе: float(np.float32(0.1)) - 0.1 и float(np.float64(0.1)) - 0.1. Выведите оба числа в repr и в :.20e. Посчитайте, во сколько раз ошибка float32 больше ошибки float64. Сделайте вывод: в каких задачах численных методов float32 допустим, а в каких — нет.
error32 = float(np.float32(0.1)) - 0.1
error64 = float(np.float64(0.1)) - 0.1
print(f"float32 error (repr):  {repr(error32)}\nfloat32 error (.20e): {error32:.20e}\nfloat64 error (repr):  {repr(error64)}float64 error (.20e): {error64:.20e}\n")
ratio = abs(error32) / abs(error64) if error64 != 0 else float('inf')
print(f"Ошибка float32 больше ошибки float64 в {ratio} раз")
print("\nПояснение: ")

num1 = np.zeros((2, 3), dtype=np.float64)
num2 = np.zeros((2, 3), dtype=np.float32)
num3 = np.ones((2, 3), dtype=np.int16)
num4 = np.full((2, 3), 7, dtype=np.uint8)
print(f"num1 (float64): dtype: {num1.dtype}, bytes: {num1.nbytes}\nnum2 (float32): dtype: {num2.dtype}, bytes: {num2.nbytes}\nnum3 (int16):   dtype: {num3.dtype}, bytes: {num3.nbytes}\nnum4 (uint8): dtype: {num4.dtype}, bytes: {num4.nbytes}\n")
element = 1000 * 1000
bytes_float64 = element * 8
bytes_float32 = element * 4
saved_bytes = bytes_float64 - bytes_float32
s = saved_bytes / (1024 * 1024)
print(f"В байтах: {saved_bytes} байт")
print(f"В мегабайтах: {s} МБ")

# Блок 2. reshape, ravel, flatten, .T, newaxis (задачи 5–8)

# Задача 5. Цепочка reshape.
# Создайте a = np.arange(24). Преобразуйте последовательно в (4, 6), (2, 3, 4), (2, 2, 6), (24,). После каждого шага выведите shape и проверьте через np.array_equal(a, текущий.ravel()), что данные не потерялись. Объясните: почему reshape обычно не копирует данные и когда он вынужден скопировать.
a = np.arange(24)

num = [(4, 6), (2, 3, 4), (2, 2, 6), (24,)]

active = a
for sh in num:
    active = active.reshape(sh)
    equal = np.array_equal(a, active.ravel())
    print(f"Shape: {active.shape:<10} | Данные совпадают: {equal}")


# Задача 6. flatten vs ravel — копия или view.
# Создайте M = np.arange(12).reshape(3, 4). Получите f = M.flatten() и r = M.ravel(). Выведите f.base is None, r.base is M (или r.base is not None). Измените f[0] = 999 и r[1] = 888 — проверьте, изменился ли M в каждом случае. Сделайте вывод: когда использовать ravel, когда flatten.
M = np.arange(12).reshape(3, 4)
flatten_M = M.flatten()
ravel_M= M.ravel()
print(f"f.base is None: {flatten_M.base is None}")
print(f"r.base is M: {ravel_M.base is M}\n")
flatten_M[0] = 999
ravel_M[1] = 888
print(f"M[0,0]: {M[0, 0]}")
print(f"M[0,1]: {M[0, 1]}")


# Задача 7. newaxis, squeeze, транспонирование.
# Создайте v = np.arange(5). Получите:

# v[:, None] — форма?
# v[None, :] — форма?
# np.squeeze(v[:, None]) — форма?
# np.arange(6).reshape(2, 3).T — форма и содержимое.
# Для каждой операции объясните одной строкой, что произошло. Затем вычислите v[:, None] + v[None, :] — какая форма получилась и что это за матрица (подсказка: таблица умножения).
v = np.arange(5)
print(f"v[:, None]: {v[:, None].shape}")
print(f"v[None, :]: {v[None, :].shape}")
print(f"squeeze: {np.squeeze(v[:, None]).shape}")
m_t = np.arange(6).reshape(2, 3).T
print(f"T shape: {m_t.shape}\n.T data:\n{m_t}")
res = v[:, None] + v[None, :]
print(f"Форма сложения: {res.shape}")
print(f"Матрица: {res}")

# Задача 8. Транспонирование без копии.
# Создайте A = np.arange(6).reshape(2, 3). Получите B = A.T. Проверьте B.base is A (или B.base is not None). Измените B[0, 1] = 999 — изменился ли A? Сделайте вывод: почему .T — view, а не копия, и как это связано с strides.
A = np.arange(6).reshape(2, 3)
B = A.T
print(f"B.base A: {B.base is A}")
B[0, 1] = 999
print(f"A = {A}")
# Блок 3. Операции, агрегации, axis (задачи 9–11)

# Задача 9. Поэлементно vs матричное.
# Создайте A = np.arange(6).reshape(2, 3) и B = np.arange(6).reshape(3, 2). Выполните A @ B, A.T @ B.T, A * A. Выведите формы и значения. Объясните: почему A * B даёт ошибку (или работает?) и в чём разница между * и @. Приведите пример, когда * и @ дают одинаковый результат (подсказка: диагональная матрица).
A = np.arange(6).reshape(2, 3)
B = np.arange(6).reshape(3, 2)     
A_B = A @ B
A_B_T = A.T @ B.T
A_A = A * A                                                                                                                                                        
print(f"A @ B = {A_B}, Shape = {A_B.shape}\nA.T @ B.T = {A_B_T}, Shape = {A_B_T.shape}\nA * A = {A_A}, Shape = {A_A.shape}")

# Задача 10. axis=0 vs axis=1.
# Создайте M = np.arange(12).reshape(3, 4). Вычислите M.sum(axis=0), M.sum(axis=1), M.mean(axis=0), M.mean(axis=1), M.argmax(axis=0), M.argmax(axis=1). Для каждой операции объясните одной строкой: по какой оси «свернули» и что означает результат. Проверьте на маленьком примере, что M.sum(axis=0) — это сумма по столбцам, а не по строкам.
M = np.arange(12).reshape(3, 4)
sum_axis0 = M.sum(axis=0)
sum_axis1 =M.sum(axis=1)
mean_axis0 = M.mean(axis=0)
mean_axis1 = M.mean(axis=1)
argmax_axis0 = M.argmax(axis=0)
argmax_axis1 = M.argmax(axis=1)

print(f"sum_axis0: {sum_axis0}\nsum_axis1: {sum_axis1}\nmean_axis0: {mean_axis0}\nmean_axis1: {mean_axis1}\nargmax_axis0: {argmax_axis0}\nargmax_axis1: {argmax_axis1}\nargmax_axis1: {argmax_axis1}")
mini_M = np.array([[1, 2], [3, 4]])
print(f"Маленький пример: {mini_M}")

# Задача 11. keepdims и broadcasting.
# Создайте X = np.random.default_rng(42).normal(size=(5, 3)). Вычислите X.mean(axis=0) (форма (3,)) и X.mean(axis=0, keepdims=True) (форма (1, 3)). Выполните X - X.mean(axis=0) и X - X.mean(axis=0, keepdims=True) — обе формы должны дать (5, 3). Затем посчитайте X.std(axis=1) без keepdims и с ним, и нормируйте строки: (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True). Убедитесь, что средние по строкам ≈ 0, std по строкам ≈ 1. Объясните, зачем нужен keepdims.
X = np.random.default_rng(42).normal(size=(5, 3))
mean_X = X.mean(axis=0)
mean_X_kd = X.mean(axis=0, keepdims=True)
res_1 = X - mean_X
res_2 = X - mean_X_kd
X_norm = (X - X.mean(axis=1, keepdims=True)) / X.std(axis=1, keepdims=True)
print(f"X.mean(axis=0) shape: {mean_X.shape}\nX.mean(axis=0, keepdims=True) shape: {mean_X_kd.shape}Форма res_1: {res_1.shape}, Форма res_2: {res_2.shape}\nСредние по строкам: {X_norm.mean(axis=1)}\nStd по строкам (≈1): {X_norm.std(axis=1)}")


# Блок 4. Индексация, выборки, broadcasting (задачи 12–15)

# Задача 12. Срез — view, не копия.
# Создайте a = np.arange(10). Получите b = a[2:5]. Измените b[0] = 999 и проверьте a. Затем повторите с c = a[2:5].copy() — изменился ли a? Объясните: почему это важно для численных методов (подсказка: если вы «обрезаете» данные для анализа и случайно меняете оригинал, что произойдёт с экспериментом?). Приведите пример, когда view — преимущество (экономия памяти), а когда — баг.
a = np.arange(10)
b = a[2:5]
b[0] = 999
print(f"После изменения b: a = {a}")
a = np.arange(10)
c = a[2:5].copy()
c[0] = 999
print(f"После изменения c: a = {a}")


# Задача 13. Булева маска и fancy indexing.
# Создайте a = np.random.default_rng(0).normal(size=20). Выполните:
# a[a > 0] — сколько элементов?
# a[(a > -1) & (a < 1)] — сколько?
# a[[0, 5, 10, 15]] — что это за выборка?
# a[np.abs(a) > 2] — выбросы.
a = np.random.default_rng(0).normal(size=20)
count_element = a[a > 0]
count = a[(a > -1) & (a < 1)]
fancy_idx = a[[0, 5, 10, 15]]
outliers = a[np.abs(a) > 2]
print(f"Количество элементов: {len(count_element)}\nКоличество элементов: {len(count)}\nВыборка по индексам: {fancy_idx}\nВыбросы: {outliers}")
a[a < 0] = 0
print(f"Массив после зануления отрицательных элементов:\n{a}")

# Задача 14. Broadcasting в реальной задаче.
# Создайте X = np.random.default_rng(1).normal(size=(100, 3)) (100 наблюдений, 3 признака). Нормируйте каждый столбец: вычтите среднее и разделите на std через broadcasting (без цикла). Убедитесь, что X_norm.mean(axis=0) ≈ 0 и X_norm.std(axis=0) ≈ 1. Затем посчитайте матрицу попарных евклидовых расстояний между строками: D[i, j] = ||X_norm[i] - X_norm[j]|| — через broadcasting в одну строку, без цикла. Проверьте, что D.shape = (100, 100), диагональ ≈ 0, матрица симметрична.
X = np.random.default_rng(1).normal(size=(100, 3))
X_norm = (X - X.mean(axis=0)) / X.std(axis=0)
print(f"Средние по столбцам: {X_norm.mean(axis=0)}\nStd: {X_norm.std(axis=0)}")
D = np.sqrt(np.sum((X_norm[:, np.newaxis, :] - X_norm[np.newaxis, :, :]) ** 2, axis=-1))
print(f"Форма матрицы D: {D.shape}\nСреднее на диагонали: {np.mean(np.diag(D))}\nМатрица симметрична: {np.allclose(D, D.T)}")

# Задача 15. Полный кейс: загрузка → выборка → reshape → агрегация → нормировка.
# Сгенерируйте «измерения»: rng = np.random.default_rng(42), 30 дней × 4 датчика, нормальное распределение со средним 20 и std 2, плюс один искусственный выброс (raw[7, 2] = 100).

# Выполните по шагам и выведите результат каждого:

# shape, dtype, size.
# Найдите выбросы булевой маской: np.abs(raw - raw.mean(axis=0)) > 3 * raw.std(axis=0). Сколько их?
# Замените выбросы на np.nan, затем на среднее по столбцу через np.nanmean и np.where.
# Преобразуйте (30, 4) в (4, 30) через .T, затем обратно через .T — убедитесь через np.array_equal, что данные не изменились.
# «Сплющите» в (120,) через ravel, затем восстановите (30, 4) через reshape — проверьте равенство.
# Посчитайте средние и std по каждому датчику (axis=0).
# Нормируйте каждый столбец через broadcasting. Убедитесь, что средние ≈ 0, std ≈ 1.
# Оформите как один скрипт с print на каждом шаге. В конце — короткий вывод (3–5 предложений): какие операции потребовали copy(), где сработал broadcasting, где могла возникнуть ошибка формы.\
rng = np.random.default_rng(42)
raw = rng.normal(20, 2, size=(30, 4))
raw[7, 2] = 100
raw_shape = raw.shape
raw_dtype = raw.dtype
raw_size = raw.size
print(f"Форма массива: {raw_shape}\nТип данных: {raw_dtype}\nРазмер массива: {raw_size}")

raw_mean = raw.mean(axis=0)
otklonenie = raw.std(axis=0)
raznica = np.abs(raw - raw_mean)
viborosi = raznica > 3 * otklonenie
skolko_viborosov = np.sum(viborosi)
print(f"Сколько всего выбросов нашли: {skolko_viborosov}")

raw_copy = raw.copy()
raw_copy[viborosi] = np.nan
srednee_nanmean = np.nanmean(raw_copy, axis=0)
raw_f = np.where(np.isnan(raw_copy), srednee_nanmean, raw_copy)
print(f"Значение в сломанной ячейке после замены: {raw_f[7, 2]}")

raw_T1 = raw_f.T
raw_T2 = raw_T1.T
proverka= np.array_equal(raw_f, raw_T2)
print(f"Массивы совпали после .T.T?: {proverka}")

raw_f_ravel = raw_f.ravel()
new_raw=raw_f_ravel.reshape(30, 4)
proverka2 = np.array_equal(raw_f, new_raw)
print(f"Форма после ravel: {raw_f_ravel.shape}\nМассивы совпали после reshape?: {proverka2}")

final_mean = raw_f.mean(axis=0)
final_std = raw_f.std(axis=0)
print(f"Среднее по датчикам: {final_mean}\nStd по датчикам: {final_std}")

norm_raw = (raw_f - final_mean) / final_std
print(f"Финальное среднее: {norm_raw.mean(axis=0)}\nФинальное std: { norm_raw.std(axis=0)}")