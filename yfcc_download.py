import urllib2
import os.path
import subprocess

def split_str(s, n):
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

def img_download(url, filename):
    img = urllib2.urlopen(url)
    fout = open(filename, 'wb')
    fout.write(img.read())
    img.close()
    fout.close()

fin = open('./yfcc100m_dataset.csv')
imgdir = './img'

print 'Start downloading YFCC100M dataset...'
for line in fin:
    line_split = line.strip().split('\t')
    line_num = int(line_split[0])
    photo_id = int(line_split[1])    # photo id
    photo_url = line_split[16]    # photo URL for downloading
    photo_ext = os.path.splitext(photo_url)[1]
    if photo_ext=='':
        photo_ext = '.mp4'
    split_photo_id = split_str(str(photo_id), 3)
    photo_dir = os.path.join(imgdir, split_photo_id[0], split_photo_id[1])
    photo_name = os.path.join(photo_dir, str(photo_id)+photo_ext)
    if os.path.isfile(photo_name) and os.path.getsize(photo_name):
        print 'Line %d, id %d, skipped' % (line_num, photo_id)
        continue    # avoid duplicate downloading
    print 'Line %d, id %d, download' % (line_num, photo_id)
    try:
        subprocess.call('mkdir -p ' + photo_dir, shell=True)
        img_download(photo_url, photo_name)
    except:
        print 'Failed'

