# -*- coding: utf-8 -*-
import re
import json
from nltk.corpus import stopwords
import pandas as pd
from pandas import ExcelWriter
list_stopWords=list(set(stopwords.words('english')))

#create the document_name:text dictionary data
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

#doc2tf_dic = transform_doc2tf_dic()
def create_termset(doc2wordlist):
	term_set = set()
	for wordlist in doc2wordlist.values():
		term_set = term_set|set(wordlist)
	return term_set

#term_set = create_termset()


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
			print('doc_name:'+str(doc_name)+', w:' + w +',value: %s' % tf_dic[w])
	return tf_dataframe


def output(tf_dataframe):
	writer = ExcelWriter('tf_result.xlsx')
	tf_dataframe.to_excel(writer, 'tf')
	writer.save()
	print("File Output Success")

def main():
	doc2text = conv_dic()
	doc2wordlist = transform_doc2wordlist(doc2text)
	doc2tf_dic = transform_doc2tf_dic(doc2wordlist)
	term_set = create_termset(doc2wordlist)
	tf_dataframe = term_frequency(doc2tf_dic,term_set)
	output(tf_dataframe)



if __name__ == '__main__':
	main()

