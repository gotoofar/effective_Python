# -*- coding=utf-8 -*-

'''
14.尽量使用异常来表示特殊情况，而不要返回None
因为在判断 if not 时，0和None得到一样的结果

'''
def divide(a,b):
    try:
        return a/b
    except ZeroDivisionError:
        return None

result=divide(x,y)

'''if not result:
if result is None: 
这两种都可以判断，但None和0对于条件表达式都是False
有两种办法可以解决
1.返回二元组  表示状态和结果
2.异常抛给上一级
'''

#1
def divide(a,b):
    try:
        return True,a/b
    except ZeroDivisionError:
        return False,None

success,result=divide(x,y)

#2
def divide(a,b):
    try :
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

x,y=5,2
try:
    result=divide(x,y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result %.1f'%result)


'''
15.在闭包里使用外围作用域的变量
闭包是一种定义在某个作用域中的函数，这个函数引用了作用域里面的变量
python的函数是一级对象，可以把函数赋给变量，把函数当作参数传给其他函数等
python使用特殊的规则来比较两个元组，按照位置逐个比较

下面的例子是把一个列表排序，使在另一个group里面的数字排前面
'''
def sort_priority(values,group):
    def helper(x):
        if x in group:
            return (0,x)
        return (1,x)
    values.sort(key=helper)


#如果想有一个返回标志位，表示列表里是否出现了群组里的高级元素，按理说 下面这种翻转标志位的做法是可以的
def sort_priority2(values,group):
    found=False
    def helper(x):
        if x in group:
            found=True
            return (0,x)
        return (1,x)
    values.sort(key=helper)
    return found  #这里的found并不会因为里面翻转为True而翻转，因为helper里定义的相当于一个新变量

'''这样的称为 scoping bug  防止函数中的局部变量污染函数外模块
python3中可以用nonlocal获取闭包中的数据，但是在复杂情况下不应该使用，以免影响外模块
'''
def sort_priority2(values,group):
    found=False
    def helper(x):
        nonlocal found   #表示这就是外面那个found
        if x in group:
            found=True
            return (0,x)
        return (1,x)
    values.sort(key=helper)
    return found

'''
写成一个类会更加清晰
'''
class Sorter(object):
    def __init__(self,group):
        self.group=group
        self.found=False
    def __call__(self, x):
        if x in self.group:
            self.found=True
            return (0,x)
        return (1,x)
sorter=Sorter(group)
numbers.sort(key=sorter)  #__call__ 使得类可以当作函数使用

#python2 里面是不支持nonlocal关键字的，用列表也可以实现

def sort_priority3(number,group):
    found=[False]
    def helper(x):
        if x in group:
            found[0]=True
            return (0,x)
        return (1,x)
    number.sort(key=helper)
    return found[0]




