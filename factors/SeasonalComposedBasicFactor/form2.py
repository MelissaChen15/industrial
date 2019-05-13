# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/29 10:45


from factors.Frequency import SeasonalFrequency
from factors.Category import ComposedBasicFactorForm1
from factors.sql import pl_sql_oracle

import numpy as np
import pandas as pd

"""
季频组合基本面因子， Form2, (X_change/AT)_pct形式


代码表：
    CB0363 - CB725

"""




class SeasonalComposedBasicFactorF2(SeasonalFrequency, ComposedBasicFactorForm1):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频组合基本面因子， Form2, (X_change/AT)_pct形式'

    # 形式2, (X_change/AT)_pct
    def init_factors(self):
        factor_code = 363
        factor_entities = {}

        numerator = pd.read_excel(r'./SeasonalComposedBasicFactor/组合基本面因子.xlsx', sheet_name='分子')
        numerator = numerator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]

        denominator = pd.read_excel(r'./SeasonalComposedBasicFactor/组合基本面因子.xlsx', sheet_name='分母')
        denominator = denominator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]

        # numerator = pd.read_excel(r'./组合基本面因子.xlsx', sheet_name='分子')
        # numerator = numerator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]
        #
        # denominator = pd.read_excel(r'./组合基本面因子.xlsx', sheet_name='分母')
        # denominator = denominator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]


        for n in numerator.itertuples(index=True, name='Pandas'):  # 分子
            for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
                factor_name = str(getattr(n, '英文简写')) + 'chgto' + str(getattr(d, '英文简写') + 'pct')
                factor_des = str('('+ getattr(n, '描述')) + '的变化值/' + str(getattr(d, '描述') +')较上期变化的百分数')
                factor_entity = SeasonalComposedBasicFactorF2(factor_code='CB%04d' % factor_code,
                                                                  name=factor_name,
                                                                 describe=factor_des)
                factor_entities[factor_name] = factor_entity
                factor_code += 1

        return factor_entities

    def calculate_change(self,component):
        """
        计算字段相较于上期的改变量
        :param components:  pd.DataFrame, 原始数据
        :return: pd.DataFrame, 已经转换好的数据
        """
        import datetime
        desired_date = datetime.datetime.strptime('2004-12-01', '%Y-%m-%d')

        change =  component.drop(columns=['SECUCODE', 'STARTDAY']).diff(axis=0)
        change[['SECUCODE', 'STARTDAY']] = component[['SECUCODE', 'STARTDAY']]
        change = change.sort_values(by='STARTDAY')
        for row in change.itertuples(index=True, name='Pandas'):  # 将2005年1月1日前的数据drop掉
            if getattr(row, 'STARTDAY') < desired_date:
                change = change.drop(index=change[change.STARTDAY < desired_date].index[0])
            else:
                break
        return change

    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # 因为资产负债表数据存在追溯调整的情况,所以同一个报告期会有很多份数据
        # 此处去重
        for key in components.keys():
            components[key] = components[key].drop_duplicates(['ENDDATE', 'SECUCODE'], keep='first')

        # TODO: 读取时需要按时间排序
        # LC_BalanceSheetAll
        # LC_IncomeStatementAll
        # LC_MainDataNew
        # LC_CashFlowStatementAll
        # LC_DerivativeData
        # LC_BalanceSheet
        # LC_Staff

        try:
            # t1 LC_BalanceSheetAll
            components['LC_BalanceSheetAll']  = components['LC_BalanceSheetAll'].sort_values(by='ENDDATE')
            components['LC_BalanceSheetAll_monthly'] = self.seasonal_to_monthly(components['LC_BalanceSheetAll'],['OTHERCURRENTASSETS', 'OTHERASSETS', 'CAPITALRESERVEFUND','DEFERREDPROCEEDS', 'DIVIDENDPAYABLE',
                                                                                 'FIXEDASSETS', 'GOODWILL',
                                                                                 'OTHERCURRENTLIABILITY',
                                                                                 'NOTESPAYABLE', 'INTANGIBLEASSETS',
                                                                                 'MINORITYINTERESTS',
                                                                                 'ACCOUNTRECEIVABLE', 'TREASURYSTOCK',
                                                                                  'ADVANCEPAYMENT','SHORTTERMLOAN'])
            # print(components['LC_BalanceSheetAll_monthly'])
            components['LC_BalanceSheetAll_monthly_chg'] = self.calculate_change(components['LC_BalanceSheetAll_monthly'])
            # print(components['LC_BalanceSheetAll_monthly_chg']['STARTDAY'])
        except: pass


        try: # t3 LC_IncomeStatementAll
            components['LC_IncomeStatementAll'] = components['LC_IncomeStatementAll'].sort_values(by='ENDDATE')
            components['LC_IncomeStatementAll_monthly'] = self.seasonal_to_monthly(components['LC_IncomeStatementAll'],['NETPROFIT', 'OTHERNETREVENUE','RANDD', 'OPERATINGREVENUE', 'OPERATINGPAYOUT', 'ADMINISTRATIONEXPENSE'])
            components['LC_IncomeStatementAll_monthly_chg'] = self.calculate_change(components['LC_IncomeStatementAll_monthly'])
            # print(components['LC_IncomeStatementAll_monthly_chg'])

        except Exception as e: print(e)
        #
        try: # t4 LC_MainDataNew
            components['LC_MainDataNew'] = components['LC_MainDataNew'].sort_values(by='ENDDATE')
            components['LC_MainDataNew_monthly'] = self.seasonal_to_monthly(components['LC_MainDataNew'],
                                                                            ['TOTALASSETS', 'TOTALCURRENTLIABILITY',
                                                                             'TOTALSHAREHOLDEREQUITY', 'TOTALASSETS',
                                                                             'TOTALCURRENTASSETS', 'INVENTORIES',
                                                                             'TOTALLIABILITY', 'TOTALCURRENTLIABILITY',
                                                                             'TOTALSHAREHOLDEREQUITY'])
            components['LC_MainDataNew_monthly_chg'] = self.calculate_change(components['LC_MainDataNew_monthly'])
            # print(components['LC_MainDataNew_monthly_chg'])
        except: pass

        try: # t5 LC_CashFlowStatementAll 只有分子
            components['LC_CashFlowStatementAll'] = components['LC_CashFlowStatementAll'].sort_values(by='ENDDATE')
            components['LC_CashFlowStatementAll_monthly'] = self.seasonal_to_monthly(components['LC_CashFlowStatementAll'],['CASHEQUIVALENTINCREASE', 'INVENTORYDECREASE', 'NETOPERATECASHFLOW', 'INTANGIBLEASSETAMORTIZATION',
                 'NETINVESTCASHFLOW'])
            components['LC_CashFlowStatementAll_monthly_chg'] = self.calculate_change(components['LC_CashFlowStatementAll_monthly'])
            # print(components['LC_CashFlowStatementAll_monthly_chg'])
        except: pass


        try: # t6 LC_DerivativeData
            components['LC_DerivativeData'] = components['LC_DerivativeData'].sort_values(by='ENDDATE')
            components['LC_DerivativeData_monthly'] = self.seasonal_to_monthly(components['LC_DerivativeData'],
                                                                               ['TOTALOPERATINGCOSTTTM',
                                                                                'RETAINEDEARNINGS', 'GROSSPROFITTTM',
                                                                                'NETWORKINGCAITAL',
                                                                                'TOTALOPERATINGREVENUETTM',
                                                                                'TOTALPAIDINCAPITAL',
                                                                                'TOTALOPERATINGCOSTTTM'])
            components['LC_DerivativeData_monthly_chg'] = self.calculate_change(components['LC_DerivativeData_monthly'])
            # print(components['LC_DerivativeData_monthly_chg'])


        except: pass

        try: # t7 LC_BalanceSheet
            components['LC_BalanceSheet'] = components['LC_BalanceSheet'].sort_values(by='ENDDATE')
            components['LC_BalanceSheet_monthly'] = self.seasonal_to_monthly(components['LC_BalanceSheet'],
                                                                         ['TOTALLONGTERMLIABILITY'])

        except: pass
        try:# t8 LC_Staff
            components['LC_Staff'] = components['LC_Staff'].sort_values(by='ENDDATE')
            components['LC_Staff_monthly'] = self.seasonal_to_monthly(components['LC_Staff'], ['EMPLOYEESUM'])

        except: pass

        return components

    def get_factor_values_2(self, components,numerator, denominator):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        factor_values = pd.DataFrame(components['LC_BalanceSheetAll_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值

        for n in numerator.itertuples(index=True, name='Pandas'):  # 分子
            for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
                factor_name = str(getattr(n, '英文简写')) + 'to' + str(getattr(d, '英文简写')) # 因子名
                n_table = getattr(n,'聚源表名') + '_monthly_chg' #分子表名
                d_table = getattr(d,'聚源表名') + '_monthly'#分母表名
                factor_values[factor_name] = np.nan # 使不同股票因子的个数对齐
                try:
                    factor_values[factor_name] = components[n_table][getattr(n,'聚源字段').upper()] / components[d_table][getattr(d,'聚源字段').upper()]
                    # 某类因子如果存在大于10^6的数值，这个因子取log(1+x)
                    isbig = factor_values[factor_name] >= 10e6    # 判断是否含有大于10e6的值
                    if True in isbig.values:
                        isplus = factor_values[factor_name] >= 0  # 因为log函数的定义域大于零, 所以此处还需要判断是否大于零, 如果小于零则先取绝对值再计算log再加上负号
                        factor_values[factor_name] = np.log1p(np.abs(factor_values[factor_name])) * isplus.mask(isplus == False, -1)
                except Exception as e:
                    print('factor', factor_name, 'error: ', e)

        # 计算与上期的变化百分比
        temp = factor_values.drop(columns=['SECUCODE', 'STARTDAY']).diff(axis=0)
        temp[['SECUCODE', 'STARTDAY']] = factor_values[['SECUCODE', 'STARTDAY']]
        factor_values = temp

        return factor_values

    def write_values_to_DB(self,  code_sql_file_path, data_sql_file_path):

        numerator = pd.read_excel(r'./SeasonalComposedBasicFactor/组合基本面因子.xlsx', sheet_name='分子')
        numerator = numerator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]

        denominator = pd.read_excel(r'./SeasonalComposedBasicFactor/组合基本面因子.xlsx', sheet_name='分母')
        denominator = denominator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]

        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,
                                            ['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,
                                           table_name=['LC_BalanceSheetAll','LC_IncomeStatementAll','LC_MainDataNew','LC_CashFlowStatementAll' ,'LC_DerivativeData','LC_BalanceSheet','LC_Staff'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                # print(data['LC_IncomeStatementAll_monthly_chg'])
                factor_values = self.get_factor_values_2(data,numerator,denominator)

                from sqlalchemy import String, Integer
                print(factor_values)
                # TODO: 表名必须是小写
                # pl_sql_oracle.df_to_DB(factor_values, 'seasonalcomposedbasicfactorf2',if_exists= 'append',data_type={'SECUCODE': String(20), })
                print(self.type, getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print("write to database failed, error: ", getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
    pass
    # scbf_f2 = SeasonalComposedBasicFactorF2()
    # data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_composed_basic_factor_f2n3.sql'
    # code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # data = scbf_f2.find_components(file_path=data_sql_file_path,
    #                             table_name=['LC_BalanceSheetAll', 'LC_IncomeStatementAll', 'LC_MainDataNew',
    #                                         'LC_CashFlowStatementAll', 'LC_DerivativeData', 'LC_BalanceSheet',
    #                                         'LC_Staff'],
    #                             secucode='and t2.Secucode = \'000001\' ')
    # print(data)









