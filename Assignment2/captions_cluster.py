# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:02:36 2018

@author: DELL
"""
from os import path
from data_reprocessing import conv_dic,transform_doc2wordlist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics

def cluster_wordcloud():
  doc2text = conv_dic()
  doc2word_list = transform_doc2wordlist(doc2text)
  
  def transform2text_list(doc2word_list):
      text_list = []
      for word_list in doc2word_list.values():
          sentence = ' '.join(word_list)
          text_list.append(sentence)
      return text_list
  
  text_list = transform2text_list(doc2word_list)
  print('testing:', end = '')
  print(text_list[:2])
  
  vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')
  X = vectorizer.fit_transform(text_list)
  k=40
  km = KMeans(n_clusters=k, max_iter=200)
  km.fit_transform(X)
  print('Silhouette Coefficient: %0.5f\n' %metrics.silhouette_score(X, km.labels_, metric='euclidean') )
  
  print('The geneation of wordclouds')
  from wordcloud import WordCloud
  import matplotlib.pyplot as plt
  d = path.dirname(__file__)
  image = 'images/'
  output_location = path.join(d,image) 
  order_centroids = km.cluster_centers_.argsort()[:, ::-1] #获取 {cluter：[feature_id]}
  terms = vectorizer.get_feature_names()# feature {feature_name: feature_id}
  for i in range(k):#retrive the cluster_id
      print('Cluster %d:' % i)
      text = ""   
      for term_id in order_centroids[i,:30]:# in order to imporve the computing efficency , we just use top 30 terms as a group
        #obtain all feature_id in a cluster
        #print(terms[word_id],end = '')
        text  = text + terms[term_id] + ' '
        
      wordcloud = WordCloud().generate(text)
      
      wordcloud.to_file(path.join(output_location, 'cluster_%s.jpg' %i))
      plt.imshow(wordcloud, interpolation = 'bilinear')
      plt.axis("off")
      plt.show()

if __name__ == '__main__':
  cluster_wordcloud()
  
    



