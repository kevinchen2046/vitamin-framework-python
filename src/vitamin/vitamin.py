# -------------------------------------
# -------------------------------------
# --- author:陈南
# --- email:kevin-chen@foxmail.com
# --- wechat:kevin_nan
# --- date:2020.7.24
# --- Copyright (c) 2020-present, KevinChen2046 Technology.
# --- All rights reserved.
# -------------------------------------
# -------------------------------------
#
# -- Vitamin使用注意  --
# -- 1.所有静态方法访问操作符为 .
# -- 2.所有实例方法访问操作符为 : ,这样访问可以传递self
# -- 3.所有实例属性访问操作符仍为 .
# -- 4.定义Class时,className为必须项

from .core.logger import Logger
from .core.event import EventEmiter

#-- 视图基类


class ViewBase(EventEmiter):
    def enter(self, *args): pass
    def exit(self): pass

    def exec(self, route, *args):
        Vitamin().exec(route, *args)

    def on(self, type, listener, priority=0):
        Vitamin().onViewEvent(type, listener, priority)

    def off(self, type, listener):
        Vitamin().offViewEvent(type, listener)

    def emit(self, type, *args):
        Vitamin().emitViewEvent(type, *args)

#-- 数据模型基类


class ModelBase(EventEmiter):
    def initialize(self, *args): pass
    def reset(self): pass

    def exec(self, route, *args):
        Vitamin().exec(route, *args)

    def on(self, type, listener, priority=0):
        Vitamin().onModelEvent(type, listener, priority)

    def off(self, type, listener):
        Vitamin().offModelEvent(type, listener)

    def emit(self, type, *args):
        Vitamin().emitModelEvent(type, *args)
#-- 命令基类


class CommandBase(EventEmiter):
    def exec(self, *args):
        pass


def Instance(clazz):
    def wrapper(*args, **kargs):
        if(getattr(clazz, "__instance__", None) == None):
            setattr(clazz, "__instance__", clazz(*args, **kargs))
        return getattr(clazz, "__instance__", None)
    return wrapper


def getInstance(clazz):
    return getattr(clazz, "__instance__", None)

#-- 框架初始化

def Inject(clazz):
    return Vitamin().getModel(clazz)

@Instance
class Vitamin():
    __model__map = {}
    __cmd__map = {}
    __view__map = {}
    __model_emiter = EventEmiter()
    __view_emiter = EventEmiter()

    def __init__(self):
        print("Vitamin created")

    @property
    def modelMap(self):
        return self.__model__map

    @property
    def cmdMap(self):
        return self.__cmd__map

    @property
    def viewlMap(self):
        return self.__view__map

    def initialize(self):
        modelNames = []
        for name in self.__model__map:
            modelNames.append(name)

        while(True):
            for key in self.__model__map:
                dependents=self.__model__map[key]["dependents"]
                if(dependents.__len__() > 0):
                    ready = True
                    for dependent in dependents:
                        if(dependent in modelNames):
                            ready = False
                            break
                    if(ready and key in modelNames):
                        self.__model__map[key]["instance"].initialize()
                        modelNames.remove(key)
                else:
                    if(key in modelNames):
                        self.__model__map[key]["instance"].initialize()
                        modelNames.remove(key)
            if(modelNames.__len__() == 0):
                break

        # for ckey in self.__cmd__map:
        #     pass
        # Logger.debug('__model__map:'+str(self.__model__map))
        # Logger.debug('__cmd__map:'+str(self.__cmd__map))
        Logger.info("Vitamin Start...")

    def getModel(self, clazz):
        return self.__model__map[clazz.__name__]["instance"]

    def getView(self, clazz):
        return clazz()

    def exec(self, route, *args):
        for key in self.__cmd__map:
            if(self.__cmd__map[key]["route"] == route):
                self.__cmd__map[key]["instance"].exec(*args)
                return
        for key in self.__cmd__map:
            if(key == route):
                self.__cmd__map[key]["instance"].exec(*args)
                return

    def onViewEvent(self, type, listener, priority):
        self.__view_emiter.on(type, listener, priority)
        self.__model_emiter.on(type, listener, priority)

    def offViewEvent(self, type, listener):
        self.__view_emiter.off(type, listener)
        self.__model_emiter.off(type, listener)

    def emitViewEvent(self, type, *args):
        self.__view_emiter.emit(type, *args)

    def onModelEvent(self, type, listener, priority):
        self.__model_emiter.on(type, listener, priority)

    def offModelEvent(self, type, listener):
        self.__model_emiter.off(type, listener)

    def emitModelEvent(self, type, *args):
        self.__model_emiter.emit(type, *args)
# -------------------------------------------------------------------
#--                         装饰器
# -------------------------------------------------------------------

# -- 装饰器在传参不不参的情况下 外方法和内方法的参数是颠倒的  不知道为什么要这么设计


def ModelClass(*dependents):
    # Logger.debug(str(type(dependents[0])),str(type(dependents[0])==type))
    def wrapper(clazz):
        if(clazz.__name__ not in Vitamin().modelMap):
            Vitamin().modelMap[clazz.__name__] = {
                "instance": clazz(), "dependents": dependents}
        return clazz
    return wrapper


def CmdClass(route):
    def wrapper(clazz):
        if(clazz.__name__ not in Vitamin().cmdMap):
            Vitamin().cmdMap[clazz.__name__] = {
                "route": route, "instance": clazz()}
        return clazz
    return wrapper

def ViewClass(clazz):
    if(clazz.__name__ not in Vitamin().viewlMap):
        Vitamin().viewlMap[clazz.__name__] = clazz()
    def wrapper(*args, **kwargs):
        return Vitamin().viewlMap[clazz.__name__]
    return wrapper
