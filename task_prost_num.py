import itertools

def primes():
    x = 2
    lst=[]
    while True:
        for j in lst:
            if x % j == 0:
                break
        else:
            yield x
            lst.append(x)
        x += 1
    
    

print(list(itertools.takewhile(lambda x : x <= 31, primes())))
