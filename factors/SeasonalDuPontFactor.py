# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import SeasonalFrequency
from factors.Category import DuPontFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
季频杜邦分析体系因子

代码表：
    1301	EquityMultipler_DuPont
    1302	NPPCToNP_DuPont
    1303	NPToTOR_DuPont
    1304	NPToTP_DuPont
    1305	TPToEBIT_DuPont
    1306	EBITToTOR_DuPont


"""

class SeasonalDuPontFactor(SeasonalFrequency,DuPontFactor ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频杜邦分析体系'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # EquityMultipler_DuPont 权益乘数_杜邦分析(%)
        EquityMultipler_DuPont = SeasonalDuPontFactor(factor_code='1301',
                                                      name='EquityMultipler_DuPont',
                                                      describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['EquityMultipler_DuPont'] = EquityMultipler_DuPont

        # NPPCToNP_DuPont 归属母公司股东的净利润/净利润(%)
        NPPCToNP_DuPont = SeasonalDuPontFactor(factor_code='1302',
                                               name='NPPCToNP_DuPont',
                                               describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPPCToNP_DuPont'] = NPPCToNP_DuPont

        # NPToTOR_DuPont 净利润/营业总收入(%)
        NPToTOR_DuPont = SeasonalDuPontFactor(factor_code='1303',
                                              name='NPToTOR_DuPont',
                                              describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPToTOR_DuPont'] = NPToTOR_DuPont

        # NPToTP_DuPont 净利润/利润总额(%)
        NPToTP_DuPont = SeasonalDuPontFactor(factor_code='1304',
                                             name='NPToTP_DuPont',
                                             describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPToTP_DuPont'] = NPToTP_DuPont

        # TPToEBIT_DuPont 利润总额/息税前利润(%)
        TPToEBIT_DuPont = SeasonalDuPontFactor(factor_code='1305',
                                               name='TPToEBIT_DuPont',
                                               describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['TPToEBIT_DuPont'] = TPToEBIT_DuPont

        # EBITToTOR_DuPont 息税前利润/营业总收入(%)
        EBITToTOR_DuPont = SeasonalDuPontFactor(factor_code='1306',
                                                name='EBITToTOR_DuPont',
                                                describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['EBITToTOR_DuPont'] = EBITToTOR_DuPont

        return factor_entities

    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # TODO: 读取时需要按时间排序
        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')

        # 如果需要转换
        components['LC_MainIndexNew_monthly']  = self.seasonal_to_monthly(components['LC_MainIndexNew'],['EQUITYMULTIPLER_DUPONT', 'NPPCTONP_DUPONT', 'NPTOTOR_DUPONT', 'NPTOTP_DUPONT', 'TPTOEBIT_DUPONT', 'EBITTOTOR_DUPONT'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['EquityMultipler_DuPont'] = components['LC_MainIndexNew_monthly']['EQUITYMULTIPLER_DUPONT']
        factor_values['NPPCToNP_DuPont'] = components['LC_MainIndexNew_monthly']['NPPCTONP_DUPONT']
        factor_values['NPToTOR_DuPont'] = components['LC_MainIndexNew_monthly']['NPTOTOR_DUPONT']
        factor_values['NPToTP_DuPont'] = components['LC_MainIndexNew_monthly']['NPTOTP_DUPONT']
        factor_values['TPToEBIT_DuPont'] = components['LC_MainIndexNew_monthly']['TPTOEBIT_DUPONT']
        factor_values['EBITToTOR_DuPont'] = components['LC_MainIndexNew_monthly']['EBITTOTOR_DUPONT']
        return factor_values



    def write_values_to_DB(self,  code_sql_file_path, data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,
                                            ['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,
                                           table_name=['LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)


                from sqlalchemy import String, Integer
                print(factor_values)
                pl_sql_oracle.df_to_DB(factor_values, 'seasonaldupontfactor',if_exists= 'append',data_type={'SECUCODE': String(20)})

                print(self.type, getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print("write to database failed, error: ", getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
    sdpf = SeasonalDuPontFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_dupont_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    sdpf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

