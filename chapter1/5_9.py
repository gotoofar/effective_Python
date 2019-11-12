# -*- coding=utf-8 -*-
import numpy as np
'''
5.切割序列
切割时start和end索引越界不会出现问题
'''
a=[1,2,3,4,5,6,7]
out_range=a[:20]  #允许  但是单个索引访问不行


'''
python里先切片，再改变切片不会影响原列表
numpy 里面的切片只是一个视图 是会改变的 想要复制的话要用.copy()

'''
b=a[3:6]   #切下就复制了
a[2:5]=[12,13]  #赋值长度和索引不一样也可以，原列表会扩张或收缩   注意右边必须是个可迭代的（列表）



c=np.arange(10)
d=c[3:7]   #切下仅为视图，改变之后原列表也改变
d[1:3]=[99,99]   #赋的值如果是列表时，长度必须一样，如果是一个值，那长度随意



a=[1,2,3]
b=a   #直接赋值不会拷贝，而是指向同一块
print(b)
a[:]=[4,5,6]   #相当于把a整个赋值，b也受到影响
assert a is b
print(b)


'''
6.[start:end:stride]不应该同时指定
范围切割和步进切割可以分开 （我倒觉得没啥）
'''
odds=a[::2]
evens=a[1::2]

x=a[::-1]  #这种方法不适用于 unicode


'''
7.列表推导式取代map,filter
首先看一下map/filter/reduce用法
'''

def f(x):
    return x*x
r=list(map(f,[1,2,3,4,5]))   #第一个参数是函数


#reduce(f,[x1,x2,x3])=f(f(x1,x2),x3)
from functools import  reduce
def add(x,y):
    return x+y
print(reduce(add,[1,3,5,7]))

#filter是把列表中符合条件的保留下来
#保留奇数
def is_odd(n):
    return n%2==1
list(filter(is_odd,[1,2,3,4,5]))

'''
如果想把列表里的都平方，map用lambda的做法是  squares=map(lambda x:x**2,a) 
但是还是有些不明确，列表推导式如下
'''
squares=[x**2 for x in a]

#字典也可以用类似的方法
cc={'gdd':1,'hhaei':2,'tt':3}
ra_dict={rank:name for name,rank in cc.items()}
print(ra_dict)



'''
8.多个表达式的列表推导可以用，但考虑到可读性应尽量少，用循环代替其中的几个
比如下面的 把矩阵里的值平方
还有把本身能够被3整除 所在行各元素之和大于10的单元格挑出来
'''
matrix=[[1,2,3],[4,5,6],[7,8,9]]
squared=[[x**2 for x in row] for row in matrix]
print(squared)

filtered=[[x for x in row if x%3==0] for row in matrix if sum(row)>=10]



'''
9.数据量大时，生成器比列表推导更好
'''
x=[4,6,7,8]
it=(ii**2 for ii in x)
#还可以组合
it=((ii,ii*2) for ii in x)
print(next(it))

