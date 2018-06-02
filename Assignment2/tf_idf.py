# -*- coding: utf-8 -*-
import re
import math
import pandas as pd
from pandas import ExcelWriter
import json
from nltk.corpus import stopwords

#read the json file and convert it to be the document_name:text dictionary data
def conv_dic(location='assignment2.json') : 
    with open(location, 'r', encoding = 'utf-8') as f:    
        doc2text = {}
        doc_id = 0
        f_json = json.load(f)
        for item in f_json:
            text = item["edge_media_to_caption"]["edges"][0]["node"]["text"]
            doc2text[doc_id] = text
            doc_id +=1
    return doc2text

doc2text = conv_dic()#call the read fuction


#------------------------------------------------------------
#calculate the term frequency
def term_freq(word_list): 
    word_dict = {} 
    for w in word_list:
        if w in word_dict:
            word_dict[w] += 1
        else:
            word_dict[w] = 1
            
    word_num = float(sum(word_dict.values()))
    for w in word_dict.keys():
        word_dict[w] /= word_num
    return word_dict

#calculate the inverse document frequency
def inv_doc_freq(term_set, doc_name2word_list):
    doc_num = len(doc_name2word_list)
    idf_dict = {} 
    
    for w in term_set: 
        doc_count = 0
        
        for word_list in doc_name2word_list.values(): 
            if w in word_list:
                doc_count += 1
        idf_dict[w] = math.log(float(doc_num)/float(doc_count))
    return idf_dict

    
if __name__ == '__main__':
   doc_name2word_list = {}
   doc_name2tf_dict = {}
   term_set = set()
   
   list_stopWords=list(set(stopwords.words('english')))
   doc_name_list = []
   for doc_name in doc2text:
       print('doc_name:%s' %doc_name) 
       doc_name_list.append(doc_name)
       content = ''
       for line in doc2text[doc_name]:
           content += line 
       content = content.strip()
       content = re.sub('[^A-Za-z\s]', '' ,content)
       content = content.lower()
       content = content.replace('\n',' ')
       word_list = re.split('\ +', content) 
       word_list = [w for w in word_list if not w in list_stopWords]
       print('cotent:%s' %word_list)
       doc_name2word_list[doc_name] = word_list 
       doc_name2tf_dict[doc_name] = term_freq(word_list) 
       term_set = term_set | set(word_list) 
           
           
   idf_dict = inv_doc_freq(term_set, doc_name2word_list)
   term_list = list(term_set)
   print('term:%s' %term_list)
   tf_idf = pd.DataFrame(columns = doc_name_list, index = term_list)
   for doc_name in doc_name2word_list:
       print('='*100)
       print('doc_name:'+ str(doc_name))
       #in order to imporve the execution efficiency, the program does not calculate the tf_idf that the term doesn't appear the document!!!
       #So the excel file has many empty cell,which means that the value of term frequency is zero
       for w in doc_name2word_list[doc_name]:
           tf_idf.loc[w,doc_name] = doc_name2tf_dict[doc_name][w]*idf_dict[w]      
           w_tf_idf = tf_idf.loc[w,doc_name]
           print('doc_num' + ':' +str(doc_name)+'---------'+ w +':' + str(w_tf_idf))
   print('Writing done')
   
   #output
   writer = ExcelWriter('tfidf_result.xlsx')
   tf_idf.to_excel(writer, 'tfidf')
   writer.save()
   print("tfidf_file Output Success")
   