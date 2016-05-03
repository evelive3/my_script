#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problem Description:
小B最近对电子表格产生了浓厚的兴趣，她觉得电子表格很神奇，功能远比她想象的强大。她正在研究的是单元格的坐标编号，
她发现表格单元一般是按列编号的，第1列为A,第2列为B，一次类推，第26列为Z。之后是两位字符编号的，第27列编号为AA,
第28列为AB，第52列为AZ。之后则是三位，四位，五位。。。规则类似。
表格单元所在的行则是按数值从1开始编号，表格单元名称是列+行编号组成，如单元格BB22则为54列第22行的单元格。
而编号系统有时也采用RxCy的规则，其中x和y为数值，表示单元格位于第x行第y列。如：R22C54。
设计算法实现两种表示之间的转换。通过输入 R22C54 或者 AB22，来得到相应的另一种表示。
"""

import re


def conversion(axes_string):
    # 先判断是否为excel_like模式
    is_excel_like = re.match(r'^([A-Za-z]+)(\d+)$', axes_string)
    if is_excel_like is not None:
        excel_like = is_excel_like.groups()
        col_name = excel_like[0].upper()
        row_number = excel_like[1]
        # 将col_name反序，逐位减去与大写字母A的asc码距离值，得到其26进制数字值，再进行26进制转10进制计算
        col_number = sum([(26**n) * (ord(x)-64) for n, x in enumerate(col_name[::-1])])
        return 'R{0}C{1}'.format(row_number, col_number)
    # 再判断是否为RxCy模式
    is_rxcy = re.match(r'^[R,r](\d+)[C,c](\d+)$', axes_string)
    if is_rxcy is not None:
        rxcy = is_rxcy.groups()
        col_number = rxcy[1]
        row_number = rxcy[0]

        # 制作一个同时计算出商与余的函数
        f = lambda x, n: (x // n, x % n)

        # 10进制转n(n>2)进制生成器
        def dec_to_n(dec, n_bit):
            while dec > n_bit:
                dec, remainder = f(dec, n_bit)
                yield remainder
            if dec <= n_bit:
                yield dec

        # 将Remainder列表反序，逐位转换为相应字母
        col_name = ''.join([chr(x + 64) for x in list(dec_to_n(int(col_number), 26))[::-1]])
        return '{0}{1}'.format(col_name, row_number)
    # 都不是，报错退出
    raise ValueError('输入值不符合预期')

if __name__ == '__main__':
    s = input('Please input a string, Like "CC13" or "R12C7": ')
    print('convert {0} to {1}'.format(s.upper(), conversion(s)))
