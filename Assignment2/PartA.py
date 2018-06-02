# -*- coding: utf-8 -*-
import pandas as pd
from pandas import ExcelWriter
import math
from captions_cluster import cluster_wordcloud
from data_reprocessing import conv_dic,transform_doc2wordlist,create_termset # load the data preprocessing modules

#-----------------------calculate the term frequency----------------------------------------------
def transform_doc2tf_dic(doc2wordlist):
	doc2tf_dic = {}
	for (doc_name,wordlist) in doc2wordlist.items():
		tf_dic = {}
		num_word = len(wordlist)
		for w in wordlist:
			if w in tf_dic:
				tf_dic[w] +=1
			else:
				tf_dic[w] = 1
			tf_dic[w] = tf_dic[w]/float(num_word)
		doc2tf_dic[doc_name] = tf_dic
	return doc2tf_dic

def term_frequency(doc2tf_dic,term_list):
	doc_name_list = []
	for doc_name in doc2tf_dic:
		doc_name_list.append(doc_name)
	tf_dataframe = pd.DataFrame(columns = doc_name_list, index = term_list) 
	for (doc_name, tf_dic) in doc2tf_dic.items():
#In order to imporve the execution efficiency, the program does not calculate the term frequence that the term doesn't appear the document!
#So the excel file has many empty cell,the empty cell means that the value of term frequency is zero
		for w in tf_dic:
			tf_dataframe.loc[w,doc_name] = tf_dic[w]
			print('doc_name:'+str(doc_name)+',' + w +',tf_value: %s' % tf_dic[w])
	return tf_dataframe

def output_tf(tf_dataframe):
	writer = ExcelWriter('tf_result.xlsx')
	tf_dataframe.to_excel(writer, 'tf')
	writer.save()
	print("tf_file Output Success")
#-------------------------calculate the inverse document frequency-----------------------------------------------------

def inv_doc_freq(term_set,doc_name2word_list):
    doc_num = len(doc_name2word_list)
    idf_dict = {}
    for w in term_set:
        doc_count = 0
        #find the appear frenquency among all documents
        for word_list in doc_name2word_list.values():
            if w in word_list:
                doc_count += 1
        idf_dict[w] = math.log(float(doc_num)/float(doc_count))
    return idf_dict

def idf_dataframe(idf_dict):
	columns_name = ['idf_value',]
	idf_dataframe = pd.DataFrame(columns = columns_name, index = idf_dict.keys())
	for w in idf_dict:
		idf_dataframe.loc[w,columns_name[0]] = idf_dict[w]
		print('word: %s' %w +',idf_value:%s' %idf_dict[w])
	return idf_dataframe

def output_idf(idf_dataframe):
	writer = ExcelWriter('idf_result.xlsx')
	idf_dataframe.to_excel(writer, 'idf')
	writer.save()
	print("idf_file Output Success")

#------------------------------- --------------tf_and_idf----------------------------------------------------------
def tf_and_idf():
    #public
	doc2text = conv_dic()
	doc2wordlist = transform_doc2wordlist(doc2text)
	term_set = create_termset(doc2wordlist)
    
    #idf
	idf_dict = inv_doc_freq(term_set,doc2wordlist)
	idf_data_frame = idf_dataframe(idf_dict)
	output_idf(idf_data_frame)    
    
    #tf
	doc2tf_dic = transform_doc2tf_dic(doc2wordlist)	
	tf_dataframe = term_frequency(doc2tf_dic,term_set)
	output_tf(tf_dataframe)
    
if __name__ == '__main__':
  tf_and_idf()
  cluster_wordcloud()
    
    

