import time

class Loggable:
    def log(self, msg):
        print(str(time.ctime()) + ": " + str(msg))

class LoggableList(list, Loggable):
    def append(self,a):
        super().append(a)
        self.log(a)


l = LoggableList()
print(l)
l.append(2)
print(l)