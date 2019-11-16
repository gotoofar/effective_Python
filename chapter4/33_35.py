# -*- coding=utf-8 -*-

'''
元类是创建类的类

首先 定义类可以等价如下
'''

class Base:
    pass

class ChildWithMethod(Base):
    bar = True

    def hello(self):
        print('hello')


def hello(self):
    print('hello')

# 等价定义
ChildWithMethod = type('ChildWithMethod', (Base,), {'bar': True, 'hello': hello})

'''
想要控制类的创建
比如校验或者修改类的属性的时候

'''

class Meta(type):
    def __new__(meta,name,bases,class_dict):
        print((meta,name,bases,class_dict))    #创建类的时候 把信息都打出来
        return type.__new__(meta,name,bases,class_dict)

class MyClass(object,metaclass=Meta):
    stuff = 123

    def foo(self):
        pass


'''
为了确保类里面的参数都有效，可以把相关逻辑验证添加到 Meta.__new__ 方法中

元类里面编写的验证逻辑，针对的是基类的子类，而不是它本身
比如一个多边形作为基类，基类把一个验证类当作元类，子类有个三角形，

'''
class ValidatePolygon(type):
    def __new__(meta,name,bases,class_dict):
        #这句防止对基类进行验证
        if bases !=(object,):
            if class_dict['sides']<3:
                raise ValueError('Polygons need 3+ sides')

        return type.__new__(meta,name,bases,class_dict)

class Polygon(object,metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides-2)*180

class Triangle(Polygon):
    sides=3

#如果尝试继承Polygon时在里面把sides定为3以下  这个class代码都过不了












'''
34.用元类来注册子类

用json序列化举例，定义一个可序列化类，再用Point2D去继承他

'''
class Serializable(object):
    def __init__(self,*args):
        self.args = args

    def serialize(self):
        return json.dumps({'args':self.args})   #把参数都存进json

class Point2D(Serializable):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x=x
        self.y=y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x,self.y)

point = Point2D(5,3)
print('Object: ',point)
print('Serialized:',point.serialize())   #序列化

'''
反序列化可以把JSON字符串还原为Python对象

'''
class Deserializable(Serializable):
    @classmethod
    def deserialize(cls,json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class BetterPoint2D(Deserializable):
    pass

point = BetterPoint2D(5,3)
data=point.serialize()           #序列化
after=BetterPoint2D.deserialize(data)   #反序列化


'''
这种序列化的缺点是我们必须提前知道序列化的数据类型

理想方案时有很多类都可以把本类对象转换成JSON格式的序列化字符串，但只需要一个公用的反序列化函数
就可以将任意的JSON字符串还原成相应的Python对象
可以把序列化对象的类名写到JSON数据里面
'''

class BetterSerializable(object):
    def __init__(self,*args):
        self.args=args

    def serialize(self):
        return json.dumps({'class':self.__class__.__name__,'args':self.args})

    def __repr__(self):
        #...
        pass

#把类名与该类对象构造器之间的关系维护到一份字典里

registry = {}

def register_class(target_class):
    registry[target_class.__name__]=target_class

def deserialize(data):
    params = json.loads(data)
    name=params['class']
    target_class=registry[name]
    return target_class(*params['args'])

'''
为了确保deserialize 函数正常运作，必需用register_class把要反序列化的类都注册一遍
'''

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x=x
        self.y=y

register_class(EvenBetterPoint2D)   #注册


point = EvenBetterPoint2D(5,3)
data = point.serialize()
after = deserialize(data)    #不用知道是什么类了，也能反序列化


'''
如果写完了类忘记注册就不好了，这里可以通过元类提前准备

'''

class Meta(type):
    def __new__(meta, name, bases,class_dict):
        cls=type.__new__(meta,name,bases,class_dict)
        register_class(cls)  #注册
        return cls

class RegisteredSerializable(BetterSerializable,metaclass=Meta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self,x,y,z):
        super().__init__(x,y,z)
        self.x,self.y,self.z=x,y,z

v3 = Vector3D(10,-7,3)
data=v3.serialize()
print(deserialize(data))

'''
在构建模块化的Python程序时，类的注册是一种很有用的模式
每次从基类中继承子类时，基类的元类都可以自动运行注册代码
通过元类来实现类的注册可以确保所有子类都不会遗漏。

'''
