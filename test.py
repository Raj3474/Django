class A:

    @staticmethod
    def display():
        print('Class A')

class B:

    @staticmethod
    def display():
        print('Class B')

class C(A, B):

    pass

c = C()
c.display()

print(C.mro())


