def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return recur_fibo(n - 1) + recur_fibo(n - 2)


def THISSHOULDBEFOUNDEASILY():
    from collections import Counter
    ctr = Counter({'birds': 200, 'lizards': 340, 'hamsters': 120})
    ctr['hamsters']
    #for i in range(3):
    #    print(recur_fibo(i))
    recur_fibo(3)


THISSHOULDBEFOUNDEASILY()
