# -*- coding=utf-8 -*-

'''
22.尽量用辅助类来维护程序的状态
例如一个字典里包含另一个字典时，或者元组过长时，用辅助类会更清晰

这个栗子是 一个班里有很多学生，每个学生有几门课，科目有分数和权重，如果用字典表示名单
再用嵌套字典表示这个学生的几个科目分数和权重（元组） 这样会非常复杂
'''

#科目类 包含一系列考试成绩
class Subject(object):
    def __init__(self):
        self._grades=[]

    def report_grade(self,score,weight):
        self._grades.append(Grade(score,weight))   #这里用上了具名元组

    def average_grade(self):
        total,total_weight=0,0
        for grade in self._grades:
            total+=grade.score*grade.weight
            total_weight+=grade.weight
#学生类  包含正在学习的课程
class Student(object):
    def __init__(self):
        self._subjects={}

    def subject(self,name):
        if name not in self._subjects:
            self._subjects[name]=Subject

    def average_grade(self):
        total,count=0,0
        for subject in self._subjects.values():
            total+=subject.average_grade()
            count+=1
        return total/count

#包含所有学生考试成绩的容器类
class Gradebook(object):
    def __init__(self):
        self._students={}

    def student(self,name):
        if name not in self._students:
            self._students[name] = Student()
            return self._students[name]

book=Gradebook()
albert=book.student('Albert Einstein')
math=albert.subject('Math')
math.report_grade(80,0.10)

print(albert.average_grade())







