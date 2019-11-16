# -*- coding=utf-8 -*-

'''
以@classmethod形式的多态去通用地构建对象

书在这里举了MapReduce流程作为例子，原理如下：
对于大规模的数据处理任务，可以使用大量的机器同时做子任务，再汇总结果
这些机器分为Master（负责调度） Mapper（负责处理） Reducer（负责汇总）
假设原始任务的Input个数为M,output个数为N。Mapper的个数为P，Reducer的个数为R。
则有关系，M〉P〉N〉R。也就是说，一个Mapper要做M/P个input的处理任务，一个Reducer
要做N/R个output的汇总工作。

举例来说，统计一系列文档中的词频。文档数量规模很大，有1000万个文档，英文单词的总数
可能只有3000（常用的）。那么input M=10000000，output N=3000。
于是我们搞了10000个PC做Mapper，100个PC做Reducer。每个Mapper做1000个文档
的词频统计，统计之后把凡是和同一个word相关的统计中间结果传给同一个Reducer做
汇总。比如某个Reducer负责词表中前30个词的词频统计，遍历10000个PC，这10000个
Mapper PC把各自处理后和词表中前30个词汇相关的中间结果都传给这个Reducer做最终的处理分析。


链接：https://www.zhihu.com/question/23345991/answer/53996060
来源：知乎

下面实现一套普通MapReduce流程
'''
import os
from threading import Thread

class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):   #还可能有其他类似的子类用不同的方法读取数据
    def __init__(self,path):
        super().__init__()
        self.path=path

    def read(self):
        return open(self.path).read()

class Worker(object):
    def __init__(self,input_data):
        self.input_data=input_data
        self.result=None

    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

#下面这个Worder子类是一个换行符计数器
class LineCountWorker(Worker):
    def map(self):
        data=self.input_data.read()
        self.result=data.count('\n')

    def reduce(self,other):
        self.result+= other.result

#为目录中的每个文件创建一个PathInputData实例
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir,name))

#用generate_inputs方法返回的InputData实例创建 LineCountWorker实例
def create_workers(input_list):   #输入的是上面生成的
    workers=[]
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

#执行实例  分发到各个线程中去
def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for threads in threads: threads.start()
    for threads in threads: threads.join()

    first,rest = workers[0],workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

#把上面这些代码拼装到函数里
def mapreduce(data_dir):
    inputs=generate_inputs(data_dir)
    workers=create_workers(inputs)
    return execute(workers)
#运行
result=mapreduce(tmpdir)




'''
这些函数不够通用，如果有其他的InputData 或 Worker类就得重写下面这些函数
希望每个InputData子类都提供特殊的构造器，但Python只允许名为__init__的构造器方法
所以无法要求每个InputData子类都提供兼容的构造器
所以用 @classmethod 形式的多态，针对的是整个类而不是从该类构建出来的对象
'''

class GenericInputData(object):
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls,config):   #这个方法接受一份含有配置参数的字典，子类可以解读
        raise NotImplementedError


class PathInputData(GenericInputData):

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls,config):
        data_dir=config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir,name))

class GenericWorker(object):
    #...
    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

    @classmethod
    def create_workers(cls,input_class,config):
        workers=[]
        for input_data in input_class.genenerate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCountWorker(GenericWorker):
    # ...
    pass

def mapreduce(worker_class,input_class,config):
    workers=worker_class.create_workers(input_class,config)
    return execute(workers)

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir':tmpdir}
    result = mapreduce(LineCountWorker, PathInputData , config)

'''
通过类方法，用一种与构造器 __init__ 相仿的方式来构造类的对象
别的方法可能不是通过路径传入数据的，但在编写其他 GenericInputData 和 GenericWorker子类时就不用修改前面的拼接代码了
'''














