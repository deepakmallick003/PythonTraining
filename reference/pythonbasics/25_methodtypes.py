class Student:
    school = 'Telusko'

    def __init__(self, m1, m2, m3):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

    def avg(self):
        return (self.m1 + self.m2 + self.m3) / 3

    def get_m1(self):
        return self.m1

    def set_m1(self, value):
        self.m1 = value

    @classmethod
    def get_school(cls):
        return cls.school

    @staticmethod
    def info():
        print('this is a static method')


s1 = Student(34, 47, 32)
s2 = Student(89, 32, 112)

print(s1.avg())
print(Student.get_school())
Student.info()