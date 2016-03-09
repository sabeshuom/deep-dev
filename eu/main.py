#!/usr/bin/python
import csv
import json
import get_data as gd
import os

host = 'http://h17.ceeqapp.com:9250'
es_type = 'trademark'
es_index = 'EU'
prefix = 'tmv'

home_dir = '/Volumes/DL'
tmkeys_json = home_dir + '/tmv/logomatch/www/js/tmKeys_' + es_index + '.json'

files = {'train': prefix + '_' + es_index + '_' + 'train.json', \
         'validation': prefix + '_' + es_index + '_' + 'validation.json',\
         'test': prefix + '_' + es_index + '_' + 'test.json',\
         'map_key': prefix + '_'+ es_index + '_' + 'map_key.json'}
key_start = 1
key_size = 500000
train_r  = 0.6
test_r = 0.2
minNoOfImagesPerKey = 1000

tmkeys = gd.get_tmkeys(tmkeys_json)
data = gd.get_keyword(host, es_type, es_index, key_start, key_size)

map_key = []
train = {}
test = {}
validation = {}

for k in sorted(data, key=lambda k: len(data[k]), reverse=True):
    ids  = data[k]
    print k + ':' + str(len(ids)) 
    
    if len(ids) < minNoOfImagesPerKey :
        break
    
    train_lastidx = int((len(ids)*train_r))
    test_lastidx = train_lastidx + int((len(ids)*test_r))
    train_ids = ids[0:train_lastidx]
    test_ids = ids[train_lastidx: test_lastidx]
    validation_ids = ids[test_lastidx:]
    d = {}
    d['label'] = len(map_key)
    d['key'] = k
    d['n_tain'] = len(train_ids)
    d['n_test'] = len(test_ids)
    d['n_validation'] = len(validation_ids)
    map_key.append(d)
    
    for _id in train_ids:
        #print _id
        if _id in train:
            train[_id].append(d['label'])
        else:
            train[_id] = [d['label']]

    for _id in test_ids:
        #print _id
        if _id in test:
            test[_id].append(d['label'])
        else:
            test[_id] = [d['label']]

    for _id in validation_ids:
        #print _id
        if _id in validation:
            validation[_id].append(d['label'])
        else:
            validation[_id] = [d['label']]

with open(files['train'], "w") as fp:
    json.dump(train, fp, indent=4, sort_keys=True)

print "train json saved"
print "train path : " + os.path.abspath(files['train'])

with open(files['test'], "w") as fp:
    json.dump(test, fp, indent=4, sort_keys=True)

print "test json saved"
     
with open(files['validation'], "w") as fp:
    json.dump(validation, fp, indent=4, sort_keys=True)

print "validation json saved"

with open(files['map_key'], 'w') as fp:  
    json.dump(map_key, fp, indent=4, sort_keys=True)
print "map key saved"




