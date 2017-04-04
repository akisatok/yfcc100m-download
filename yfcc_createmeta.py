import json
import os.path
import subprocess

def split_str(s, n):
    length = len(s)
    return [ s[i:i+n] for i in range(0, length, n) ]

def extract_metadata(elems):
    if len(elems)<2: return None
    text = elems[1]
    text_split = text.split(',')
    d = dict()
    for elem in text_split:
        key = elem.split(':')[0]
        val = elem.split(':')[1]
        d[key] = val
    return d

def extract_metadata_d(elems):
    if len(elems)<25: return None
    d = dict()
    d['photo_hash'] = elems[2]
    d['user_id'] = elems[3]
    d['user_nickname'] = elems[4]
    d['date_taken'] = elems[5]
    d['date_uploaded'] = elems[6]
    d['capture_device'] = elems[7]
    d['title'] = elems[8]
    d['description'] = elems[9]
    d['user_tags'] = elems[10]
    d['machine_tags'] = elems[11]
    d['longitude'] = elems[12]
    d['latitude'] = elems[13]
    d['pos_accuracy'] = elems[14]
    d['url_show'] = elems[15]
    d['url_get'] = elems[16]
    d['license_name'] = elems[17]
    d['license_url'] = elems[18]
    d['server_id'] = elems[19]
    d['farm_id'] = elems[20]
    d['photo_secret'] = elems[21]
    d['photo_secret_orig'] = elems[22]
    d['photo_ext'] = elems[23]
    d['photo_or_video'] = elems[24]
    return d

fin_autotag = open('yfcc100m_autotags.csv')
fin_exif    = open('yfcc100m_exif.csv')
fin_places  = open('yfcc100m_places.csv')
fin_dataset = open('yfcc100m_dataset.csv')
metadir = './meta'

while True:
    # read lines
    line_a = fin_autotag.readline()
    line_e = fin_exif.readline()
    line_p = fin_places.readline()
    line_d = fin_dataset.readline()
    if (not line_a) or (not line_e) or (not line_p) or (not line_d):
        break
    line_a_split = line_a.strip().split('\t')
    line_e_split = line_e.strip().split('\t')
    line_p_split = line_p.strip().split('\t')
    line_d_split = line_d.strip().split('\t')
    # check photo ID
    photo_id_a = int(line_a_split[0])
    photo_id_e = int(line_e_split[0])
    photo_id_p = int(line_p_split[0])
    photo_id_d = int(line_d_split[1])
    if photo_id_a!=photo_id_e or photo_id_e!= photo_id_p or photo_id_p!=photo_id_d:
        print 'Photo ID mismatched.'
        continue
    photo_id = photo_id_a
    # check existing files
    split_photo_id = split_str(str(photo_id), 3)
    json_dir = os.path.join(metadir, split_photo_id[0], split_photo_id[1])
    json_path = os.path.join(json_dir, str(photo_id)+'_meta.json')
    if os.path.isfile(json_path) and os.path.getsize(json_path):
        print 'Photo ID %d metadata already exists, skip.' % photo_id
        continue
    print 'Photo ID %d metadata creating...' % photo_id
    subprocess.call('mkdir -p ' + json_dir, shell=True)
    # extract metadata
    autotags = extract_metadata(line_a_split)
    exif = extract_metadata(line_e_split)
    places = extract_metadata(line_p_split)
    othermeta = extract_metadata_d(line_d_split)
    # form JSON data and write it to a file
    json_data = dict()
    if autotags: json_data['autotags'] = autotags
    if exif: json_data['EXIF'] = exif
    if places: json_data['places'] = places
    if othermeta: json_data['othermeta'] = othermeta
#    print json_data
    with open(json_path, 'wb') as fout:
        json.dump(json_data, fout, sort_keys=True, indent=4)
