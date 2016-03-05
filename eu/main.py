#!/usr/bin/python
import csv
import json
import get_data as gd

root = 'tmv'
src_dir = '/home/sabesan/deep-tmv'
tmv_dir = src_dir + '/tmv'
host = 'http://h17.ceeqapp.com:9250'
es_type = 'trademark'
es_index = 'EU'
tmkeys_json = tmv_dir + '/logomatch/www/js/tmKeys_' + es_index + '.json'
files = {'train': root + '_' + es_index + '_' + 'train.json', \
         'validation': root + '_' + es_index + '_' + 'validation.json',\
         'test': root + '_' + es_index + '_' + 'test.json'}
key_start = 1
key_size = 10
no_of_classes = 100
train_r  = 1.0
test_r = 0.2
# get the keywords for each image 
#data = get_keywords(host, es_index, es_type, es_from, es_size)

#save them as json file
#save_keyidpair_as_json(data)

#save json file as csv file

#get the keyword pair with discritpions to count how many keyword pair
tmkeys = gd.get_tmkeys(tmkeys_json)
data = gd.get_keyword(host, es_type, es_index, key_start, key_size)

map_key = {}
train = {}

a = [{'id':34343} ,{'id':343434}]
print a['id']

for k in sorted(data, key=lambda k: len(data[k]), reverse=True):
    ids  = data[k]
    train_ids = ids[0:int((len(ids)*train_r))]
    
    #test_ids = ids((int((len(ids)*train_r)) +1):int((len(ids)* test_r)))
    #validation_ids = ids(1:int((len(ids)*test_r)))
    map_key[k] = len(map_key)
  
    for id in train_ids:
        if 'id' in train:
            if id in train['id']:
                temp = train['id']
                #print temp
                #print "\n"
                #print temp.index(id)
                #print temp(temp.index(id))
                #train[temp.index(id)]['key'].append(map_key[k])
            else:
                train['id'] = id
                train['key'] = map_key[k]
        else:
            train['id'] = id
            train['key'] = map_key[k]

#print train


#for key in data:
#    print key
#    print data[key]



#for key in len(data)
#    data[key]['keyw']
#    code[key].append()

#with open('test.json', "w") as fp:
#    json.dump(data, fp, indent=4)
#ids = gd.get_idsForkey(tmkeys[0])

#for key in range(len(tmkeys))
#trainin_data = gd.ids_forkeyword()



