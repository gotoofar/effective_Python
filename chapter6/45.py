# -*- coding=utf-8 -*-


'''
45.用datatime模块来处理本地时间，而不是time模块
time模块在处理不同时区时容易出错


UTC是标准的时间表述方式，某一时刻与UNIX时间原点（1970年最开始）相差的秒数
UTC时间与当地时间的转换比较常用


'''

#time模块的localtime函数可以把UNIX时间戳（UTC时刻距离原点的秒数）转换为当地时间
from time import localtime,strftime

now=1574480710
local_tuple = localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = strftime(time_format,local_tuple)
print(time_str)

#还有反向处理
from time import mktime,strptime
time_tuple = strptime(time_str,time_format)
utc_now = mktime(time_tuple)
print(utc_now)

'''
但在有时区计算时，strptime可以正确解析计算机支持的时区，别的时区不行
比如下面这个 UTC与宿主计算机的当地时区之间进行转换

噢这个很无聊，只是时区转换中datetime的优势，而且我不知道这个UTC时间转给某个时区，但这个UTC是从哪个时区开始算的？
'''
parse_format = '%Y-%m-%d %H:%M:%S %Z'
depart_sfo = '2019-11-23 20:27:15 PTD'
time_tuple = strptime(depart_sfo,parse_format)
time_str = strftime(time_format,time_tuple)
print(time_str)







