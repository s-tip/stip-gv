#!/usr/bin/env python

import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctim.settings')

    #ubuntuでは/usr/local/libの方のdyangoライブラリを用いると
    #エラーが発生するため、優先順位を下げる
    if os.name != 'nt':
        sys.path.remove('/usr/local/lib/python2.7/dist-packages')
        sys.path.append('/usr/local/lib/python2.7/dist-packages')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
