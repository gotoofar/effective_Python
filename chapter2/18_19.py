# -*- coding=utf-8 -*-


'''
18.用数量可变的位置参数减少视觉杂讯

'''
def log(message,*values):
    if not values:
        print(message)
    else:
        values_str=','.join(str(x) for x in values)
        print('%s:%s'%(message,values_str))
log('My numbers are ',1,2)
log('Hi there')  #不传入也不要紧

'''把已有的列表传给带有变长参数的函数，前面加个*'''
favorites=[7,33,99]
log('Favorite colors',*favorites)

'''
接受数量可变的位置参数，带来两个问题
1.变长参数在传给函数时总要先化成元组，如果传入带有*操作符的生成器，生成器完整
迭代一轮，可能因为量崩溃
'''
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it=my_generator()
my_func(*it)

'''
2.如果给函数添加新的位置参数，必须修改函数代码
'''
def log2(sequence,message,*values):
    if not values:
        print('%s: %s'%(sequence,message))
    else :
        values_str=','.join(str(x) for x in values)
        print(('%s:%s:%s'%(sequence,message,values_str)))
log(1,'Favorites',7,33)
log('Favorite numbers',7,33)  #  因为位置参数 导致7对上了message这个输入，如果要加的话，建议用关键字参数




'''
19.用关键字参数来表达可选行为，在调用时指明参数配置
注意： 位置参数必须出现在关键字参数之前
      每个参数只能指定一次
'''
def remainder(number,divisor):  #这里还可以设定默认值
    return number % divisor
#以下等效
remainder(20,7)
remainder(20,divisor=7)
remainder(number=20,divisor=7)
remainder(divisor=7,number=20)

#以下错误，位置参数必须出现在关键字参数之前
remainder(number=20,7)  #编辑时就会报错

#每个参数只能指定一次，这样会给number赋两次
remainder(20,number=7)




