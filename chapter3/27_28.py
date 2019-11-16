# -*- coding=utf-8 -*-


'''
27. 多用public属性 少用private属性

如果想保护这个数据，就用 ss.__name 把数据变为私有变量，外部无法访问（其实用 _Student__name可以访问，但不建议 ）
子类也无法访问父类的私有变量'''

#子类直接访问 不行的
class MyParentObject(object):
    def __init__(self):
        self.__private_field=71

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field

baz = MyChildObject()
baz.get_private_field()


'''
虽然下面这种写法看起来好像可以，但会在继承时出问题
如果MyClass上面还有一个父类，这个值是它的，那么我子类 用 _MyClass__value这种方式访问就错了

'''
class MyClass(object):
    def __init__(self,value):
        self.__value=value

    def get_value(self):
        return str(self.__value)

class MyIntegerSubclass(MyClass):
    #重写init方法是不是就不算访问父类属性了
    def get_value(self):
        return int(self._MyClass__value)

foo=MyIntegerSubclass(5)
assert foo.get_value()=='5'


'''
恰当的做法是，宁可叫子类更多地去访问超类的protected属性，也别把属性设置为private
应该用文档说明每个字段的含义

当需要避免子类和超类的属性名冲突时，需要用private属性

'''
class ApiClass(object):
    def __init__(self):
        self._value=5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value='hello'   #这时候父类的 _value=5被覆盖了



class ApiClass2(object):   #这里时API 子类不受我们控制，所以写成 private
    def __init__(self):
        self.__value=5

    def get(self):
        return self.__value   #这样至少不会冲突

class Child2(ApiClass2):
    def __init__(self):
        super().__init__()
        self._value='hello'



'''
继承collections.abc以实现自定义的容器类型
这个很像pytorch里面 实现自己的dataset类  实现__getitem__  __len__方法


'''


#继承list并且添加计算元素频次的方法
class FrequencyList(list):
    def __init__(self,members):
        super().__init__(members)

    def frequency(self):
        counts={}
        for item in self:
            counts.setdefault(item,0)
            couts[item]+=1
        return counts


'''
如果要分别实现这些方法就太麻烦了，还容易忘记
内置的collection.abc定义了一系列抽象类，如果忘记实现一些必要方法，它会提醒
如果有一些非必要重写的方法，它会自动提供
它能够确保我们的子类具备适当的接口及行为

'''
