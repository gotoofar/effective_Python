# -*- coding=utf-8 -*-
'''
49.提供docstring为每个模块/类/函数编写文档
为模块撰写文档时，应该介绍本模块内容，并且把用户需要了解的重要类和重要函数列出来
为类撰写文档时，应该在class语句下面的docstring中介绍本类的行为/重要属性以及本类的子类应该实现的行为
为函数及方法撰写文档时，在def下面的docstring语句中介绍函数的每个参数，函数的返回值，在执行过程中可能抛出的异常以及其他行为

先用一句话阐述用途 再用一段话详述操作方式
'''


def palindrome(word):
    """Return True if the given word is a palindrome."""
    return word == word[::-1]

print(palindrome.__doc__)


#模块的文档
"""one sentence explaination

more explaination

Available functions:
- palindrome: Determine if a word is a palindrome
- check_anagram: Determine if two words are anagrams
...
"""


#类的文档  比较重要的public属性和方法要在里面介绍
class Player(object):
    """Represents a player of the game

    Subclasses may override the 'trick' method to provide
    custom ...

    Public attributes:
    - power:Unused power-ups
    - coins:Coins found during the level
    ...

    """

#函数的文档   一句话写功能 一段话写具体行为和函数参数   返回值也要写，如果会抛出异常且异常也是函数接口  要加上

def find_anagrams(word,dictionary):
    """Find all anagrams for a word

    This function only runs as fast as the test for
    membership in the 'dictionary' container. It will
    be slow...

    Args:
        word:String of the target word
        dictionary:Container with all strings that
            are know to be actual words.

    Returns:
        List of anagrams that were found.Empty if
        none were found.

    """

'''
50.用包来安排模块，并提供稳固的API
包是一种含有其他模块的模块
只要把__init__.py文件放入含有其他源文件的目录里，就可以把这个目录定为包
把外界可见的名称列在名为__all__的特殊属性里，可以为包提供一套明确的API

如果想隐藏某个包的内部实现，可以在包的__init__.py文件中只把外界可见的那些名称引入进来

在__init__里面还可以用__all__ 属性把目录下的模块都整合一下

'''

#utils.py
__all__ =['simulate_collision']

def _dot_product(a,b):
    pass

def simulate_collision(a,b):
    pass




'''
51.为自编的模块定义根异常，以便将调用者与API相隔离


'''


'''
52.用适当的方式打破循环依赖关系
两个模块互相import，需要打破这个依赖
最佳方案：把导致两个模块互相依赖的那部分代码重构为单独的模块，并把它放在依赖树的底部
最简方案：执行动态的引入操作，可以缩减重构所花的精力，也可以尽量降低代码的复杂度


'''




'''
53.用虚拟环境隔离项目，并重建其依赖关系
当我们的两个包都依赖同一个包时，那个包更新后，依赖它的两个包可能会出现一个依赖新版本 一个依赖旧版本而无法使用的情况
通过pyvenv我们可以在同一个系统上面同时安装某软件包的多个版本，很像anaconda

pip freeze命令可以把某套环境所依赖的软件包汇总到一份文件里。把这个requirements.txt文件提供给pip install -r命令
可以重建一套与原环境相仿的新环境

'''














