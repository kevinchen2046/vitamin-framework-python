#-------------------------------------
#-------------------------------------
#--- author:陈南
#--- email:kevin-chen@foxmail.com
#--- wechat:kevin_nan
#--- date:2020.7.24
#--- Copyright (c) 2020-present, KevinChen2046 Technology.
#--- All rights reserved.
#-------------------------------------
#-------------------------------------
from functools import cmp_to_key

class EventEmiter :
    className = "EventEmiter"
    _map= {}
    def __init__(self):
        self._map = {}
    #-- 监听事件
    #-- type 事件类型
    #-- listener 事件回调
    #-- priority 事件优先级
    def on (self, type, listener, priority=0):
        if (priority == None):priority = 0
        if (self._map.get(type)== None):self._map.setdefault(type,[])
        _list = self._map[type]
        _index=self.__getIndex(_list,listener)
        if(_index==-1):
            _list.insert(_list.__len__(),{"method" : listener,"priority" : priority})
        return self
    #-- 取消事件
    def off (self, type, listener):
        _list = self._map[type]
        if (_list and _list.length):
            off = 0
            for i in _list:
                _object = _list[i + off]
                if (_object["method"] == listener):
                    _list.remove(_object)
                    off = off - 1
        return self
    #-- 发送事件
    def emit (self, type, *arg):
        def _sort(a,b):
            return 1 if (a["priority"] > b["priority"]) else -1
        _list = self._map.get(type)
        if(_list==None):return self
        _list.sort(key=cmp_to_key(_sort))
        for _object in _list:
            _object["method"](*arg)
        return self

    def __getIndex(self,_list,listener):
        for i in range(len(_list)):
            if(_list[i]["method"]==listener):
                return i
        return -1
