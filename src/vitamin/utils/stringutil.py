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

class StringUtil:
    
    #-- 首字母大写
    @staticmethod
    def firstToUpper(content):
        return content.capitalize()

    #-- 首字母小写
    @staticmethod
    def firstToLower(content):
        return content[0].lower() + content[1:]

