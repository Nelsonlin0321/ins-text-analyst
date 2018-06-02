# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 19:29:45 2018

@author: DELL
"""
import json
import re
from nltk.corpus import stopwords
list_stopWords=list(set(stopwords.words('english')))
def conv_dic(location='assignment2.json') : # read the json file
    with open(location, 'r', encoding = 'utf-8') as f:    
        doc2text = {}
        doc_id = 0
        f_json = json.load(f)
        for item in f_json:
            text = item["edge_media_to_caption"]["edges"][0]["node"]["text"]
            doc2text[doc_id] = text
            doc_id +=1
    return doc2text
  
def transform_doc2wordlist(doc2text):
    doc2wordlist = {}
    for doc_name in doc2text: #获取每个doc_name
        content = doc2text[doc_name] #获取每一个tex
        content = content.strip()	
        content = re.sub('[^A-Za-z\s]', '' ,content) 	
        content = content.lower()
        content = content.replace('\n',' ')
        word_list = re.split('\ +', content)
        word_list = [w for w in word_list if not w in list_stopWords]
        doc2wordlist[doc_name] = word_list
    return doc2wordlist

def create_termset(doc2wordlist):
	term_set = set()
	for wordlist in doc2wordlist.values():
		term_set = term_set|set(wordlist)
	return term_set
