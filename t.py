import copy


class A:
    def __init__(self, a):
        self.a = a
        self.next = None

    def __str__(self):
        return "{} {}".format(self.a,self.next)


a1 = A("1")
a2 = A("2")
a3 = A("3")
a1.next = a2

b = [a1, a2, a3]

c = copy.copy(b)

print(c[0])