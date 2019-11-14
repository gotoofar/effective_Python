# -*- coding=utf-8 -*-


'''
16.考虑用生成器来改写直接返回列表的函数

例如下面这个函数，传入一句话，返回每个单词首字母的位置
'''
def index_words(text):
    result=[]
    if text:
        result.append(0)
    for index,letter in enumerate(text):
        if letter==' ':
            result.append(index+1)
    return result

'''
有两个问题
一是代码太冗余，用生成器更加清晰
我们想强调的不是result的append，而是index的获取
'''
def index_words_iter(text):
    if text:
        yield 0
    for index,letter in enumerate(text):
        if letter==' ':
            yield index+1

address="Four and seven years ago"
result=list(index_words_iter(address))

'''
二是如果输入量很大，把他们全弄一个列表里会导致崩溃
下面这样处理一整个文件都不会崩溃
'''
def index_file(handle):
    offset=0
    for line in handle:
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

with open(txt_path,'r') as f:
    it=index_file(f)
    result=islice(it,0,3)   #这个函数会影响生成器的噢，切片之后生成器就往后推了
    print(list(result))



'''
17.迭代器只能产生一轮结果，在抛出过StopIteration异常的迭代器或生成器上继续
迭代第二轮是没有结果的

'''
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

it=read_visits('xxxx.txt')
print(list(it))
print(list(it))   #这个输出为空[]

def normalize(numbers):
    sum=sum(numbers)
    for value in numbers:  #这个迭代器已经被耗尽了，无结果
        sum+=value
    return sum
#如果想要它起作用，传入一个迭代器，先转为list再迭代
def normalize1(numbers):
    numbers=list(numbers)  #存在一个问题，如果量特别大可能导致崩溃
    sum = sum(numbers)
    for value in numbers:
        sum+=value
    return sum

'''
有两种解决方案
一是传入的不是一个迭代器，而是一个函数，每次返回一个新迭代器
二是新编一种实现迭代器协议的容器类,令自己的类把__iter__方法实现为生成器

'''
def normalize_func(get_iter):  #传入的是一个函数名
    total=sum(get_iter())  #调用一次
    for value in get_iter():  #调用另一次
        pass
    return total
result=normalize_func(lambda: read_visits(path))  #调用时就要把之前的迭代器变成匿名函数


class ReadVisits(object):
    def __init__(self,data_path):
        self.data_path=data_path

    def __iter__(self):  #实现iter
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

#检测输入的值是否为迭代器本身  有一个  if iter(numbers) is iter(numbers) 两次调用iter如果返回相同则是迭代器
def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers):
        raise TypeError('必须是个容器')
    total = sum(numbers)
    result=[]
    for value in numbers:
        percent=100*value/total
        result.append(percent)
    return result





