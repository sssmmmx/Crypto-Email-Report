# -*- coding = utf-8 -*-
# @time:2021/12/16 19:53
# Author:ldx
# @File:QueryTool.py
# @Software:PyCharm

import pandas as pd
import time as t
from Common.generic.config import publicAPI, marketAPI


def qx1(data, col):
    t0 = t.mktime(t.strptime(col[0], "%y%m%d"))
    t1 = t.mktime(t.strptime(col[1], "%y%m%d"))
    t2 = t.mktime(t.strptime(col[2], "%y%m%d"))
    t3 = t.mktime(t.strptime(col[3], "%y%m%d"))
    t4 = t.mktime(t.strptime(col[4], "%y%m%d"))

    data['CW%'] = (data[col[1]] - data[col[0]]) / data[col[0]] * 100
    data['CW%'] = data['CW%'].apply(lambda x: round(x, 2))
    data['CWdays'] = int((t1 - t0) / (24 * 60 * 60)) - 1

    data['NW%'] = (data[col[2]] - data[col[0]]) / data[col[0]] * 100
    data['NW%'] = data['NW%'].apply(lambda x: round(x, 2))
    data['NWdays'] = int((t2 - t0) / (24 * 60 * 60)) - 1

    data['CS%'] = (data[col[3]] - data[col[0]]) / data[col[0]] * 100
    data['CS%'] = data['CS%'].apply(lambda x: round(x, 2))
    data['CSdays'] = int((t3 - t0) / (24 * 60 * 60)) - 1

    data['NS%'] = (data[col[4]] - data[col[0]]) / data[col[0]] * 100
    data['NS%'] = data['NS%'].apply(lambda x: round(x, 2))
    data['NSdays'] = int((t4 - t0) / (24 * 60 * 60)) - 1
    return data


def qx2(data, col):
    t0 = t.mktime(t.strptime(col[0], "%y%m%d"))
    t1 = t.mktime(t.strptime(col[1], "%y%m%d"))
    t2 = t.mktime(t.strptime(col[2], "%y%m%d"))
    t3 = t.mktime(t.strptime(col[3], "%y%m%d"))

    data['CW%'] = (data[col[1]] - data[col[0]]) / data[col[0]] * 100
    data['CW%'] = data['CW%'].apply(lambda x: round(x, 2))
    data['CWdays'] = int((t1 - t0) / (24 * 60 * 60)) - 1

    data['NW%'] = (data[col[2]] - data[col[0]]) / data[col[0]] * 100
    data['NW%'] = data['NW%'].apply(lambda x: round(x, 2))
    data['NWdays'] = int((t2 - t0) / (24 * 60 * 60)) - 1

    data['CS%'] = (data[col[3]] - data[col[0]]) / data[col[0]] * 100
    data['CS%'] = data['CS%'].apply(lambda x: round(x, 2))
    data['CSdays'] = int((t3 - t0) / (24 * 60 * 60)) - 1

    return data


