import sys
from PyQt5.QtWidgets import *
import Kiwoom
import time
from pandas import DataFrame
import datetime
import webreader
import numpy as np
import re


class PySell:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_bought_code_list()

    def get_bought_code_list(self):
        f = open("buy_list.txt", 'rt')
        buy_list = f.readlines()
        f.close()
        self.bought_list = []
        for i in range(0, 5):
            bought = re.split(';', buy_list[i])
            if bought[-1] == '주문완료\n':
                self.bought_list.append(bought[1])

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.2)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                       index=self.kiwoom.ohlcv['date'])
        return df

    def check_speedy_decreasing_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20 / 20
        if today_vol < avg_vol20 / 2:  ## 20일 평균보다 절반 떨어졌을 경우
            return True

    def update_sell_list(self, sell_list):
        f = open("sell_list.txt", "wt")
        for code in sell_list:
            f.writelines("매도;", code, ";시장가;10;0;매도전")
        f.close()

    def run(self):
        sell_list = []
        num = len(self.bought_list)

        for i, code in enumerate(self.bought_list):
            print(code, i, '/', num)
            if self.check_speedy_decreasing_volume(code):
                sell_list.append(code)

        self.update_sell_list(sell_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pysell = PySell()
    pysell.run()