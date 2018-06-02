# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 11:55:34 2018

@author: DELL
"""

from term_frequency import conv_dic,transform_doc2wordlist,create_termset
import pandas as pd
import math
from pandas import ExcelWriter



def inv_doc_freq(term_set,doc_name2word_list):
    doc_num = len(doc_name2word_list)
    idf_dict = {}
    #term in all doc
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
	



def output(idf_dataframe):
	writer = ExcelWriter('idf_result.xlsx')
	idf_dataframe.to_excel(writer, 'idf')
	writer.save()
	print("idf_file Output Success")

def main():
	doc2text = conv_dic()
	doc2wordlist = transform_doc2wordlist(doc2text)
	term_set = create_termset(doc2wordlist)
	idf_dict = inv_doc_freq(term_set,doc2wordlist)
	idf_data_frame = create_dataframe(idf_dict)
	output(idf_data_frame)

if __name__=='__main__':
	main()



