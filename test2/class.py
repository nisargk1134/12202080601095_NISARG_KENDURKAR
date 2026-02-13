class A:
    def __new__(cls):
        print("Constructor Used Here")
        return super(A, cls).__new__(cls)


A()


class B:
    def __init__(self, name, age):
        self.name = name
        self.age = age


c = B("Nisarg", 22)
print(c.name)
print(c.age)


# Default Constructor


class C:
    def __init__(self):
        self.name = "Renault"
        self.model = "Duster"
        self.year = 2014


d = C()
print(d.name)
print(d.model)
print(d.year)


# Parameterized Constructor


class D:
    def __init__(self, name, model, year):
        self.name = name
        self.model = model
        self.year = year


e = D("Nissan", "Sunny", 2012)
print(e.name)
print(e.model)
print(e.year)


# Destructor


class E:
    def __del__(self):
        print("DIE")


E()
