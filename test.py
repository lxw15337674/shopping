class a():
    a = 1
    def __init__(self):
        self.a = 2
        print(self.a)
    def b(self):
        self.__init__()

if __name__ == '__main__':
    a.b()