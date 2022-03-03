# -*- coding = utf-8 -*-
# @time:2021/12/16 20:01
# Author:ldx
# @File:qq_report.py
# @Software:PyCharm
# QQ邮件 信息播报程序
# coding=utf-8

import datetime
from QueryTool import *
import smtplib
from email.mime.text import MIMEText

df_a, df_b = bzjfinfo()
df0 = zjfinfo()
df1 = df0.head(10)
df2, col = qxinfo()
today = datetime.date.today()

hold = ['FLM','STARL','SWRV','LAT','BTM','MINA','CFX','KISHU','CONV']

zjf3090 = ""
zjf_detail = ""
bzjf3090 = ""
qxxx = ""
qxfirst = ""

df3 = df0[df0['30天资金费累加'] > 0].head(10)
df4 = df0[df0['30天资金费累加'] < 0].head(10)

try:
    # zjf3090 = ""
    for q in df1.index:
        dl = list(df1.loc[q].values)

        font_color = "black"

        # 判断正负 更改颜色
        if float(dl[1]) < 0:
            font_color = "red"

        # 打*标记
        if dl[0][:-10] in hold:
            dl_id = "*"+ dl[0][:-10]
        else:
            dl_id = dl[0][:-10]

        zjf3090 = zjf3090 + """
<tr align="center">
<td>{}</td>
<td><p style="color:{}">{:.2f}%</p></td>
<td><p style="color:{}">{:.2f}%</p></td>
<td><p style="color:{}">{:.2f}%</p></td>
<td><p style="color:{}">{:.2f}%</p></td></tr>
""".format(dl_id, font_color, 100 * float(dl[1]), font_color, float(dl[2]), font_color, 100 * float(dl[3]),
           font_color, float(dl[4]))

    # ---------- 计算U本位正负资金费的详情 ----------
    len3 = len(list(df3.index))
    len4 = len(list(df4.index))

    for j in range(10):
        if j < len3:
            k3 = list(df3.index)[j]
            unit3 = list(df3.loc[k3].values)
        else:
            unit3 = ['null', 0, 0, 0, 0]

        if j < len4:
            k4 = list(df4.index)[j]
            unit4 = list(df4.loc[k4].values)
        else:
            unit4 = ['null', 0, 0, 0, 0]

        # 打*标记
        if unit3[0][:-10] in hold:
            unit3_id = "*"+ unit3[0][:-10]
        else:
            unit3_id = unit3[0][:-10]

        # 打*标记
        if unit4[0][:-10] in hold:
            unit4_id = "*"+ unit4[0][:-10]
        else:
            unit4_id = unit4[0][:-10]

        # 计算U本位正负资金费的详情
        zjf_detail = zjf_detail + """
<tr align="center">
<td>{}</td>
<td>{:.2f}%</td>
<td>{:.2f}%</td>
<td>{:.2f}%</td>
<td>{:.2f}%</td>
<td><p style="color:red">{}</p></td>
<td><p style="color:red">{:.2f}%</p></td>
<td><p style="color:red">{:.2f}%</p></td>
<td><p style="color:red">{:.2f}%</p></td>
<td><p style="color:red">{:.2f}%</p></td>
</tr>
""".format(unit3_id, 100 * float(unit3[1]), float(unit3[2]), 100 * float(unit3[3]), float(unit3[4]),
           unit4_id, 100 * float(unit4[1]), float(unit4[2]), 100 * float(unit4[3]), float(unit4[4]))

    # bzjf3090 = ""
    for w in df_a.index:
        dl = list(df_a.loc[w].values)

        font_color = "black"

        # 判断正负 更改颜色
        if float(dl[1]) < 0:
            font_color = "red"

        bzjf3090 = bzjf3090 + """
<tr align="center">
<td width="80">{}</td>
<td width="80"><p style="color:{}">{:.2f}%</p></td>
<td width="80"><p style="color:{}">{:.2f}%</p></td>
<td width="80"><p style="color:{}">{:.2f}%</p></td>
<td width="80"><p style="color:{}">{:.2f}%</p></td></tr>
""".format(dl[0][:-9], font_color, 100 * float(dl[1]), font_color, float(dl[2]), font_color, 100 * float(dl[3]),
           font_color, float(dl[4]))

    for y in df_b.index:
        dl = list(df_b.loc[y].values)

        font_color = "black"

        # 判断正负 更改颜色
        if float(dl[1]) < 0:
            font_color = "red"

        bzjf3090 = bzjf3090 + """
<tr align="center">
<td>{}</td>
<td><p style="color:{}">{:.2f}%</p></td>
<td><p style="color:{}">{:.2f}%</p></td>
<td><p style="color:{}">{:.2f}%</p></td>
<td><p style="color:{}">{:.2f}%</p></td></tr>
""".format(dl[0][:-9], font_color, 100 * float(dl[1]), font_color, float(dl[2]), font_color, 100 * float(dl[3]),
           font_color, float(dl[4]))

    # qxxx = ""
    if len(col) == 5:
        for x in df2.index:
            dl = list(df2.loc[x].values)

            if float(dl[2]) == 0:
                n1 = 0
            else:
                n1 = abs(float(dl[1]) / float(dl[2]) * 365)
            if float(dl[4]) == 0:
                n2 = 0
            else:
                n2 = abs(float(dl[3]) / float(dl[4]) * 365)
            if float(dl[6]) == 0:
                n3 = 0
            else:
                n3 = abs(float(dl[5]) / float(dl[6]) * 365)
            if float(dl[8]) == 0:
                n4 = 0
            else:
                n4 = abs(float(dl[7]) / float(dl[8]) * 365)

            font_color = "black"

            # 判断正负 更改颜色
            if float(dl[1]) < 0:
                font_color = "red"

            qxxx = qxxx + """
<tr align="center">
<td>{}</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td></tr>
""".format(dl[0][:-5], dl[1], n1, dl[2], dl[3], n2, dl[4], dl[5], n3, dl[6], dl[7], n4, dl[8])

        qxfirst = """
<tr align="center">
<td> ID </td>
<td>当周</td><td>年化</td><td>{}</td>
<td>次周</td><td>年化</td><td>{}</td>
<td>当季</td><td>年化</td><td>{}</td>
<td>次季</td><td>年化</td><td>{}</td></tr>""".format(col[1], col[2], col[3], col[4])

    else:
        for z in df2.index:
            dl = list(df2.loc[z].values)

            if float(dl[2]) == 0:
                n1 = 0
            else:
                n1 = abs(float(dl[1]) / float(dl[2]) * 365)
            if float(dl[4]) == 0:
                n2 = 0
            else:
                n2 = abs(float(dl[3]) / float(dl[4]) * 365)
            if float(dl[6]) == 0:
                n3 = 0
            else:
                n3 = abs(float(dl[5]) / float(dl[6]) * 365)

            qxxx = qxxx + """
<tr align="center">
<td>{}</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td>
<td>{}%</td><td><p style="color:green">{:.2f}%</p></td><td>{}天</td></tr>
""".format(dl[0][:-5], dl[1], n1, dl[2], dl[3], n2, dl[4], dl[5], n3, dl[6])

        qxfirst = """
<tr align="center">
<td> ID </td>
<td>当周</td>
<td>年化</td>
<td>{}</td>
<td>次周</td>
<td>年化</td>
<td>{}</td>
<td>当季</td>
<td>年化</td>
<td>{}</td></tr>""".format(col[1], col[2], col[3])

