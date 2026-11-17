import timeit
import tracemalloc
import matplotlib.pyplot as plt
print("Задание №1")
sizes = [100, 1000, 10000]
checks = 1000
num = -1

list_times = []
set_times = []

for n in sizes:
    lst = list(range(n))
    st = set(range(n))

    raw_list = timeit.repeat(
        "num in lst",
        globals={"num": num, "lst": lst},
        number=checks,
        repeat=5
    )
    raw_set = timeit.repeat(
        "num in st",
        globals={"num": num, "st": st},
        number=checks,
        repeat=5
    )

    t1 = min(raw_list) / checks * 1_000_000
    t2 = min(raw_set) / checks * 1_000_000

    list_times.append(t1)
    set_times.append(t2)

    print(f"n={n}: list = {t1:.3f} мкс, set = {t2:.3f} мкс, set быстрее в {t1 / t2:.1f} раз")

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(sizes, list_times, marker="o", label="x in list")
ax.plot(sizes, set_times, marker="s", label="x in set")

ax.set_yscale("log")
ax.set_xlabel("Размер коллекции (n)")
ax.set_ylabel("Время одной проверки (мкс)")
ax.set_title("Сравнение времени поиска: list vs set")
ax.legend()
ax.grid(True, which="both", alpha=0.2)

plt.tight_layout()
plt.show()

# #2
print("Задание №2")
sizes = [100_000, 1_000_000]

approaches = {
    "Цикл с append": "squares = []\nfor num in range(N):\n    squares.append(num * num)",
    "List comprehension": "squares = [num * num for num in range(N)]",
    "map + lambda": "squares = list(map(lambda num: num * num, range(N)))",
}

execution_times_ms = {label: [] for label in approaches}
peak_memory_mb = {label: [] for label in approaches}

for count in sizes:
    for label, code_snippet in approaches.items():
        # Замер времени (мс)
        raw_times = timeit.repeat(code_snippet, globals={"N": count}, number=1, repeat=5)
        execution_times_ms[label].append(min(raw_times) * 1000)

        # Замер пиковой памяти (МБ)
        tracemalloc.start()
        exec(code_snippet, {"N": count})
        current_bytes, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_mb[label].append(peak_bytes / (1024 * 1024))

# Два графика рядом
figure, (time_ax, memory_ax) = plt.subplots(1, 2, figsize=(13, 5))

# График времени: линии с маркерами
for label in approaches:
    time_ax.plot(sizes, execution_times_ms[label], "o-", label=label)

time_ax.set_xlabel("N")
time_ax.set_ylabel("Время (мс)")
time_ax.set_title("Время выполнения")
time_ax.legend()
time_ax.grid(True, alpha=0.3)

# График памяти: столбцы
bar_positions = range(len(sizes))
bar_width = 0.25

for idx, label in enumerate(approaches):
    shifted_positions = [pos + (idx - 1) * bar_width for pos in bar_positions]
    memory_ax.bar(shifted_positions, peak_memory_mb[label], bar_width, label=label)

memory_ax.set_xlabel("N")
memory_ax.set_ylabel("Пиковая память (МБ)")
memory_ax.set_title("Потребление памяти")
memory_ax.set_xticks(list(bar_positions))
memory_ax.set_xticklabels([f"N={count}" for count in sizes])
memory_ax.legend()
memory_ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
print("Вывод: По памяти все три варианта почти одинаковы, получается один и тот же список из N чисел. Быстрее всего list comprehension, он работает на уровне C и обходится без append. map + lambda медленнее , потому что lambda вызывается для каждого элемента.")