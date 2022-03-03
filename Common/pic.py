# -*- coding = utf-8 -*-
# @time:2021/11/3 18:06
# Author:ldx
# @File:pic.py
# @Software:PyCharm

from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont


def image(field_names, content, image_name):

    # # 设置表头
    # tab.field_names = ["Name", "Age", "Country", "City"]
    # # 表格内容插入
    # tab.add_row(['chal', '23', '中国', 'Shanghai'])
    # tab.add_row(['charle', '29', 'China', 'Xuzhou'])
    # tab.add_row(['jack', '32', 'United States', 'Washington'])

    tab = PrettyTable()
    # 设置表头
    tab.field_names = field_names
    # 表格内容插入
    for c in content:
        tab.add_row(c)

    tab_info = str(tab)
    space = 5

    # PIL模块中，确定写入到图片中的文本字体
    # ubuntu
    font = ImageFont.truetype('/home/doge/YaHeiConsolas.ttf', 15, encoding='utf-8')
    # windows
    # font = ImageFont.truetype('simsun.ttc', 15, encoding='utf-8')
    # Image模块创建一个图片对象
    im = Image.new('RGB', (10, 10), (255, 255, 255, 0))
    # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
    draw = ImageDraw.Draw(im, "RGB")
    # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
    img_size = draw.multiline_textsize(tab_info, font=font)
    # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    # 批量写入到图片中，这里的multiline_text会自动识别换行符
    # python2
    # draw.multiline_text((space,space), unicode(tab_info, 'utf-8'), fill=(255,255,255), font=font)
    # python3
    draw.multiline_text((space, space), tab_info, fill=(0, 0, 0), font=font)
    path = "/auto_report/png/" + image_name
    im_new.save(path, "PNG")
    del draw