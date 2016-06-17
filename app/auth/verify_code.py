#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/6/6'
__author__ = 'chuan.li'

import Image, ImageFilter, ImageFont, ImageDraw
import random
import base64

try:
    import cStringIO as StringIO
except:
    import StringIO


# 随机字母
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随即颜色2
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def generate_validate_code():
    # 240*60
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象
    font = ImageFont.truetype('app/static/font/arial.ttf', 36)
    # 创建Draw对象
    draw = ImageDraw.Draw(image)
    # 填充每个像素
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字
    strs = ''
    for t in range(4):
        str = rndChar()
        strs += str
        draw.text((60 * t + 10, 10), str, font=font, fill=rndColor2())
    # 模糊
    image = image.filter(ImageFilter.BLUR)
    # img_io = StringIO.StringIO()
    # image.save(img_io, 'jpeg')
    # img_io.seek(0)
    # img_base64 = base64.b64encode(img_io.read())
    return image, strs
