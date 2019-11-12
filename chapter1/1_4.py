# -*- coding=utf-8 -*-

'''
第一章 用Pythonic方式来思考
2.
PEP8风格指南
https://www.python.org/dev/peps/pep-0008/

空白：
* 用4个空格，不要用tab
* 多行表达式，换行之后应该再缩进4个空格
* 函数与类之间用两个空行隔开，方法与方法之间用一个空行隔开
* 变量赋值 a = b 的时候，符号两边各放一个空格

命名：
* 函数/变量/属性用小写字母和下划线
* 受保护的属性前面一个下划线，私有属性两个下划线
* 类与异常的每个单词首字母都要大写
* 模块级别的常量均大写
* 类中的实例方法第一个参数为self，类方法第一个参数为cls

表达式和语句：
* 否定词要尽量往里放（内联），if a is not b 要比  if not a is b 更好
* 判断为空时不要用 if len(somelist)==0 应该用 if not somelist
* import语句部分应该分为三个,标准库模块、第三方模块以及自用模块

文件中读写二进制数据时，应该以模式'wb' 'rb'来开启文件

'''


#3.接收 str和bytes，总是返回str的方法
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value
#返回bytes的把编码解码换一下就可以
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value



'''
4.
复杂的表达式可以用辅助函数取代
这里用URL解码查询字符串作为示例
'''
from urllib.parse import parse_qs
url_str='red=5&blue=0&green='
my_value=parse_qs(url_str,keep_blank_values=True)
print(repr(my_value))
print('Red: ',my_value.get('red'))
print('Green: ',my_value.get('green'))
print('Opacity: ',my_value.get('opacity'))

#在这里输出的值会因为字符串里不包含而输出None或空列表，为了让输出更规范，在get里面加参数，并且获得值而不是列表

green=my_value.get('green',[''])[0] or 0

#get如果待查询的键没有则返回第二个值
#但是上面这种写法很复杂，最好写成下面的辅助函数

def get_first_int(values,key,default=0):
    found=values.get(key,[''])
    if found[0]:
        found=int(found[0])
    else:
        found=default
    return found

green=get_first_int(my_value,'green')
print(green)


