#-------------------------------------
#-------------------------------------
#--- author:陈南
#--- email:kevin-chen@foxmail.com
#--- wechat:kevin_nan
#--- date:2020.8.1
#--- Copyright (c) 2020-present, KevinChen2046 Technology.
#--- All rights reserved.
#-------------------------------------
#-------------------------------------
from enum import Enum
class ConsoleColor(Enum):
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    PINK = "35"
    CYAN = "36"
    WHITE = "37"

class Logger:
    @staticmethod
    def line(*args):
        content = ""
        for arg in args:
            content+=arg+" "
        content=content[0:len(content)-1]
        total = 20
        _len = total - len(content) / 2
        _line = ""
        while _len>0:
            _line = _line+"-"
            _len -=1
        result = "\033[0;33;40m\t"+_line+content+_line+"\033[0m"
        print(result)

    @staticmethod
    def log(*args):
        Logger.__out(ConsoleColor.WHITE,"[LOG]", *args)

    @staticmethod
    def info(*args):
        Logger.__out(ConsoleColor.GREEN,"[INFO]", *args)

    @staticmethod
    def warn(*args):
        Logger.__out(ConsoleColor.YELLOW,"[WARN]", *args)

    @staticmethod
    def debug(*args):
        Logger.__out(ConsoleColor.CYAN,"[DEBUG]", *args)

    @staticmethod
    def error(*args):
        Logger.__out(ConsoleColor.RED,"[ERROR]", *args)

    @staticmethod
    def __out(color,*args):
        content = ""
        for arg in args:
            content+=arg+" "
        content=content[0:len(content)-1]
        content="\033[0;"+color.value+";40m"+content+"\033[0m"
        print(content)
