def get(name, var):
    if name == 'None':
        return name
    else:
        if var in ns[name][1:]:
            return name
        else:
            return get(ns[name][0], var)
ns = {'global':['None']}
result = []
n = int(input())
for i in range(n):
    oper, nmsp, var = map(str, input().split())
    if oper == 'add': ns[nmsp].append(var)
    if oper == 'create': ns[nmsp] = [var]
    if oper == 'get': result.append(get(nmsp, var))
for i in result:
    print(i)
