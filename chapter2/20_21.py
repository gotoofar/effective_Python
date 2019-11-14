# -*- coding=utf-8 -*-
import datetime

'''
20. 在想用动态默认值参数的时候，用None和文档字符串

'''
def log(message,when=datetime.now()):  #这个取时间其实是在函数定义时就确定的  这是个可变类型(mutable)
    print('%s: %s'%(when,message))

log('Hi there!')  #两次的时间戳一样
sleep(0.1)
log('Hi there!')

'''为了让两次时间不同，应该默认为None'''

def log1(message,when=None):
    when=datetime.now() if when is None else when
    print('%s: %s' % (when, message))


'''如果默认的是一个空列表，也会出现这种情况
如果两次都尝试调用默认空列表，他们调用的其实是同一个
'''
def decode(data,default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default  #返回的两次用的是同一个{}
#默认为None，在文档字符串里描述默认值的实际行为
def decode(data,default=None):
    if default is None:
        default={}
    try:
        return json.loads(data)
    except ValueError:
        return default


'''
21.给一些参数定下规则，只能以关键字参数，不能以位置参数
这样调用时比较明晰

关键字参数前面放一个* 这样调用的时候尝试用位置参数会报错
Python2里面没有这种写法，只有用 **kwargs
'''

def safe_division_c(number,divisor,*,ignore_overflow=False,ignore_zero_division=False):
    try:
        return number/divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise







