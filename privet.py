for n in range(2,5):
    print('n = ',n)
    for x in range(2,n+1):
        print('x =',x)
        print(n, '%', x, '=', n%x)
        if n%x == 0:
            print(n, 'равно', x, '*', int(n/x))
        break
    '''else:
        print(n, 'простое число')'''

