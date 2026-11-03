import math

def experiment(f_bad, f_good, xs, f_exact):
    print(f"{'x':>10} | {'bad':>14} | {'good':>14} | "
          f"{'err_bad':>10} | {'err_good':>10}")
    print("-" * 78)
    for x in xs:
        b  = f_bad(x)
        g  = f_good(x)
        ex = f_exact(x)                    
        eb = abs(b - ex) / abs(ex) if ex else float('inf')
        eg = abs(g - ex) / abs(ex) if ex else float('inf')
        print(f"{x:>10.0e} | {b:>14.8e} | {g:>14.8e} | "
              f"{eb:>10.2e} | {eg:>10.2e}")


xs = [1e-4, 1e-2, 1.0, 1e2,1e10, 1e12, 1e14]
experiment(

    f_bad  = lambda x: math.sqrt(x + 1) - math.sqrt(x),
    f_good = lambda x: 1.0 / (math.sqrt(x + 1) + math.sqrt(x)),
    xs     = xs,
    f_exact= lambda x: 1.0 / (math.sqrt(x + 1) + math.sqrt(x))
)