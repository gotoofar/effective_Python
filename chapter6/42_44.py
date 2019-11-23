# -*- coding=utf-8 -*-

'''
42.用functools.wraps定义函数修饰器
修饰器能够在那个函数执行之前以及执行之后分别运行一些附加代码，
使得开发者可以在修饰器里面访问并修改原函数的参数及返回值，以
实现约束语义、调试程序、注册函数等目标

这个效果就相当于以该函数作为参数调用修饰器，再把修饰器的结果返回给同名函数

fibonacci = trace(fibonacci)
'''

def trace(func):
    def wrapper(*args,**kwargs):
        result=func(*args,**kwargs)
        print('%s(%r,%r)->%r'%(func.__name__,args,kwargs,result))
        return result
    return wrapper

@trace
def fibonacci(n):
    if n in (0,1):
        return n
    return (fibonacci(n-2)+fibonacci(n-1))

'''
这样导致fibonacci名称不是他自己了，而变成了wrapper
比如 help(fibonacci) 都用不了
这种可以用内置的functools模块中的wraps辅助函数来解决
它本身也是修饰器，可以把与内部函数相关的重要元数据全部复制到外围函数

为了维护函数的接口，修饰后的函数必须保留原函数的某些标准Python属性，例如__name__ 和__module__
'''

def trace(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        pass
    return wrapper





'''
43.用contextlib和with来改写可复用的try/finally

用下面这个打印日志作为栗子
默认的信息级别是WARNING 所以只会打印中间那句
'''
def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('Mone debug data')

'''
把一个辅助函数写成可以用with调用的模式
就是用 contextmanager把它写成一个用with的情境管理器
会在运行with块内的代码之前临时修改信息级别，等到with块结束再回复
'''
import contextlib
import logging

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield     #这里就是with块中的语句要展开执行的地方
    finally:
        logger.setLevel(old_level)


with debug_logging(logging.DEBUG):
    my_function()    #等级调整到了DEBUG 会把三条都输出



'''
还可以设计成像with open as 打开文件的模式
在yield的语句向with语句返回一个值，会赋给由as关键字所指定的变量
with open('a.txt','w') as handle:
    handle.write('This is some data!')
'''

@contextmanager
def log_level(level,name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with log_level(logging.DEBUG,'my-log') as logger:
    logger.debug('This is my message!')  #因为在with里得到的这个是改过级别的，所以可以打印出
    logging.debug('This will not print')





'''
44.用copyreg 实现可靠的pickle操作

以一个游戏玩家状态作为例子

'''
import pickle
class GameState(object):
    def __init__(self):
        self.level = 0
        self.lives = 4

state = GameState()
state.level+=1
state.lives-=1

state_path = 'game_state.bin'
with open(state_path,'wb') as f:
    pickle.dump(state,f)

#如果想把文件还原成对象
with open(state_path,'rb') as f:
    state_after = pickle.load(f)
print(state_after.__dict__)

'''
假如游戏更新了，玩家有一个得分属性，而之前保存的文件里只有等级和生命属性
那么从文件还原的对象就只有之前的属性了
这里用copyreg模块来解决
首先写辅助函数
'''
import copyreg
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state,(kwargs,)

def unpickle_game_state(kwargs):
    return GameState(**kwargs)

#用copyreg来注册
copyreg.pickle(GameState,pickle_game_state)

#序列化和反序列化都照常进行
state = GameState()
state.points +=1000
serialized = pickle.dump(state)
state_after = pickle.loads(serialized)


#这时候给GameState加属性
class GameState(object):
    def __init__(self,level=0,lives=4,points=0,magic=5):
        pass



'''
用版本号来管理类
如果一个属性在后期被移除，那么通过带有默认值的参数来进行反序列化的方案就会出错
比如去掉lives这一个属性
要在pickle_game_state里加一个表示版本号的参数
新版的对象进行pickle的时候，version会设置为2
'''
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version']=2
    return unpickle_game_state,(kwargs)

def unpickle_game_state(kwargs):
    version= kwargs.pop('version',1)
    if version==1:
        kwargs.pop('lives')
    return GameState(**kwargs)


'''
类名修改之后，会影响pickle
比如把GameState改成BetterGameState后，之前的对象进行反序列化操作就会出错
这个copyreg可以搞定

'''








