# -*- coding: utf-8 -*-
import win32com.client

CUR_CODE_1 = '348dcfdf'
CUR_CODE_2 = '46e77ef0'

FISH_KEY = '1'
BUFF_KEY = '2'




dm = win32com.client.Dispatch('dmsoft')
print dm.ver()

def main():
    pass

if __name__ == '__main__':
    main()
