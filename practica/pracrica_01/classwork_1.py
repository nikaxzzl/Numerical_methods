import math 

def relative_error(approx, exact):
    return abs((approx - exact) / exact)

def main():
    # 1
    print(f"(π)и (3.14):\n{relative_error(3.14, math.pi)}")
    #2
    print(f"((0.1+0.2))и (0.3): {relative_error((0.1 + 0.2), 0.3)}")
    #3
    num = [0.1] * 1_000_000
    naive = sum(num)
    fsum  = math.fsum(num)
    exact = 100_000.0  

   
    print(f"Относительная ошибка naive: {relative_error(naive, exact)}")
    print(f"Относительная ошибка fsum: {relative_error(fsum, exact)}")
    
    print(f"милион sym:{naive}")
    print(f"милион fsum:{fsum}")

if __name__ == "__main__":
    main()
