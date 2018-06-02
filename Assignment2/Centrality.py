# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:17:34 2018

@author: DELL
"""


import numpy as np
from math import sqrt



def Eigenvector_Centrality(ajacency_metrics):
  initial_vector = np.ones(len(ajacency_metrics))
  #创建初始向量
  def normalisation(multi_result):
    total=0
    for num in multi_result:
      total = total +num*num
    if total == 0:
      vector = np.array([0,0,0])
      return vector
    else:
      vector = multi_result/sqrt(total)   
    return vector
         
  def computation(vector):
    #print('-'*20+'iteration'+ '-'*20)
    #print("before_vector:%s" %vector)
    vector_result = np.dot(ajacency_metrics,vector)
    vector_result=normalisation(vector_result)
    #print("After_vector_result:%s" %vector_result)
    if (vector_result==vector).all():
      #print('convergence')
      print('Eigenvector_Centrality:',end = '')
      print(vector_result)
      return(vector_result)
    else:
      computation(vector_result)
      
  computation(initial_vector)


    

def Katz_Centrality(ajacency_metrics,alpha,beta):
  initial_vector = np.ones(len(ajacency_metrics))
  beta_vetor = initial_vector*beta
  #print(beta_vetor)       
  def computation(vector):   
    #print('-'*20+'iteration'+ '-'*20)
    #print("before_vector:%s" %vector)
    multi_result = np.dot(ajacency_metrics,vector)
    multi_result = multi_result *alpha
    vector_result = multi_result +beta_vetor 
    #print("After_vector_result:%s" %vector_result)
    if (vector_result==vector).all():
      #print('convergence')
      print('Katz_Centrality:',end = '')
      print(vector_result)
      return(vector_result)
    else:    
      computation(vector_result)
      
  computation(initial_vector)
  

#WI
def PageRank_Centrality(PageRank_metrics,alpha,beta):
  all_one_vector = np.ones(len(PageRank_metrics))
  initial_vector = all_one_vector/len(PageRank_metrics) #1/3
  beta_vetor = all_one_vector*beta
  ###
  def computation(vector):
    #print('vector:%s' %vector)
    #print('-'*20+'iteration'+ '-'*20)
    #print("before_vector:%s" %vector)
    multi_result = np.dot(PageRank_metrics,vector)
    multi_result = multi_result *alpha
    vector_result = multi_result +beta_vetor
      
    vector1 = np.around(vector,decimals = 10)
    vector2 = np.around(vector_result,decimals = 10)
    #print((vector1==vector2).all())
    #print("After_vector_result:%s" %vector2)
    if (vector1==vector2).all():
      #print('convergence')
      print('PageRank_Centrality:',end = '')
      print(vector2)
      return(vector2)
    else:    
      computation(vector_result)
      
  computation(initial_vector)

'''
#big Data
def Finite_PageRank_Centrality(PageRank_metrics,alpha,beta):
  initial_vector = np.ones(len(PageRank_metrics))/len(PageRank_metrics)
  beta_vetor = initial_vector*beta #加一个En(u)*B
  
  print(beta_vetor)
  def computation(vector):
    
    print('-'*20+'iteration'+ '-'*20)
    print("before_vector:%s" %vector)
    multi_result = np.dot(PageRank_metrics,vector)
    multi_result = multi_result *alpha
    vector_result = multi_result +beta_vetor
    vector1 = np.around(vector_result,decimals = 10)
    vector2 = np.around(vector,decimals = 10)
    print("After_vector_result:%s" %vector_result)
    print((vector1==vector2).all())
    print("After_vector_result:%s" %vector_result)
    
    if (vector1==vector2).all():
      #print('convergence')
      print('PageRank_Centrality:',end = '')
      print(np.around(vector_result,decimals = 5))
      return(np.around(vector_result,decimals = 5))
    else:     
      computation(vector_result)
    
  computation(initial_vector)
'''
ajacency_metrics = np.array([[0,0,0],[1,0,1],[1,1,0]])
PageRank_metrics_homework = np.array([[0,0.5,0.5],[0,0,0.5],[0,0.5,0]])

#
remove_metrics = np.array([[0,0,0],[1,0,0],[1,1,0]])
remove_PageRank = np.array([[0,1,0.5],[0,0,0.5],[0,0,0]])

if __name__== '__main__':
  print('3):')
  print('  a:',end = '')
  Eigenvector_Centrality(ajacency_metrics)
  print('  b:alpha = 0.1, beta = 0.1  ', end = '')
  Katz_Centrality(ajacency_metrics,0.1,0.1)
  print('  c:alpha = 0.1, beta = 0.1  ', end = '')
  PageRank_Centrality(PageRank_metrics_homework,0.1,0.1)
  
  print('='*100)
  print('4): alpha = 0.1, beta = 0')
  Eigenvector_Centrality(ajacency_metrics)
  Katz_Centrality(ajacency_metrics,0.1,0)
  PageRank_Centrality(PageRank_metrics_homework,0.1,0)
  
  print('='*100)
  print('5): remove the link from Node2 to Node3')
  Eigenvector_Centrality(remove_metrics)
  Katz_Centrality(remove_metrics,0.1,0.1)
  PageRank_Centrality(remove_PageRank,0.1,0.1)
  

  