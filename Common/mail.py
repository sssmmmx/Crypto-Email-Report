# -*- coding = utf-8 -*-
# @time:2021/10/23 21:42
# Author:ldx
# @File:mail.py
# @Software:PyCharm

# 邮件功能 使用邮箱发送邮件的功能

import time
import smtplib
from email.mime.text import MIMEText


# ================发送邮件=============

content = "邮件测试"

# 获取今天的字符串
today = time.strftime("%Y-%m-%d", time.localtime(time.time()))

# 邮箱集合
msg_to_list = ['lindingxuan@qq.com', 'otakuho@gmail.com']


msg_from = 'lindingxuan@qq.com'  # 发送方邮箱
passwd = 'zumiovtsbuawcjbd'  # 填入发送方邮箱的授权码
msg_to = 'lindingxuan@qq.com' # 收件人邮箱
subject = today+" OKEX参数报告"  # 主题

# msg = MIMEText(content)

msg = MIMEText(content, "html", "utf-8")

msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

try:
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)    # 邮件服务器及端口号
    s.login(msg_from, passwd)
    for msg_to in msg_to_list:
        s.sendmail(msg_from, msg_to, msg.as_string())
        print(msg_to, "发送成功")

except():   # s.SMTPException
    print("发送失败")

finally:
    s.quit()
