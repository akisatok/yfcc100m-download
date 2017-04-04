import os.path
import subprocess

def split_str(s, n):
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

for line in open('imglist.txt'):
    basename, ext = os.path.splitext(line.strip())
    basename_split = split_str(basename, 3)
    old_path = os.path.join('img', basename + ext)
    new_dir  = os.path.join('img', basename_split[0], basename_split[1])
    new_path = os.path.join(new_dir, basename + ext)
    subprocess.call('mkdir -p ' + new_dir, shell=True)
    cmd = 'mv ' + old_path + ' ' + new_path
    subprocess.call(cmd, shell=True)
