# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/5 17:01
#

# 因子类
class Factor():

    # 因子的基本参数
    def __init__(self, code, name, frequency,describe, origin, direct):
        self.code = code # 因子代码：主键，不可空
        self.name = name # 因子名：不可空
        self.frequency = frequency # 频率：不可空
        self.components = dict() # 计算因子需要的数据: 不可空
        self.type = '' # 因子的类型，如：价值类因子
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




# 价值类因子
class ValueFactor(Factor):
    # 价值类因子的基本参数
    def __init__(self, code, name, frequency, describe, origin,direct):
        Factor.__init__(self, code, name, frequency,describe, origin, direct)
        self.type = 'value'


class EP(ValueFactor):

    def __init__(self):
        ValueFactor.__init__(self,
                             code = '0001',
                             name = 'EP',
                             frequency = 'month',
                             describe = 'this is description for EP',
                             origin = 'basic',
                             direct = '+'
                             )
        self.components = {'TTM' : 'LC_DerivativeData.NetProfitTTM, 季频',
                           'TotalMV' : 'QT_Performance.TotalMV, 日频，单位百万'
                           }

    def find_components(self, date):
        self.components['TTM'] = 'sql to acquire LC_DerivativeData.NetProfitTTM(考虑时间)'
        self.components['TotalMV'] = 'sql to acquire QT_Performance.TotalMV(考虑时间)'
        return self.components

    def calculate(self):
        ep = self.components['TTM'] / self.components['TotalMV']
        return ep

    def store(self):
        pass





if __name__ == '__main__':
    ep_month1 = EP()
    print(ep_month1)
    print(ep_month1.find_components(date = 20140102))
    print(ep_month1.calculate())