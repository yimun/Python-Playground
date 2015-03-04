#!/usr/bin/env python
# coding:utf8
import argparse
import os
import time
import math
import re
import sys
from color import *


total_items = 0

def initMenu():
    '''
    添加命令行参数并且返回当前的参数字典

    Returns:
        命令行参数所构成的字典
    '''
    parser = argparse.ArgumentParser(description='Implement [ls] command with python!')
    parser.add_argument("-a", "--all", action = 'store_true',
        help = "do not ignore entries starting with . [default:off]")
    parser.add_argument("-H", "--hidden", action = 'store_true',
        help = "show hidden files [default:off]")
    parser.add_argument("-m", "--modified", action = 'store_true',
        help = "show last modified date/time [default:off]")
    parser.add_argument("-o","--order", default = 'name',
        help = "order by ('name','n';'modified','m';'size','s';'type','t') [default: name]")
    parser.add_argument("-r","--recursive",action = 'store_true',
        help = "recurse into subdirectories [default:off]")
    parser.add_argument("-s","--sizes",action = 'store_true',
        help = "show sizes [default:off]")
    # nargs 是参数个数  metavar是变量在usage中的显示别名
    parser.add_argument('path', metavar='PATH', type=str, nargs='*', 
        help = 'one or more path to show') 
    return vars(parser.parse_args())

def getDirectory(path,all,hidden,modified,order,recursive,sizes):
    '''
    获取并打印目录
    '''
    if not path:
        path.append('.') # 默认是当前目录
    for item in path:
        if len(path) > 1:
            print item
        try:
            str_dirs = os.listdir(item)
        except:
            sys.exit("ERR: wrong path '{}'".format(item))
        dirs = [getFullInfo(os.path.join(item,str_dir)) for str_dir in str_dirs if all or not all and not str_dir.startswith('.')]
        mSort(dirs,order)
        for dir in dirs:
            form = ''
            if not modified:
                form = '{0}  '
            if not sizes:
                form += '{1:>15}    '
            form += '{2:.60}'
            form = form.format(dir['mtime'],intcomma(dir['size']),os.path.basename(dir['path']))
            global total_items;
            total_items += 1
            if dir['isdir']:
                printColor(form,FOREGROUND_BLUE | FOREGROUND_INTENSITY)
                if recursive:
                    getDirectory([dir['path']],all,hidden,modified,order,recursive,sizes)

            elif dir['isexe']:
                printColor(form,FOREGROUND_GREEN | FOREGROUND_INTENSITY)
            else:
                print form
                    


def getFullInfo(path):
    '''
    获取目录条目的详细信息，如大小、修改时间等

    Returns:
        每一条目录信息所构成的字典
        {'path':..., 
         'mtime':...,
         'size':...,
         'isdir':...,
         'isexe':...}
    '''
    mtime = os.path.getatime(path)
    mtime = time.strftime('%Y-%m-%d   %H:%M:%S',time.gmtime(mtime))
    size = os.path.getsize(path)
    return {'path':path,'mtime':mtime,'size':size,
        'isdir':os.path.isdir(path),'isexe':path.endswith(('.exe','.py','.bat'))}

def mSort(dirs,order):
    '''
    对目录进行排序
    
    Args:
        dirs: 目录列表
        order: 制定的排序方式
    '''
    if order == 'size' or order == 's':
        dirs.sort(key = lambda dir : dir['size'],reverse = True)
    if order == 'type' or order == 't':
        dirs.sort(key = lambda dir : dir['isexe'],reverse = True)
        dirs.sort(key = lambda dir : dir['isdir'],reverse = True)   
    if order == 'modified' or order == 'm':
        dirs.sort(key = lambda dir : dir['mtime'],reverse = True)

def intcomma(value):
    '''
    给整形数每三位添加标点

    Args:
        value:输入数字
        
    Returns：
        格式化后的字符串
    '''
    orig = str(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new)


if __name__ == '__main__':
    args = initMenu()
    # print args
    getDirectory(**args)  # *arg 将其扩展成元组，**arg将其扩展成字典

    print '\tTotal {} items'.format(intcomma(total_items))




