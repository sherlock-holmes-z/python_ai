class Student:
    def __init__(self, name, age, chinese, math, english):
        self.name = name
        self.age = age
        self.chinese = chinese
        self.math = math
        self.english = english

    def __str__(self):
        total = self.chinese + self.math + self.english
        return f"name:{self.name},chinese:{self.chinese},math:{self.math},english:{self.english},total_score:{total}"

    def update_score(self, chinese=None, math=None, english=None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english


class EduManagement:
    system_name = "教务管理系统"
    system_version = "1.0.0"

    stu_dict = {}

    def __init__(self):
        pass

    def stu_count(self):
        print(f"学生数量{len(self.stu_dict)}")

    def add_stu(self, stu: Student):
        self.stu_dict[stu.name] = stu

    def del_stu(self, name):
        del self.stu_dict[name]

    def get_stu(self, name):
        stu = self.stu_dict.get(name)
        if stu is None:
            print("没有这个学生")
        else:
            print(stu)

    def update_stu(self, stu: Student):
        self.stu_dict[stu.name] = stu


if __name__ == "__main__":
    student = Student("zhangsan", 17, 10, 20, 30)
    print(student)
    student.update_score(chinese=100)
    print(student)

    edu_management = EduManagement()
    student2 = Student('lisi',20,11,12,13)
    edu_management.add_stu(student)
    edu_management.add_stu(student2)

    edu_management.stu_count()

    edu_management.get_stu("zhangsan")

    student = Student("zhangsan", 17, 10, 10, 10)
    edu_management.update_stu(student)
    edu_management.get_stu("zhangsan")

    edu_management.del_stu("zhangsan")

    edu_management.stu_count()
