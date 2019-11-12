# -*- coding=utf-8 -*-

'''
10.用enumerate代替range
想获取迭代并且拿到索引时enumerate更好用，把迭代器包装成生成器
'''
fpx=['GimGoon','Tian','Doinb','lwx','Crisp']
for i,player in enumerate(fpx,1):  #第二个参数表示从几开始计数
    print('%d: %s'%(i,player))


'''
11.zip遍历多个迭代器
如果迭代器不等长，zip会自动提前终止
itertools内置模块的zip_longest函数可以不在乎长度
python3里zip相当于生成器  python2里面是先把元组生成好，一次性返回一个列表，容易崩
'''
maxlength=0
longestname=None
length=[len(n) for n in fpx]
for name,count in zip(fpx,length):
    if count>maxlength:
        longestname=name
        maxlength=count

print(longestname)


'''
for-else  和  while-else 应该慎用
在循环里没有碰到break时会执行
比如 判断两个数是否互质，用和不用else写如下两例
'''
a=4
b=9
for i in range(2,min(a,b)+1):
    print('Testing',i)
    if a%i==0 and b%i==0:
        print('Coprime')
        break
else:
    print('Coprime')

def coprime(a,b):
    for i in range(2,min(a,b)+1):
        if a%i==0 and b%i==0:
            return False
        return True

'''
try/except/else/finally 合理利用
'''
#try-finally 组合，适用于无论如何都要把文件句柄关闭的情况
handle=open('**.txt')
try:
    data=handle.read()
finally:
    handle.close()


#try-else-except结构可以描述哪些异常自己处理，哪些异常返回上一级
#有else还可以少放一些代码在try中
def load_json_key(data,key):
    try:
        #这里产生的异常自己处理
        result_dict=json.loads(data)
    except ValueError as e:
        raise KeyError from e
    else:
        #查询异常时，这个异常会向上传播
        return result_dict[key]


'''
混合使用
运行try块后，若想使某些操作能在finally块的清理代码前执行，就放到else中
'''
UNDEFINED=object()
def divide_json(path):
    handle=open(path,'r+')
    try:
        data=handle.read()
        op=json.loads(data)
        value=(op['numerator']/op['denominator'])
    except ZeroDivisionError as e:
        return UNDEFINED
    else:
        op['result']=value
        result=json.dumps(op)
        handle.write(result)
        return value
    finally:
        handle.close()




