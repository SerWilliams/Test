key, value, str1, str2 = list(input()), list(input()), list(input()), list(input())
for i in str1:
    print(value[key.index(i)], end = '')
print()
for j in str2:
    print(key[value.index(j)], end = '')
print()
