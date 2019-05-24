# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/26  8:39
desc:
'''

import talib
# 集合了工具性代码->技术指标因子->5类技术指标因子


class TechnicalIndicatorFunc(object):
    def __init__(self,high,low,close,open,volume):
        '''
        :param self.high: 最高价
        :param self.low: 最低价
        :param self.close: 收盘价
        :param self.open: 开盘价
        :param volume: 成交量
        '''
        self.high = high
        self.low = low
        self.close = close
        self.open = open
        self.vol = volume

    def CDL2CROWS(self):
        #  三日K线模式，第一天长阳，第二天高开收阴，第三天再次高开继续收阴， 收盘比前一日收盘价低，预示股价下跌。
        return talib.CDL2CROWS(self.open, self.high, self.low, self.close)

    def CDL3BLACKCROWS(self):
        #  三日K线模式，连续三根阴线，每日收盘价都下跌且接近最低价， 每日开盘价都在上根K线实体内，预示股价下跌。
        return talib.CDL3BLACKCROWS(self.open, self.high, self.low, self.close)

    def CDL3INSIDE(self):
        #  三日K线模式，母子信号+长K线，以三内部上涨为例，K线为阴阳阳， 第三天收盘价高于第一天开盘价，第二天K线在第一天K线内部，预示着股价上涨。
        return talib.CDL3INSIDE(self.open, self.high, self.low, self.close)

    def CDL3LINESTRIKE(self):
        # 四日K线模式，前三根阳线，每日收盘价都比前一日高， 开盘价在前一日实体内，第四日市场高开，收盘价低于第一日开盘价，预示股价下跌。
        return talib.CDL3LINESTRIKE(self.open, self.high, self.low, self.close)

    def CDL3STARSINSOUTH(self):
        # 三日K线模式，与大敌当前相反，三日K线皆阴，第一日有长下影线， 第二日与第一日类似，K线整体小于第一日，第三日无下
        # 影线实体信号， 成交价格都在第一日振幅之内，预示下跌趋势反转，股价上升。
        return talib.CDL3STARSINSOUTH(self.open, self.high, self.low, self.close)

    def CDL3WHITESOLDIERS(self):
        # 三日K线模式，三日K线皆阳， 每日收盘价变高且接近最高价，开盘价在前一日实体上半部，预示股价上升。
        return talib.CDL3WHITESOLDIERS(self.open, self.high, self.low, self.close)

    def CDLABANDONEDBABY(self):
        # 三日K线模式，第二日价格跳空且收十字星（开盘价与收盘价接近， 最高价最低价相差不大），预示趋势反转，发生在顶部下跌，底部上涨
        return talib.CDLABANDONEDBABY(self.open, self.high, self.low, self.close, penetration=0)

    def CDLADVANCEBLOCK(self):
        # 三日K线模式，三日都收阳，每日收盘价都比前一日高， 开盘价都在前一日实体以内，实体变短，上影线变长。
        return talib.CDLADVANCEBLOCK(self.open, self.high, self.low, self.close)

    def CDLBELTHOLD(self):
        # 两日K线模式，下跌趋势中，第一日阴线， 第二日开盘价为最低价，阳线，收盘价接近最高价，预示价格上涨。
        return talib.CDLBELTHOLD(self.open, self.high, self.low, self.close)

    def CDLBREAKAWAY(self):
        #  五日K线模式，以看涨脱离为例，下跌趋势中，第一日长阴线，第二日跳空阴线，延续趋势开始震荡， 第五日长阳线，
        # 收盘价在第一天收盘价与第二天开盘价之间，预示价格上涨。
        return talib.CDLBREAKAWAY(self.open, self.high, self.low, self.close)

    def CDLCLOSINGMARUBOZU(self):
        # 一日K线模式，以阳线为例，最低价低于开盘价，收盘价等于最高价， 预示着趋势持续。
        return talib.CDLCLOSINGMARUBOZU(self.open, self.high, self.low, self.close)

    def CDLCONCEALBABYSWALL(self):
        # 四日K线模式，下跌趋势中，前两日阴线无影线 ，第二日开盘、收盘价皆低于第二日，第三日倒锤头， 第四日开盘价高于
        # 前一日最高价，收盘价低于前一日最低价，预示着底部反转。
        return talib.CDLCONCEALBABYSWALL(self.open, self.high, self.low, self.close)

    def CDLCOUNTERATTACK(self):
        # 二日K线模式，与分离线类似。
        return talib.CDLCOUNTERATTACK(self.open, self.high, self.low, self.close)

    def CDLDARKCLOUDCOVER(self):
        # 二日K线模式，第一日长阳，第二日开盘价高于前一日最高价， 收盘价处于前一日实体中部以下，预示着股价下跌。
        return talib.CDLDARKCLOUDCOVER(self.open, self.high, self.low, self.close, penetration=0)

    def CDLDOJI(self):
        # 一日K线模式，开盘价与收盘价基本相同。
        return talib.CDLDOJI(self.open, self.high, self.low, self.close)

    def CDLDOJISTAR(self):
        # 一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转。
        return talib.CDLDOJISTAR(self.open, self.high, self.low, self.close)

    def CDLDRAGONFLYDOJI(self):
        #  一日K线模式，开盘后价格一路走低， 之后收复，收盘价与开盘价相同，预示趋势反转。
        return talib.CDLDRAGONFLYDOJI(self.open, self.high, self.low, self.close)

    def CDLENGULFING(self):
        # 两日K线模式，分多头吞噬和空头吞噬，以多头吞噬为例，第一日为阴线， 第二日阳线，第一日的
        # 开盘价和收盘价在第二日开盘价收盘价之内，但不能完全相同
        return talib.CDLENGULFING(self.open, self.high, self.low, self.close)

    def CDLEVENINGDOJISTAR(self):
        # 三日K线模式，基本模式为暮星，第二日收盘价和开盘价相同，预示顶部反转。
        return talib.CDLEVENINGDOJISTAR(self.open, self.high, self.low, self.close, penetration=0)

    def CDLGAPSIDESIDEWHITE(self):
        # 二日K线模式，上升趋势向上跳空，下跌趋势向下跳空, 第一日与第二日有相同开盘价，实体长度差不多，则趋势持续。
        return talib.CDLGAPSIDESIDEWHITE(self.open, self.high, self.low, self.close)

    def CDLHAMMER(self):
        # 一日K线模式，实体较短，无上影线， 下影线大于实体长度两倍，处于下跌趋势底部，预示反转。
        return  talib.CDLHAMMER(self.open, self.high, self.low, self.close)

    def CDLHARAMI(self):
        # 二日K线模式，分多头母子与空头母子，两者相反，以多头母子为例，在下跌趋势中，第一日K线长阴， 第二日开盘价收盘价在第一日价格振幅之内，为阳线，预示趋势反转，股价上升。
        return talib.CDLHARAMI(self.open, self.high, self.low, self.close)

    def CDLHARAMICROSS(self):
        # 二日K线模式，与母子县类似，若第二日K线是十字线， 便称为十字孕线，预示着趋势反转。
        return talib.CDLHARAMICROSS(self.open, self.high, self.low, self.close)

    def CDLHIKKAKE(self):
        # 三日K线模式，与母子类似，第二日价格在前一日实体范围内, 第三日收盘价高于前两日，反转失败，趋势继续。
        return talib.CDLHIKKAKE(self.open, self.high, self.low, self.close)

    def CDLHIKKAKEMOD(self):
        # 三日K线模式，与陷阱类似，上升趋势中，第三日跳空高开； 下跌趋势中，第三日跳空低开，反转失败，趋势继续。
        return talib.CDLHIKKAKEMOD(self.open, self.high, self.low, self.close)

    def CDLIDENTICAL3CROWS(self):
        # 三日K线模式，上涨趋势中，三日都为阴线，长度大致相等， 每日开盘价等于前一日收盘价，收盘价接近当日最低价，预示价格下跌。
        return talib.CDLIDENTICAL3CROWS(self.open, self.high, self.low, self.close)

    def CDLINVERTEDHAMMER(self):
        # 一日K线模式，上影线较长，长度为实体2倍以上， 无下影线，在下跌趋势底部，预示着趋势反转。
        return talib.CDLINVERTEDHAMMER(self.open, self.high, self.low, self.close)

    def CDLKICKING(self):
        # 二日K线模式，与分离线类似，两日K线为秃线，颜色相反，存在跳空缺口。
        return talib.CDLKICKING(self.open, self.high, self.low, self.close)

    def CDLLADDERBOTTOM(self):
        # 五日K线模式，下跌趋势中，前三日阴线， 开盘价与收盘价皆低于前一日开盘、收盘价，第四日倒锤头，第五
        # 日开盘价高于前一日开盘价， 阳线，收盘价高于前几日价格振幅，预示着底部反转。
        return talib.CDLLADDERBOTTOM(self.open, self.high, self.low, self.close)

    def CDLLONGLEGGEDDOJI(self):
        # 一日K线模式，开盘价与收盘价相同居当日价格中部，上下影线长， 表达市场不确定性。
        return  talib.CDLLONGLEGGEDDOJI(self.open, self.high, self.low, self.close)

    def CDLLONGLINE(self):
        # 一日K线模式，K线实体长，无上下影线。
        return talib.CDLLONGLINE(self.open, self.high, self.low, self.close)

    def CDLMARUBOZU(self):
        # 一日K线模式，上下两头都没有影线的实体， 阴线预示着熊市持续或者牛市反转，阳线相反。
        return talib.CDLMARUBOZU(self.open, self.high, self.low, self.close)

    def CDLMATCHINGLOW (self):
        # 二日K线模式，下跌趋势中，第一日长阴线， 第二日阴线，收盘价与前一日相同，预示底部确认，该价格为支撑位。
        return talib.CDLMATCHINGLOW (self.open, self.high, self.low, self.close)

    def CDLMATHOLD(self):
        # 五日K线模式，上涨趋势中，第一日阳线，第二日跳空高开影线， 第三、四日短实体影线，第五日阳线，收盘价高于前四日，预示趋势持续。
        return talib.CDLMATHOLD(self.open, self.high, self.low, self.close, penetration=0)

    def CDLMORNINGDOJISTAR(self):
        # 三日K线模式， 基本模式为晨星，第二日K线为十字星，预示底部反转。
        return talib.CDLMORNINGDOJISTAR(self.open, self.high, self.low, self.close, penetration=0)

    def CDLONNECK(self):
        # 二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低， 收盘价与前一日最低价相同，阳线，实体较短，预示着延续下跌趋势。
        return talib.CDLONNECK(self.open, self.high, self.low, self.close)

    def CDLRICKSHAWMAN(self):
        # 一日K线模式，与长腿十字线类似， 若实体正好处于价格振幅中点，称为黄包车夫。
        return talib.CDLRICKSHAWMAN(self.open, self.high, self.low, self.close)

    def CDLRISEFALL3METHODS(self):
        # 五日K线模式，以上升三法为例，上涨趋势中， 第一日长阳线，中间三日价格在第一日范围内小幅震荡， 第五日长阳线
        # ，收盘价高于第一日收盘价，预示股价上升。
        return talib.CDLRISEFALL3METHODS(self.open, self.high, self.low, self.close)

    def CDLSEPARATINGLINES(self):
        #  二日K线模式，上涨趋势中，第一日阴线，第二日阳线， 第二日开盘价与第一日相同且为最低价，预示着趋势继续。
        return talib.CDLSEPARATINGLINES(self.open, self.high, self.low, self.close)

    def CDLSHOOTINGSTAR(self):
        # 一日K线模式，上影线至少为实体长度两倍， 没有下影线，预示着股价下跌
        return talib.CDLSHOOTINGSTAR(self.open, self.high, self.low, self.close)

    def CDLSPINNINGTOP(self):
        # 一日K线，实体小。
        return talib.CDLSPINNINGTOP(self.open, self.high, self.low, self.close)

    def CDLSTICKSANDWICH(self):
        # 三日K线模式，第一日长阴线，第二日阳线，开盘价高于前一日收盘价， 第三日开盘价高于前两日最高价，收盘价于第一日收盘价相同。
        return talib.CDLSTICKSANDWICH(self.open, self.high, self.low, self.close)

    def CDLTASUKIGAP(self):
        # 三日K线模式，分上涨和下跌，以上升为例， 前两日阳线，第二日跳空，第三日阴线，收盘价于缺口中，上升趋势持续。
        return talib.CDLTASUKIGAP(self.open, self.high, self.low, self.close)

    def CDLTRISTAR(self):
        # 三日K线模式，由三个十字组成， 第二日十字必须高于或者低于第一日和第三日，预示着反转。
        return talib.CDLTRISTAR(self.open, self.high, self.low, self.close)

    def CDLUNIQUE3RIVER(self):
        # 三日K线模式，下跌趋势中，第一日长阴线，第二日为锤头，最低价创新低，第三日开盘价低于第二日收盘价，收阳线，
        #  收盘价不高于第二日收盘价，预示着反转，第二日下影线越长可能性越大。
        return talib.CDLUNIQUE3RIVER(self.open, self.high, self.low, self.close)

    def CDLUPSIDEGAP2CROWS(self):
        # 三日K线模式，第一日阳线，第二日跳空以高于第一日最高价开盘， 收阴线，第三日开盘价高于第二日，收阴线，与第一日比仍有缺口。
        return talib.CDLUPSIDEGAP2CROWS(self.open, self.high, self.low, self.close)

    def CDLXSIDEGAP3METHODS(self):
        #五日K线模式，以上升跳空三法为例，上涨趋势中，第一日长阳线，第二日短阳线，第三日跳空阳线，第四日阴线
        # ，开盘价与收盘价于前两日实体内， 第五日长阳线，收盘价高于第一日收盘价，预示股价上升
        return talib.CDLXSIDEGAP3METHODS(self.open, self.high, self.low, self.close)

    def HT_dcperiod(self):
        return talib.HT_DCPERIOD(self.close)

    def HT_dcphase(self):
        return talib.HT_DCPHASE(self.close)

    # def HT_phasor(self):
    #     return talib.HT_PHASOR (self.close)

    # def HT_sine(self):
    #     return talib.HT_SINE (self.close)

    def HT_trendmode(self):
        return talib.HT_TRENDMODE (self.close)

    def AveragePrice(self):
        return talib.AVGPRICE(self.open, self.high, self.low, self.close)

    def MedianPrice(self):
        return talib.MEDPRICE(self.high, self.low)

    def TypicalPrice(self):
        return talib.TYPPRICE(self.high, self.low, self.close)

    def WeightedClosePrice(self):
        return talib.WCLPRICE(self.high, self.low, self.close)

    def ADLine(self):
        '''
        多空对比 = [（收盘价- 最低价） - （最高价 - 收盘价）] / （最高价 - 最低价)
        :return:
        '''
        return talib.AD(self.high,self.low,self.close,self.vol)

    def ADOscillator(self):
        '''
        计算公式：fastperiod A/D - slowperiod A/D
        :return:
        '''
        return talib.ADOSC(self.high, self.low, self.close, self.vol, fastperiod=3, slowperiod=10)

    def ADX(self):
        return talib.ADX(self.high, self.low, self.close, timeperiod=14)

    def APO(self):
        return talib.APO(self.close, fastperiod=12, slowperiod=26, matype=0)

    # def AROON(self):
    #     return talib.AROON(self.high, self.low, timeperiod=14)  # aroondown, aroonup 两个输出

    def BOP(self):
        return talib.BOP(self.open, self.high, self.low, self.close)

    def CCI(self):
        return talib.CCI(self.high, self.low, self.close, timeperiod=14)

    def CMO(self):
        return talib.CMO(self.close, timeperiod=14)

    def MACD(self):
        macd, macdsignal, macdhist = talib.MACD(self.close, fastperiod=12, slowperiod=26, signalperiod=9)
        return macd

    def MFI(self):
        return talib.MFI(self.high, self.low, self.close, self.vol, timeperiod=14)

    def MINUS_DI(self):
        return talib.MINUS_DI(self.high, self.low, self.close, timeperiod=14)

    def MOM(self):
        return talib.MOM(self.close, timeperiod=10)

    def PPO(self):
        return talib.PPO(self.close, fastperiod=12, slowperiod=26, matype=0)

    def ROC(self):
        return talib.ROC(self.close, timeperiod=10)

    def ROCP(self):
        return talib.ROCP(self.close, timeperiod=10)

    def RSI(self):
        return talib.RSI(self.close, timeperiod=14)

    # def STOCH(self):
    #     return talib.STOCH(self.high, self.low, self.close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)  # slowk, slowd
    #
    # def STOCHRSI(self):
    #     return talib.STOCHRSI(self.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)  # fastk, fastd

    def TRIX(self):
        return talib.TRIX(self.close, timeperiod=30)

    def WILLR(self):
        return talib.WILLR(self.high, self.low, self.close, timeperiod=14)

    def DEMA(self):
        # 两条移动平均线来产生趋势信号，较长期者用来识别趋势，较短期者用来选择时机。正是两条平均线及价格三者的相互
        # 作用，才共同产生了趋势信号。
        return talib.DEMA(self.close, timeperiod=30)

    def HT_TRENDLINE(self):
        # 是一种趋向类指标，其构造原理是仍然对价格收盘价进行算术平均，并根据计算结果来进行分析，用于判断价格未来走势的变动趋势。
        return talib.HT_TRENDLINE(self.close)

    def MA(self):
        # 移动平均线，Moving Average，简称MA，原本的意思是移动平均，由于我们将其制作成线形，所以一般称之为移动平均线，
        # 简称均线。它是将某一段时间的收盘价之和除以该周期。 比如日线MA5指5天内的收盘价除以5 。
        return talib.MA(self.close, timeperiod=30, matype=0)

    def MIDPOINT (self):

        return talib. MIDPOINT(self.close, timeperiod=14)

    def MIDPRICE(self):

        return talib.MIDPRICE(self.high, self.low, timeperiod=14)

    def SAR(self):

        return talib.SAR(self.high, self.low, acceleration=0, maximum=0)

    def T3(self):
        # TRIX长线操作时采用本指标的讯号，长时间按照本指标讯号交易，获利百分比大于损失百分比，利润相当可观。 比如
        # 日线MA5指5天内的收盘价除以5 。
        return talib.T3(self.close, timeperiod=5, vfactor=0)

    def WMA(self):

        return talib.WMA(self.close, timeperiod=30)