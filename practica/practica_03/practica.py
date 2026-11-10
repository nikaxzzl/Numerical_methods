import numpy as np
import numpy as np

mas = np.arange(24).reshape(6, 4)
print(mas.shape)
print(mas.ndim)
print(mas.size)
print(mas.dtype)

b = mas.reshape(4, 6)
c = mas.reshape(2, 3, 4)
d = c.reshape(24)

print(b.shape)             
print(c.shape)        
print(d.shape)      
print(np.array_equal(mas, b))
print("a == c :", np.array_equal(mas, c))          
print("a.ravel() == d:", np.array_equal(mas.ravel(), d))

#3
kol = mas[:, 2]
kol[0] = 999
print(mas[0, 2])

 #4
mas = np.arange(24).reshape(6, 4) # сброс!
mask = mas > 10
select = mas[mask]
print(select.sum() / len(select))

#5
row = mas.sum(axis=1, keepdims=True) / mas.shape[1] 
center = mas - row
print(center.shape)              
print(center.sum(axis=1))