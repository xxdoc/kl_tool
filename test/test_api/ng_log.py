#-------------------------------------------------------------------------------
# Name:        Ä£¿é1
# Purpose:
#
# Author:      kongl
#
# Created:     28/12/2017
# Copyright:   (c) kongl 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import pykl

def main_move():
    pwd = os.getcwd()
    file_map = pykl.pyfile.get_dict_of_dir(pwd, lambda f: f[-4:]=='.log')
    for ff, _ in file_map.items():
        nn = ff.replace(pwd + '\\', '').split('\\')[0] + '.log'
        nf = os.path.join(pwd, nn)
        if ff != nf:
            os.rename(ff, nf)
    pass

def main():
    pwd = os.getcwd()
    file_map = pykl.pyfile.get_dict_of_dir(pwd, lambda f: f[-4:]=='.log' and f.find('error_')>0)
    line_list = []
    for ff, _ in file_map.items():
        with open(ff, 'r') as rf:
            line_list.extend(rf.readlines())

    out_file = "all_error.log"
    with open(os.path.join(pwd, out_file), 'w') as wf:
        wf.writelines(line_list)
    pass

if __name__ == '__main__':
    main()
