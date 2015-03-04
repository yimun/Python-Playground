import sys
import os

lspath = "E:/@Python/Python-Playground/05.cmd ls/ls.py"

if __name__ == '__main__':
    strarg = ' '.join(sys.argv[1:])
    command = 'python "{0}" {1}'.format(lspath,strarg)
    # print command
    os.system(command)