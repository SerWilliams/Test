from datetime import *
n = [int(i) for i in input().split()]
new_date = (date(n[0], n[1], n[2]) + timedelta(days=int(input()))).timetuple()
for i in range(3):
    print(new_date[i], end = ' ')

