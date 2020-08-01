#!/usr/bin/python
import vitamin.core.logger
from vitamin.core.logger import Logger

import vitamin.core.event
from vitamin.core.event import EventEmiter

from functools import cmp_to_key

Logger.info("Hello, World!")

__map={}

__map["a"]=[]

__list=__map["a"]

_obj={"_a":1,"_b":"hello"}

__list.insert(__list.__len__(),_obj)

Logger.info(str(__map.get('a').__len__()),str(__map))

_emitter=EventEmiter()

_array=["b","c","e","y","i","6"]
def __sort(a,b):
    return 1 if "y"==a else -1

_array.sort(key=cmp_to_key(__sort))
Logger.debug(str(_array))
_emitter.on("TEST",lambda v,v1:Logger.info(v,v1)).emit("TEST","This is:","kevin chen")

def decorate(func):
    def wrapper():
        print("定义一个装饰器")
        #func(*args,**kwargs)
    return wrapper

class AA:
    @decorate
    def a():
        return 1

aa=AA()
Logger.log(str(aa.a()))

