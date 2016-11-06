#!F:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'mrq==0.1.12','console_scripts','mrq-worker'
__requires__ = 'mrq==0.1.12'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mrq==0.1.12', 'console_scripts', 'mrq-worker')()
    )
