
def function():
    pass

class Student:
    

    def __init__(self):
        self.classes = []
        print('init Student')

    def print_classes(self):
        print(self.classes)

    def __getitem__(self, key):
        print(key)
        return 'Yolo'



s1 = Student()

s1.classes.append('Math')
s1.classes.append('Physics')
s1.classes.append('Chemistry')

s1.age=20
print(s1.age)

s1.print_classes()

x = s1['sdsss']
print(x)

print(s1.classes)
print(s1.classes[2])
s2 = Student()
print(s2.classes)

print(type(s1))

