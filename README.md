# vitamin-framework-python
python 版本的 vitamin 框架

## 例子
```python
#!/usr/bin/python

from vitamin.core.logger import Logger
from vitamin.core.event import EventEmiter
from functools import cmp_to_key
from vitamin.vitamin import *

# Model的装饰器 无任何依赖项
@ModelClass()
class ModelUser(ModelBase):
    name="ModelUser!!!!"
    def initialize(self,*args):
        Logger.log("ModelUser initialize...")

# Model的装饰器 该Model依赖ModelUser模块
@ModelClass("ModelUser")
class ModelLogin(ModelBase):
    name="ModelLogin!"
    
    # 注入ModelUser
    @property
    def user(self):return Inject(ModelUser)

    def initialize(self,*args):
        Logger.log("ModelLogin initialize...")
        Logger.debug(self.user.name)

# Command的装饰器 需要填写该Cmd的路由 也可以通过Cmd的className触发该Command
@CmdClass("game.login")
class CmdLogin(CommandBase):
    def exec(self,*args):
        for arg in args:
            Logger.warn("CmdLogin:"+str(arg))

# View装饰器     
@ViewClass
class ViewLogin(ViewBase):
    def enter(self,*args):
        super().exec("game.login",*args)

# 单例装饰器 
@Instance
class Util():
    def plus(self,a,b):
        return a+b


vitamin=Vitamin()

# 初始化Vitamin框架
vitamin.initialize()

## 测试单例
util1=Util()
util2=Util()
Logger.debug("util1==util2",str(util1==util2))

## 测试Model的单例性质
model1=vitamin.getModel(ModelLogin).user
model2=vitamin.getModel(ModelUser)
Logger.debug("model1==model2")

# 打开界面 执行了一个Command
vitamin.getView(ViewLogin).enter("Some Thing is Happended")

vitamin.getView(ViewLogin).on("TEST",lambda v,v1:Logger.info("ViewLogin:",v,v1))
vitamin.getModel(ModelLogin).on("TEST",lambda v,v1:Logger.info("ModelLogin:",v,v1))

# 从View处触发的事件 只有View能接收到
vitamin.getView(ViewLogin).emit("TEST","This is View:","Kevin")
# 从Model处触发的事件 Model和View都能接收到
vitamin.getModel(ModelLogin).emit("TEST","This is Model:","Chen")
```