import urllib.request
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import numpy as np


def get_annual_dividend_yield(code):
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A%s&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701=" % (
        code)
    f = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(f, 'html5lib')
    now = datetime.datetime.now()
    cur_year = now.year
    nan_previous_dividend_yield = {}
    nan_previous_dividend = [np.nan] * 8
    previous_dividend = [np.nan] * 8
    for i, year in enumerate(range(cur_year - 5, cur_year + 3)):
        nan_previous_dividend_yield[year] = nan_previous_dividend[i]

    table_data = soup.find_all('table', {'class': "us_table_ty1 h_fix zigbg_no"})
    if len(table_data) < 5 :
        return  pd.Series(nan_previous_dividend_yield)
    elif len(table_data) >=5 :
        tr_data = table_data[5].find_all('tr')[-1]
        if len(tr_data) < 1 :
            return  pd.Series(nan_previous_dividend_yield)
        elif len(tr_data) >= 1 :
            td_data = tr_data.find_all('td')
            if len(td_data) <1 :
                return pd.Series(nan_previous_dividend_yield)
            elif len(td_data) >= 1 :
                for i in range(len(td_data)):
                    td_text = td_data[i].get_text()
                    if td_text == '\xa0':
                        td_text = np.nan
                    elif td_text != '\xa0':
                        td_text = float(td_text)
                    else :
                        td_text = np.nan
                    previous_dividend[i] = td_text

    previous_dividend_yield = {}

    for i, year in enumerate(range(cur_year - 5, cur_year + 3)):
        if np.isnan(previous_dividend[i]) == 0 :
            previous_dividend_yield[year] = previous_dividend[i]
        elif np.isnan(previous_dividend[i]) == 1 :
            previous_dividend_yield[year] = np.nan
        else :
            previous_dividend_yield[year] = np.nan

    return pd.Series(previous_dividend_yield)

def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')
    td_data = soup.find_all('td', {'class': 'cmp-table-cell td0301'})

    if not td_data:
        return np.nan

    dt_data = td_data[0].find_all('dt')

    if not dt_data:
        return np.nan

    dividend_yield = dt_data[5].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]
    if dividend_yield.replace(".", "").isdigit() == 1 :
        return float(dividend_yield)
    elif dividend_yield.replace(".", "").isdigit() == 0 :
        return np.nan
    else :
        return np.nan


def get_estimated_dividend_yield(code):
    dividend_yield  = get_annual_dividend_yield(code)
    now = datetime.datetime.now()
    cur_year = now.year

    if np.isnan(dividend_yield[cur_year]) == 0 :
        return dividend_yield[cur_year]
    elif np.isnan(dividend_yield[cur_year]) == 1 :
        return get_dividend_yield(code)
    else:
        return np.NaN


def get_previous_dividend_yield(code):
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A%s&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701=" % (
        code)
    f = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(f, 'html5lib')
    now = datetime.datetime.now()
    cur_year = now.year
    nan_previous_dividend_yield = {}
    nan_previous_dividend = [np.nan] * 5
    previous_dividend = [np.nan] * 5
    for i, year in enumerate(range(cur_year - 5, cur_year)):
        nan_previous_dividend_yield[year] = nan_previous_dividend[i]

    table_data = soup.find_all('table', {'class': "us_table_ty1 h_fix zigbg_no"})
    if not table_data:
        return nan_previous_dividend_yield
    tr_data = table_data[5].find_all('tr')[-1]
    if not tr_data:
        return nan_previous_dividend_yield
    td_data = tr_data.find_all('td')[0:5]
    if not td_data:
        return nan_previous_dividend_yield
    for i in range(len(td_data)):
        td_text = td_data[i].get_text()
        if td_text == '\xa0':
            td_text = np.nan
        elif td_text != '\xa0':
            td_text = float(td_text)
        else :
            td_text = np.nan
        previous_dividend[i] = td_text

    previous_dividend_yield = {}

    for i, year in enumerate(range(cur_year - 5, cur_year)):
        if np.isnan(previous_dividend[i]) == 0 :
            previous_dividend_yield[year] = previous_dividend[i]
        elif np.isnan(previous_dividend[i]) == 1 :
            previous_dividend_yield[year] = np.nan
        else :
            previous_dividend_yield[year] = np.nan

    return previous_dividend_yield


def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2016"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    tr_data = soup.find_all('tr', id='tr_288401_1')
    td_data = tr_data[0].find_all('td')

    treasury_3year = {}
    start_year = 1998

    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1

    # print(treasury_3year)
    return treasury_3year


def get_current_3year_treasury():
    url = "http://info.finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')
    tbody_data = soup.find_all('tbody')
    tr_data = tbody_data[0].find_all('tr')
    td_data = tr_data[0].find_all('td')
    return td_data[1].text


if __name__ == "__main__":
    # df = get_financial_statements('035720')
    # print(df)
    # get_3year_treasury()
    # dividend_yield = get_dividend_yield('058470')
    # print(dividend_yield)
    # estimated_dividend_yield = get_estimated_dividend_yield('058470')
    # print(estimated_dividend_yield)
    # print(get_current_3year_treasury())
    print(get_previous_dividend_yield('058470'))