def qxinfo():
    # ==== 期现套利相关信息 ====
    futurelist = []
    spotlist = []

    # 获取交易产品基础信息
    future_info = publicAPI.get_instruments(instType='FUTURES')
    future_info = future_info['data']
    for info in future_info:
        if info['settleCcy'] == 'USDT':
            futurelist.append(info['instId'])

    # 获取期货的交易数据 U本位 期货和价格一一对应
    futuredic = {}
    for f in futurelist:
        spotlist.append(f[:-7])
        future_market = marketAPI.get_ticker(instId=f)
        f_last = future_market['data'][0]['last']
        futuredic[f] = f_last
        t.sleep(0.1)

    # 去重
    spotlist = list(set(spotlist))
    spotdic = {}
    # 获取spot的交易数据
    for s in spotlist:
        spot_market = marketAPI.get_ticker(instId=s)
        s_last = spot_market['data'][0]['last']
        spotdic[s] = s_last
        t.sleep(0.1)

    # 数据解析部分 构建datafram 先构建qxdic={}
    date = []
    for ft in futurelist:
        date.append(int(ft[-6:]))
    date = list(set(date))
    date.sort()

    qxdic = {}
    qxlist0 = []  # BTC-USDT
    qxlist1 = []  # 当周
    qxlist2 = []  # 次周
    qxlist3 = []  # 当季
    qxlist4 = []  # 次季

    for d in list(spotdic.keys()):
        qxlist0.append(spotdic[d])
        for k in range(len(date)):
            j = d + '-' + str(date[k])
            if k == 0:
                qxlist1.append(futuredic[j])
            if k == 1:
                qxlist2.append(futuredic[j])
            if k == 2:
                qxlist3.append(futuredic[j])
            if k == 3:
                qxlist4.append(futuredic[j])

    # 获取今天的字符串
    today = t.strftime("%Y%m%d", t.localtime(t.time()))
    today = today[2:]

    # qxdic['instId'] = list(spotdic.keys())
    qxdic[today] = qxlist0
    if len(date) == 4:
        qxdic[str(date[0])] = qxlist1
        qxdic[str(date[1])] = qxlist2
        qxdic[str(date[2])] = qxlist3
        qxdic[str(date[3])] = qxlist4
    elif len(date) == 3:
        qxdic[str(date[0])] = qxlist1
        qxdic[str(date[1])] = qxlist2
        qxdic[str(date[2])] = qxlist3
    else:
        print("数据未全部更新，请稍后再试。")
        exit()

    data = pd.DataFrame(qxdic)
    data.index = list(spotdic.keys())

    # print(data)
    # print("\n==================计算后的结果====================\n")

    data = data.astype('float')

    col = list(data.columns)
    if len(col) == 5:
        data = qx1(data,col)
    else:
        data = qx2(data,col)

    data['instId'] = list(spotdic.keys())

    data['absnw'] = abs(data['NW%'])

    df = data.sort_values(by='absnw', ascending=False)

    if len(col) == 5:
        df = df[['instId', 'CW%', 'CWdays', 'NW%', 'NWdays', 'CS%', 'CSdays', 'NS%', 'NSdays']]

        df.columns = ['ID', '当周', col[1], '次周', col[2], '当季', col[3], '次季', col[4]]
    else:
        df = df[['instId', 'CW%', 'CWdays', 'NW%', 'NWdays', 'CS%', 'CSdays']]

        df.columns = ['ID', '当周', col[1], '次周', col[2], '当季', col[3]]

    # print(df)

    return df,col


def zjfinfo():
    swaplist = []

    # 获取交易产品基础信息
    all_info = publicAPI.get_instruments(instType='SWAP')
    all_info = all_info['data']
    for info in all_info:
        if info['settleCcy'] == 'USDT':
            swaplist.append(info['instId'])

    # 获取永续合约当前资金费率

    hisswapdic = {}
    hisswaplist1 = []
    hisswaplist2 = []
    hisswaplist3 = []
    hisswaplist4 = []

    print('===========================')
    hrate = publicAPI.funding_rate_history(instId="BTC-USDT-SWAP")

    # 初始时间戳
    t0 = hrate['data'][0]['fundingTime']
    t1 = int(t0) - 2851300000
    t2 = int(t0) - 2 * 2851300000
    t3 = int(t0) - 3 * 2851300000

    for n in swaplist:
        hisswaplist1.append(n)
        hrate = publicAPI.funding_rate_history(instId=n)
        hrate2 = publicAPI.funding_rate_history(instId=n,before=str(t2))
        hrate3 = publicAPI.funding_rate_history(instId=n,before=str(t3))

        h = len(hrate['data'])
        h90 = len(hrate2['data']) + len(hrate3['data'])

        hsum = 0
        for i in range(10,h):
            hsum = hsum + float(hrate['data'][i]['realizedRate'])

        hisswaplist3.append(hsum)  # 30天所有资金费累加
        havg = hsum / 30 * 3
        hisswaplist2.append(havg)  # 每天平均资金费

        hsum90 = 0
        if h90 < 200:
            hsum90 = 0
        else:
            for i in range(h):
                hsum90 = hsum90 + float(hrate['data'][i]['realizedRate'])

            for j in range(len(hrate2['data']) ):
                hsum90 = hsum90 + float(hrate['data'][j]['realizedRate'])

            for k in range(30,len(hrate3['data'])):
                hsum90 = hsum90 + float(hrate['data'][k]['realizedRate'])

        hisswaplist4.append(hsum90)  # 90天所有资金费累加




    hisswapdic['永续名称'] = hisswaplist1
    hisswapdic['平均每日资金费'] = hisswaplist2
    hisswapdic['30天资金费累加'] = hisswaplist3
    hisswapdic['90天资金费累加'] = hisswaplist4



    data = pd.DataFrame(hisswapdic)

    # 取绝对值
    data['abshsum'] = abs(data['30天资金费累加'])
    data['30天年化'] = 100 * data['30天资金费累加'] / 30 * 365
    data['90天年化'] = 100 * data['90天资金费累加'] / 90 * 365

    df = data.sort_values(by='abshsum', ascending=False)
    df = df[['永续名称', '30天资金费累加', '30天年化', '90天资金费累加', '90天年化']]

    return df


