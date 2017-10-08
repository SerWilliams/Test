class MoneyBox:
    def __init__(self, capacity):
        self.capacity = int(capacity)
        self.box = 0
# конструктор с аргументом – вместимость копилки

    def can_add(self, v):
        if self.box + int(v) <= self.capacity:
            return True
        else:
            return False
# True, если можно добавить v монет, False иначе

    def add(self, v):
        if self.can_add(v):
            self.box += v
# положить v монет в копилку


my_mbox1 = MoneyBox(10)
print("Capacity my Money Box is " + str(my_mbox1.capacity))
print("Count money in my box " + str(my_mbox1.box))
print(my_mbox1.can_add(9))
my_mbox1.add(9)
print("Count money in my box " + str(my_mbox1.box))
print(my_mbox1.can_add(2))
my_mbox1.add(2)

print("Count money in my box " + str(my_mbox1.box))



