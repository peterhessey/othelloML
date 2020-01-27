class A():
    def __init__(self, value):
        self.value = value

    def foo1(self):
        return self.foo2()

    def foo2(self):
        return self.value * 2

class B(A):
    def __init__(self, value):
        super().__init__(value)

    def foo1(self):
        return A.foo1(self)
        
    def foo2(self):
        return self.value + 3


if __name__=="__main__":
    my_object = B(10)
    print('Value is', my_object.foo1())