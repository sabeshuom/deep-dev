#!/usr/bin/python

import urllib2
import json
import csv
# =================================
# Query the resulting "table"

#url = endpoint + '/_search/?q=MarkFeature:Figurative&size=1000&fields=MarkImageDetails.MarkImage.MarkImageCategory.CategoryCodeDetails.CategoryCode'
es_fields = \
        {
            "phonetic_text_description": "WordMarkSpecification.MarkVerbalElementText.PHON_MarkVerbalElementText", # text in the image??
            #"phonetic_text_description": "PHON_MarkVerbalElementText", # text in the image??
            #note. this is the only place where the words in the image appear
            #"text_description": "WordMarkSpecification.MarkVerbalElementText",  # text in the image??
            "text_description": "WordMarkSpecification.MarkVerbalElementText.MarkVerbalElementText", # text in the image??

            # "image_description": "MarkDescriptionDetails.MarkDescription", #trouble (language) {languageCode, Description}
            "image_description": "",
            "mark_type": "MarkFeature",
            "mark_type_detail": "MarkFeature",

            # "keywords": "MarkRepresentation.MarkReproduction.MarkImageBag.MarkImage.NationalDesignClassificationBag.NationalDesignClassification.NationalDesignSearchCode",

            "keywords": "MarkImageDetails.MarkImage.MarkImageCategory.CategoryCodeDetails.CategoryCode",
            "vc_section": "MarkImageDetails.MarkImage.MarkImageCategory.CategoryCodeDetails.CategoryCode_section",
            "vc_division": "MarkImageDetails.MarkImage.MarkImageCategory.CategoryCodeDetails.CategoryCode_division",
            "vc_category": "MarkImageDetails.MarkImage.MarkImageCategory.CategoryCodeDetails.CategoryCode_category",
            "size": "size",
            "from": "from",
            "fields":"fields"
        }


def json_to_csv(json_file, csv_file,  header):
    with open(json_file) as data_file:    
        data = json.load(data_file)     
        data_items = data.items()
        print "json has %d of items on it " (len(data_items))
        f = csv.writer(open(csv_file, "wb+"))
        f.writerow(header);
        for i in range(len(p)):
            f.writerow(p[i])
            #To do it is for convert current json need to chanage for json with field of dictionary
    
    
def get_keyword(host, es_type, es_index, es_from, es_size):
    
    url = host + '/' + es_index  + '/' + es_type + '/_search/?q='
    es_query = es_fields['mark_type'] +':Figurative&' + \
               es_fields['size'] +'=' + str(es_size) + '&' +\
               es_fields['from'] +'=' + str(es_from)  + '&' +\
               es_fields['fields'] +'=' + es_fields['keywords']
    
    print url +es_query
    req = urllib2.Request(url + es_query)
    out = urllib2.urlopen(req)
    data = json.loads(out.read())
    key_data = hits_to_keyidpair(data)
    return key_data

    

def get_vc_discription(vc_names_path):
    vc_names = {};
    print "Loading " + vc_names_path
    with open(vc_names_path) as data_file:    
        temp = json.load(data_file)
        print str(len(temp)) +  " number of data found."
        
        for k in temp:
            try:
                k['code'] = str(k['code'])
            except:
                continue 
                   
            split = k['code'].split('.')
            for i in range(len(split)):
                if len(split[i]) == 1:
                    split[i] = '0' + split[i]
                    code = '.'.join(split).encode('utf-8','ignore')
                    vc_names[code] = k['name'].encode('utf-8','ignore')   
               #vc_names['code'] = k['code']     
    
    return vc_names

def get_tmkeys(json_file):
    # return a list of trademark keys in the region
    tmkeys = [];
    print "Loading " + json_file
    with open(json_file) as data_file:    
        temp = json.load(data_file)
        print str(len(temp)) +  " number of data found."
        
        for k in temp:
            try:
                k['code'] = str(k['code'])
            except:
                continue 
                   
            split = k['code'].split('.')
            for i in range(len(split)):
                if len(split[i]) == 1:
                    split[i] = '0' + split[i]
                    code = '.'.join(split).encode('utf-8','ignore')
                    tmkeys.append(code);
    return tmkeys         

def hits_to_keyidpair(data):
    hits = data['hits']['hits']
    num_hits = len(hits)
    hit_count = 0
    key_map = {}
    for hit in hits :
        id = hit['_id']
        keywords = ''
        d = {};
        try:  
            keywords = hit[es_fields['fields']][es_fields['keywords']]
        except:
            continue

        for keyword in keywords:
            if str(keyword) in key_map:
                key_map[str(keyword)].append(str(id))
            else:
                key_map[str(keyword)] = [str(id)]
        hit_count +=1

        if hit_count%1000 == 0:
            print "I have processed %d of %d IDS" % (hit_count, len(hits))
    
    #print key_map
    #if (file_name != None):
    #    with open(json_file, "w") as fp:
    #        json.dump(data, fp)
    # 
    return key_map  



