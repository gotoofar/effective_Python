# -*- coding=utf-8 -*-


'''
46.使用内置算法与数据结构


(1).双向队列
list在头部插入或移除元素需要线性级的时间
'''
from collections import deque

fifo=deque()
fifo.append(1)
x=fifo.popleft()


'''
(2).标准的字典是无序的，因为是用哈希表的实现方式导致的
而collections模块中的 OrderedDict类是有序字典，按照键的插入顺序保持次序

'''
#无序
from collections import OrderedDict
a=OrderedDict()
a['foo']=1
a['bar']=2
b=OrderedDict()
b['foo']='red'
b['bar']='blue'

for value1,value2 in zip(a.values(),b.values()):
    print(value1,value2)



'''
(3).使用带有默认值的字典
defaultdict可以给不存在的键返回默认值，如果给int则默认值为0

'''
from collections import defaultdict
stats = defaultdict(int)
stats['my_counter']+=1



''' 
(4).堆队列（优先级队列）  heapq操作所耗费的时间与列表长度成正比
'''
from heapq import heappush,heapify

a=[]
heapify(a)
heappush(a,5)
heappush(a,3)
heappush(a,7)
heappush(a,4)
print(a[0])




'''
(5).二分查找
'''
x=list(range(10**6))
i = x.index(991234)
i=bisect_left(x,991234)   #二分查找数字的位置


'''
(6).与迭代器有关的工具

    *能够把迭代器连接起来的函数：
    chain  多个迭代器顺序连成一个迭代器
    cycle  无限重复一个迭代器的各个元素
    tee    一个迭代器拆分成多个平行迭代器
    zip_longest  与内置zip相似，但可以处理长度不同的迭代器
    
    
    *能够从迭代器中过滤元素的函数
    islice   不进行复制的前提下，根据索引值来切割迭代器
    takewhile  在判定函数为True的时候，从迭代器中逐个返回
    dropwhile  从判定函数初次为False的地方开始逐个返回元素
    filterfalse  与内置的filter相反 谁不符合返回谁
    
    
    *能够把迭代器中元素组合起来的函数
    
    product  根据迭代器元素计算笛卡尔积并将其返回
    permutations  用迭代器中的元素构成长度为N的各种有序排列，并将所有排列形式返回给调用者
    combination   和permutations很像，但是无序


'''