except (Exception, BaseException) as e:
    content = """异常,{}""".format(e)
    print(content)
    t.sleep(1)

# ================发送邮件=============

content_s = """<table border="0" cellspacing="0" cellpadding="4" width="800">"""
sp = """<tr><td bgcolor="#ffffff" height="30"></td></tr>"""
content_e = """</table>"""

content_zjf = """
<tr><td bgcolor="#00a6ac" height="30" style="font-size:110%;color:white">OKEX 资金费播报 U本位 </td></tr>
<tr><td bgcolor="#78cdd1" style="font-size:13px">
<table border="0" width="800">
<tr align="center">
<td>ID</td>
<td>SUM 30</td>
<td>APR 30</td>
<td>SUM 90</td>
<td>APR 90</td>
</tr>""" + zjf3090 + """</table></td></tr>"""

content_detail = """
<tr><td bgcolor="#00a6ac" style="font-size:13px"><table><tr>
<td height="30" width= "400" style="font-size:100%; color:white">正资金费</td>
<td height="30" width= "400" style="font-size:100%; color:white">负资金费</td>
</tr></table></td></tr>
<tr>
<td bgcolor="#78cdd1" style="font-size:13px">
<table border="0" width= "800">
<tr align="center">
<td>ID</td>
<td>SUM 30</td>
<td>APR 30</td>
<td>SUM 90</td>
<td>APR 90</td>
<td>ID</td>
<td>SUM 30</td>
<td>APR 30</td>
<td>SUM 90</td>
<td>APR 90</td>
</tr>
""" + zjf_detail + """</table></td></tr>"""

content_bzjf = """
<tr><td bgcolor="#00a6ac" height="30" style="font-size:110%;color:white">OKEX 资金费播报 币本位 </td></tr>
<tr><td bgcolor="#78cdd1" style="font-size:13px">
<table border="0" width="800">
<tr align="center">
<td>ID</td>
<td>SUM 30</td>
<td>APR 30</td>
<td>SUM 90</td>
<td>APR 90</td>
</tr>""" + bzjf3090 + """</table></td></tr>"""


content_qx = """
<tr><td bgcolor="#00a6ac" height="30" style="font-size:110%;color:white">OKEX 期现差播报 U本位 </td></tr>
<tr><td bgcolor="#78cdd1" style="font-size:13px " ><table border="0"  width="800">
""" + qxfirst + qxxx + """</table></td></tr>"""

content = content_s + content_zjf + sp + content_detail + sp + content_bzjf + sp + content_qx + content_e

# 获取今天的字符串
today = t.strftime("%Y-%m-%d", t.localtime(t.time()))


# 邮箱集合
msg_to_list = ['xxx@qq.com']

msg_from = 'xxx@qq.com'     # 发送方邮箱
passwd = 'xxxxxxxxxxxxxx'         # 填入发送方邮箱的授权码
msg_to = 'xxx@qq.com'       # 收件人邮箱

subject = today+" OKEX套利参数报告"      # 主题

# msg = MIMEText(content)

msg = MIMEText(content, "html", "utf-8")

msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

s = smtplib.SMTP_SSL("smtp.qq.com", 465)    # 邮件服务器及端口号

try:
    s.login(msg_from, passwd)
    for msg_to in msg_to_list:
        s.sendmail(msg_from, msg_to, msg.as_string())
        print(msg_to, "发送成功")

except():
    print("发送失败")

finally:
    s.quit()
