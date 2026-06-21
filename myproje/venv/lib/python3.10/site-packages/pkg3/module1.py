'''
@file : module1.py
@Time : 14/4/2022 下午8:22
@Author： Zheng Xingyu
@Version：1.0
@Contact：zhengxingyu_1990@126.com
'''
class Student:
    def __init__(self,name,score):
        self.name=name
        self.score=score
    @classmethod
    def info(cls):
        print(cls.name,cls.score)