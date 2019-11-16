# -*- coding=utf-8 -*-


'''
29.用纯属性取代get和set操作
之前学习很多给实例的属性是private，定义两个get和set函数，自增的时候比较麻烦
而且不符合python的风格，python一般直接用属性，如果需要动态定义对属性的访问
就用 @property 和  @attri.setter   （这个attri是属性名字）

@property  是专门把方法变成属性的
'''

class Resistor(object):
    def __init__(self,ohms):
        self.ohms=ohms
        self.voltage=0
        self.current=0


class VoltageResistance(Resistor):
    def __init__(self,ohms):
        super().__init__(ohms)
        self._voltage=0

    #获取属性
    @property
    def voltage(self):
        return self._voltage

    #进行设置
    @voltage.setter
    def voltage(self,voltage):
        self._voltage=voltage
        # 特定行为：设置电压之后，current会和电压 电阻匹配  这里面还可以做数值验证
        self.current=self._voltage/self.ohms


#这个 @property甚至可以防止父类属性遭到修改，通过判断这个改变的值是不是这个类的

class FixedResistance(Resistor):

    @property
    def ohms(self):
        return self,_ohms

    @ohms.setter
    def ohms(self,ohms):
        if hasattr(self,'_ohms'):  #这句话我很疑惑 是这样判断是否父类属性的吗？
            raise AttributeError("Can't set attribute")
        self._ohms=ohms


'''
30.考虑用@property 代替属性重构

这个修饰器还可以把简单的数值迁移为实时计算的属性

比如下面这个带有配额的漏桶算法

'''
from datetime import timedelta
import datetime

class Bucket(object):
    def __init__(self,period):
        self.period_delta = timedelta(second=period)  #这个函数会把给进去的时间自动换成标准形式  xx小时：xx分：xx秒
        self.reset_time=datetime.datetime.now()   #现在的时间
        self.quota=0

    #print时调用的是str  直接输出对象时调用的这个
    def __repr__(self):
        return 'Bucket(quota=%d)'%self.quota

#加水
def fill(bucket,amount):
    now = datetime.datetime.now()
    if now - bucket.reset_time>bucket.period_delta:  #如果两次加水时间超过周期，则桶里的水不能要了 时间也重设
        bucket.quota=0
        bucket.reset_time=now
    bucket.quota+=amount


#消耗 （漏水）
def deduct(bucket,amount):
    now = datetime.datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False          #如果桶里的水过期了 就不能取
    if bucket.quota-amount<0:    # 不够也不能拿
        return False
    bucket.quota-=amount
    return True

bucket=Bucket(60)  #设定周期为60秒
fill(bucket,100)   #加水100

if deduct(bucket,99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
'''
如果桶里的余额不够消耗，一直返回False
我们也无法知道是消耗完了还是刚开始根本就没有
可以设置两个属性，表示本周期的初始配额和本周期内消耗的配额

'''
class Bucket(object):
    def __init__(self,period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)'% (self.max_quota,self.quota_consumed))

    #根据这两个新属性，在@property方法里实时算出当前剩余的配额

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter   #为啥没有quota这个属性 都可以写这个方法?  难道fill会给他加？ 实验证明 是的
    def quota(self,amount):
        delta = self.max_quota-amount

        #这几个条件判断我有些不懂
        if amount==0:  #得到reset
            self.quota_consumed=0
            self.max_quota=0
        elif delta<0:   #得到新的fill
            assert self.quota_consumed==0
            self.max_quota=amount
        else:
            assert self.max_quota>=self.quota_consumed
            self.quota_consumed+=delta



'''
31.用描述符来改写需要复用的@property方法

先写一个反例，记录考试的成绩

'''
class Exam(object):
    def __init__(self):
        self._writing_grade=0
        self._math_grade=0

    @staticmethod
    def _check_grade(value):
        if not(0<=value<=100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self,value):
        self._check_grade(value)
        self._writing_grade=value

    #如果加一门数学课 又得写一遍
    @property
    def math_grade(self):
        return self._math_grade

    @writing_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


#如果设置一个Grade类，用这个类的实例当作Exam的类属性呢？
class Grade(object):
    def __init__(self):
        self._value=0

    def __get__(self,instance,instance_type):
        return self._value

    def __set__(self, instance, value):
        if not(0<=value<=100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value

    class Exam1(object):
        math_grade=Grade()
        writing_grade=Grade()
        #这样是不行的，不同的Exam实例用的是同一套  Grade()  相当于两场考试的 数学成绩是一样的
        #Grade实例只会在程序生命周期中构建一次


#那如果把每个Exam实例所对应的值记录到Grade中，用字典保存每个实例的状态呢？
class Grade(object):
    def __init__(self):
        self._values={}

    def __get__(self,instance,instance_type):
        if instance is None:return self   #没有还get
        return self._values.get(instance,0)

    def __set__(self,instance,value):
        if not(0<=value<=100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance]=value
'''
传给 __set__ 方法的每个Exam实例来说，_values字典都会保存指向该实例的一份引用
导致收集器无法将其回收  内存泄漏

如果使用WeakKeyDictionary 特殊字典，如果发现运行期这个字典所持有的引用是最后一份，则自动将该实例从字典的键移除


'''
class Grade(object):
    def __init__(self):
        self._values=WeakKeyDictionary()

    #...
    #就不会出现内存泄漏问题啦




