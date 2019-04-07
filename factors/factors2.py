# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/5 17:01
#

# 因子类
class Factor():

    # 因子的基本参数
    def __init__(self, code, name, describe, origin, direct):
        self.code = code # 因子代码：主键，不可空
        self.name = name # 因子名：不可空
        self.components = dict() # 计算因子需要的数据: 不可空
        self.describe = describe # 因子描述
        self.origin = origin # 因子来源
        self.direct = direct # 因子的影响方向


    # 查找计算因子需要的数据
    def find_components(self, date):
        self.components[''] = ''
        return self.components

    # 因子的计算方法
    def calculate(self):
        result = ''
        return result

    # 因子的存储方法
    def store(self):
        pass



# 日频因子
class DayFrequency(Factor):
    def __init__(self, code, name,  describe, origin,direct):
        Factor.__init__(self, code, name, describe, origin, direct)
        self.frequency = 'day'



# 价值类因子
class ValueFactor(Factor):
    def __init__(self, code, name, describe, origin,direct):
        Factor.__init__(self, code, name, describe, origin, direct)
        self.type = 'value'




class EP(ValueFactor, DayFrequency):

    def __init__(self,
                 code = '0001',
                 name = 'EP',
                 describe = 'this is description for EP',
                 origin = 'basic',
                 direct = '+'
                 ):
        ValueFactor.__init__(self, code, name,  describe, origin,direct)
        DayFrequency.__init__(self, code, name,  describe, origin,direct)
        self.components = {'TTM' : 'LC_DerivativeData.NetProfitTTM, 季频',
                           'TotalMV' : 'QT_Performance.TotalMV, 日频，单位百万'
                           }


    def find_components(self, date):
        # self.components['TTM'] = 'sql to acquire LC_DerivativeData.NetProfitTTM(考虑时间)'
        # self.components['TotalMV'] = 'sql to acquire QT_Performance.TotalMV(考虑时间)'
        self.components['TTM'] = 1
        self.components['TotalMV'] = 2
        return self.components

    def calculate(self):
        ep = self.components['TTM'] / self.components['TotalMV']
        return ep

    def store(self):
        pass





if __name__ == '__main__':
    # import datetime
    # anyday=datetime.datetime(2017,1,28).strftime("%w")
    # print(anyday)

    ep = EP()
    print(ep)
    print(ep.code,ep.name,ep.frequency, ep.type, ep.direct, ep.components, ep.describe)
    print(ep.find_components(date = 20140102))
    print(ep.calculate())