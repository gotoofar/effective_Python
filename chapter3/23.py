# -*- coding=utf-8 -*-


'''
23.简单的接口应该接受函数，而不是类的实例

再次强调python的函数是一级对象，可以像值一样传递和引用
如果要按照单词长度排序，可以用函数来挂钩
'''
names=['Gimgoon','Tian','Doinb','lwx','Crisp']

names.sort(key=lambda x:len(x))
print(names)  #从短到长排序


'''
定制defaultdict类的行为，这种数据结构允许使用者提供一个函数，查询字典时里面没有想要的键
就为这个键创建新值，可以用挂钩函数为找不到键的情况打印一条信息，并返回0

'''
import collections
def log_missing():
    print('Key added')
    return 0

current={'Gimgoon':19,'Tian':15}
increments=[('Doinb',21),('Tian',5),('lwx',19)]
result=collections.defaultdict(log_missing,current)   #传入这个函数，定制未找到键的行为
print('Before:',dict(result))
for key,amount in increments:
    result[key]+=amount
print('After:',dict(result))



'''如果想给defaultdict传入一个产生默认值的挂钩，统计一共遇到了多少个缺失的键'''


def increment_with_report(current,increments):
    added_count=0
    #辅助函数使用闭包作为产生默认值的挂钩函数
    def missing():
        nonlocal added_count   #这个值的状态就保存里面
        added_count+=1
        return 0

    result=collections.defaultdict(missing,current)
    for key,amount in increments:
        result[key]+=amount
    return result,added_count



'''
但上面这个闭包用起来会有点不清晰，可以考虑封装成一个类并实现__call__方法

这样的类可以保存状态，又不像带状态的闭包一样难懂
'''
class BetterCountMissing(object):
    def __init__(self):
        self.added=0

    def __call__(self):
        self.added+=1
        return 0
counter = BetterCountMissing()
result=collections.defaultdict(counter,current)   #用的时候就像一个函数
for key,amount in increments:
    result[key] += amount












