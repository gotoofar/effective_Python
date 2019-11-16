# -*- coding=utf-8 -*-

'''
用 __getattr__  __getattribute__  和 __setattr__实现按需生成的属性

不用先定义属性，调用的时候再动态处理，用 __getattr__就可以
'''
class LazyDB(object):
    def __init__(self):
        self.exists=5

    def __getattr__(self, name):   #访问的属性不存在时 就调用这个
        value = 'Value for %s'% name
        setattr(self,name,value)
        return value
'''
如果想添加功能，每次调用getattr的时候打印日志
就要注意  子类要用super得到父类的属性值
'''
class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)'%name)
        return super().__getattr__(name)



'''
另一个挂钩 __getattribute__ 和上面的不一样，只要是调用属性 都会触发
下面这个类用这个方法记录每次调用的时间
'''
class ValidatingDB(object):
    def __init__(self):
        self.exists=5

    def __getattribute__(self, name):    #每次访问属性都用到
        print('Called __getattribute__(%s)'% name)
        try:
            return super().__getattribute__(name)    #按照往常 返回要的数据
        except AttributeError:
            value = 'Value for %s'%name     #没有就设置一个
            setattr(self,name,value)
            return value

'''
只要是赋值 不论直接赋值或是调用setattr  都会触发 __setattr__方法

'''
class SavingDB(object):
    def __setattr__(self,name,value):
        # do something
        super().__setattr__(name,value)

class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s,%r)'%(name,value))
        super().__setattr__(name,value)




'''
用getattribute的时候要注意不要造成反复递归

'''
class BrokenDictionaryDB(object):
    def __init__(self,data):
        self._data=data

    def __getattribute__(self, name):
        pprint('Called __getattribute__(%s)'% name)
        return self._data[name]    #这个因为调用又触发 __getattribute__  无限循环递归


#解决办法是 从实例的属性字典里面直接获得值，

class BrokenDictionaryDB(object):
    def __init__(self,data):
        self._data=data

    def __getattribute__(self,name):
        data_dict = super().__getattribute__('_data')
        return data_dict[name]
#类似的，setattr也会造成这种问题，可以通过 super().__setattr__ 来完成



