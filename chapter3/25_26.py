# -*- coding=utf-8 -*-


'''
25.用super初始化父类
先看传统方式——在子类里用子类实例直接调用父类的__init__方法
'''

class MyBaseClass(object):
    def __init__(self,value):
        self.value=value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self,5)

'''
这种方式在遇到多重继承时有两个问题
一是有两个父类时初始化顺序不固定,多个父类的 __init__实际顺序不定
二是钻石继承 产生未知错误
super函数可以解决，方法解析顺序（MRO method solution order）以标准的流程安排超类之间的初始化顺序  可以通过mro方法查询
保证钻石顶部公共基类的__init__方法只会执行一次

'''

#Python 3 风格
class Explicit(MyBaseClass):
    def __init__(self,value):
        super(__class__,self).__init__(value)


#网上的风格有点不一样

class Foo():
    def __init__(self,a,b):
        self.x=a
        self.b=b

class Bar(Foo):
    def __init__(self,a,c):
        super().__init__(a,34)
        self.d=c


#之前写的应该是Python 2 风格的

# class Net(nn.Module):
#     def __init__(self):
#         super(Net,self).__init__()


'''
26.只在使用Mix-in组件制作工具类时进行多重继承
它只定义了其他类可能需要提供（？）的一套附加方法，而不定义自己的实例属性
也不要求使用者调用自己的__init__构造器

例如，把内存中的Python对象转换为字典形式，以便将其序列化，把这个功能写成通用代码
其他类可以通过继承这个类来获得功能

'''
class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)    #这个__dict__ 如果是对类用就把所有属性方法都变成字典给出来，如果是实例则就把属性给出来

    def _traverse_dict(self,instance_dict):
        output={}
        for key,value in instance_dict.items():  # 这些items里面有的是属性 有的是方法  一一序列化
            output[key]=self._traverse(key,value)
        return output
    #不管是什么类型，都把它转为字典
    def _traverse(self,key,value):
        if isinstance(value,ToDictMixin):  #有利于二叉树之类的嵌套使用
            print(1)
            return value.to_dict()
        elif isinstance(value,dict):
            print(2)
            return self._traverse_dict(value)
        elif isinstance(value,list):
            print(3)
            return [self._traverse(key,i) for i in value]
        elif hasattr(value,'__dict__'):
            print(4)
            return self._traverse_dict(value.__dict__)
        else:
            print(5)
            return value


#下面演示如何用mix-in把二叉树转为字典
class BinaryTree(ToDictMixin):
    def __init__(self,value,left=None,right=None):
        self.value=value
        self.left=left
        self.right=right
#这个例子里面只会用上if的第一个和第五个  因为除了数值 就是实例本身
tree=BinaryTree(10,left=BinaryTree(7,right=BinaryTree(9)),right=BinaryTree(13,left=BinaryTree(11)))
print(tree.to_dict())


#如果是带有指向父节点的属性，以上这种方法可能会陷入死循环,但重写_traverse方法即可

class BinaryTreeWithParent(BinaryTree):
    def __init__(self,value,left=None,right=None,parent=None):
        super().__init__(value,left=left,right=right)
        self.parent=parent
    def _traverse(self,key,value):
        if (isinstance(value,BinaryTreeWithParent) and key=='parent'):
            return value.value  #直接拿到值，而不去追踪
        else:
            return super()._traverse(key,value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7,parent=root)
root.left.right = BinaryTreeWithParent(9,parent=root.left)
print(root.to_dict())



#再写一个类似的处理类
class JsonMixin(object):
    @classmethod
    def from_json(cls,data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())  #自己没有这个方法，但子类的另一个父类有




'''
凡是想继承上面这个JsonMixin类的要有to_dict方法
继承了mix-in的那个类，才提供这个方法

将各功能实现为可插拔的mix-in组件，然后令相关的类继承自己需要的那些组件，就可以定制该类所应具备的行为
把简单的行为封装道mix-in组件里，就可以用多个mix-in组合出复杂的行为

'''
class DatacenterRack(ToDictMixin,JsonMixin):
    def __init__(self,switch=None,machines=None):
        self.switch=Switch(**switch)
        self.machines=[Machines(**kwargs) for kwargs in machines]


class Switch(ToDictMixin,JsonMixin):
    #...
class Machines(ToDictMixin,JsonMixin):
    # ...




