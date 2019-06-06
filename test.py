# -*- coding: utf-8 -*-

import os
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:')  # 当前路径下所有子目录
        for sd in dirs:
            print('|- '+sd)
        print('files:')  # 当前路径下所有非目录子文件
        for f in files:
            print('|- '+f)



if __name__ == '__main__':
    file_name(r'D:\Meiying\codes\industrial\factors')
