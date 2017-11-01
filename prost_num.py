def primes(end):
    a = [i for i in range(end+1)]
    a[1] = 0
    lst = []
    i = 2
    while i <= end:
        if a[i] != 0:
            lst.append(a[i])
            for j in range(i, end+1, i):
                a[j] = 0

        i += 1
    return len(lst)


n = int(input())                
print(primes(n))        
            
