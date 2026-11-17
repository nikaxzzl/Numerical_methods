import numpy as np
import matplotlib.pyplot as plt
print("Задание №1")
k = np.arange(7)
angles = 2 * np.pi * k / 6
points = np.column_stack([np.cos(angles), np.sin(angles)])
angle = np.deg2rad(45)
rotate = np.array([
    [np.cos(angle), -np.sin(angle)],
    [np.sin(angle),  np.cos(angle)]
])
reflect = np.array([
    [0.0, 1.0],
    [1.0, 0.0]
])
rotated = points @ rotate.T
reflected = points @ reflect.T
fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(points[:, 0], points[:, 1], 'o-', color='gray', lw=2, label='Исходный')
ax.plot(rotated[:, 0], rotated[:, 1], 'o-', color='steelblue', lw=2, label='Поворот на 45°')
ax.plot(reflected[:, 0], reflected[:, 1], 'o--', color='crimson', lw=2, label='Отражение от y = x')
ax.axline((0, 0), slope=1, color='green', linestyle=':', alpha=0.6, label='Прямая y = x')
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left')
ax.set_title('Задача 1: Поворот и отражение правильного шестиугольника')
plt.tight_layout()
plt.show()

print("Задание №2")
rng = np.random.default_rng(42)
points = rng.uniform(-2.0, 2.0, size=(200, 2))
points_h = np.hstack([points, np.ones((len(points), 1))])
scale = np.array([
    [1.5, 0.0, 0.0],
    [0.0, 0.5, 0.0],
    [0.0, 0.0, 1.0]
])
angle = np.deg2rad(60)
rotate = np.array([
    [np.cos(angle), -np.sin(angle), 0.0],
    [np.sin(angle), np.cos(angle), 0.0],
    [0.0, 0.0, 1.0]
])
translate = np.array([
    [1.0, 0.0, 1.0],
    [0.0, 1.0, -1.0],
    [0.0, 0.0, 1.0]
])

forward = translate @ rotate @ scale
transformed_h = points_h @ forward.T
transformed = transformed_h[:, :2]
translate_back = np.array([
    [1.0, 0.0, -1.0],
    [0.0, 1.0, 1.0],
    [0.0, 0.0, 1.0]
])
angle_back = np.deg2rad(-60)
rotate_back = np.array([
    [np.cos(angle_back), -np.sin(angle_back), 0.0],
    [np.sin(angle_back), np.cos(angle_back), 0.0],
    [0.0, 0.0, 1.0]
])
scale_back = np.array([
    [1.0 / 1.5, 0.0, 0.0],
    [0.0, 1.0 / 0.5, 0.0],
    [0.0, 0.0, 1.0]
])
backward = scale_back @ rotate_back @ translate_back
restored_h = transformed_h @ backward.T
restored = restored_h[:, :2]
is_equal = np.allclose(points, restored, atol=1e-12)
print("Восстановленные точки совпадают с исходными:", is_equal)
fig, ax = plt.subplots(figsize=(8, 7))
ax.scatter(points[:, 0], points[:, 1], color='gray', alpha=0.5, s=30, label='Исходные')
ax.scatter(transformed[:, 0], transformed[:, 1], color='crimson', alpha=0.7, s=25, label='Преобразованные')
ax.scatter(restored[:, 0], restored[:, 1], facecolors='none', edgecolors='steelblue', s=55, lw=1.2, label='Восстановленные')
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left')
ax.set_title('Задача 2: Композиция и обратное преобразование облака точек')
plt.tight_layout()
plt.show()
