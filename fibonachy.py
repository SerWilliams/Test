#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      lizunkov_sa
#
# Created:     14.07.2017
# Copyright:   (c) lizunkov_sa 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def fib(n):
    result = [1]
    a,b = 0,1
    c = 0
    while b < n:
        c += 1
        result.append(b)
        a,b = b,a+b
    return result


#n = int(input('Введите число:\n'))
print(fib(2000))

