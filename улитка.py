n = int(input('Введите число\n:'))
a = [[0 for i in range(n)] for j in range(n)]
d = 1
kr = 1
while d <= n*n:
    for i in range(kr - 1, n + 1 - kr):
        if i == kr - 1:
            for j in range(kr - 1, n + 1 - kr):               
                a[i][j] = d
                d += 1
        else:
            a[i][n - kr] = d
            d += 1
    for i in range(n - kr, kr - 1, -1):
        if i == n - kr:
            for j in range(n - 1 - kr, kr - 2, -1):
                a[i][j] = d
                d += 1
        else:
            a[i][kr - 1] = d
            d += 1
    kr += 1
for i in range(n):
    for j in range(n):
        print(a[i][j], end = ' ')
    print()