def bzjfinfo():
    swaplist = []

    # 获取交易产品基础信息
    all_info = publicAPI.get_instruments(instType='SWAP')
    all_info = all_info['data']
    for info in all_info:
        if info['settleCcy'] != 'USDT':
            swaplist.append(info['instId'])

    # 获取永续合约当前资金费率

    hisswapdic = {}
    hisswaplist1 = []
    hisswaplist2 = []
    hisswaplist3 = []
    hisswaplist4 = []

    print('===========================')
    hrate = publicAPI.funding_rate_history(instId="BTC-USD-SWAP")

    # 初始时间戳
    t0 = hrate['data'][0]['fundingTime']
    t1 = int(t0) - 2851300000
    t2 = int(t0) - 2 * 2851300000
    t3 = int(t0) - 3 * 2851300000

    for n in swaplist:
        hisswaplist1.append(n)
        hrate = publicAPI.funding_rate_history(instId=n)
        hrate2 = publicAPI.funding_rate_history(instId=n,before=str(t2))
        hrate3 = publicAPI.funding_rate_history(instId=n,before=str(t3))

        h = len(hrate['data'])
        h90 = len(hrate2['data']) + len(hrate3['data'])

        hsum = 0
        for i in range(10,h):
            hsum = hsum + float(hrate['data'][i]['realizedRate'])

        hisswaplist3.append(hsum)  # 30天所有资金费累加
        havg = hsum / 30 * 3
        hisswaplist2.append(havg)  # 每天平均资金费

        hsum90 = 0
        if h90 < 200:
            hsum90 = 0

        else:
            for i in range(h):
                hsum90 = hsum90 + float(hrate['data'][i]['realizedRate'])

            for j in range(len(hrate2['data']) ):
                hsum90 = hsum90 + float(hrate['data'][j]['realizedRate'])

            for k in range(30,len(hrate3['data'])):
                hsum90 = hsum90 + float(hrate['data'][k]['realizedRate'])

        hisswaplist4.append(hsum90)  # 90天所有资金费累加


    hisswapdic['永续名称'] = hisswaplist1
    hisswapdic['平均每日资金费'] = hisswaplist2
    hisswapdic['30天资金费累加'] = hisswaplist3
    hisswapdic['90天资金费累加'] = hisswaplist4

    data = pd.DataFrame(hisswapdic)

    # 取绝对值
    data['abshsum'] = abs(data['30天资金费累加'])
    data['30天年化'] = 100 * data['30天资金费累加'] / 30 * 365
    data['90天年化'] = 100 * data['90天资金费累加'] / 90 * 365
    df_a = data[['永续名称', '30天资金费累加', '30天年化', '90天资金费累加', '90天年化']].head(2)
    df = data.sort_values(by='abshsum', ascending=False)
    df_b = df[['永续名称', '30天资金费累加', '30天年化', '90天资金费累加', '90天年化']].head(8)

    return df_a, df_b

