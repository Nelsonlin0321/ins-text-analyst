# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 12:06:44 2018

@author: DELL
"""
import numpy as np
from Centrality import Finite_PageRank_Centrality,Katz_Centrality,Eigenvector_Centrality,Infinite_PageRank_Centrality

'''
#tesing the Page_Rank
BigData_Modified_Metrics = np.array([[1/2,1/2,0],[1/2,0,0],[0,1/2,1]])
Finite_PageRank_Centrality(BigData_Modified_Metrics,0.8,0.2)
'''

'''
#tesing the page_pank
Work_example = np.array([[0,0.5,0,0,0,0,0],
                         [0,0,1/3,0,0,0,0],
                         [1/3,0,0,0,0,0,1],
                         [1/3,0,1/3,0,0,1/2,0],
                         [1/3,0,0,1,0,0,0],
                         [0,1/2,1/3,0,0,0,0],
                         [0,0,0,0,1,1/2,0]])

Finite_PageRank_Centrality(Work_example,1,0)
'''
#testing Eigenvector
example_metrics = np.array([[0,1,0],[1,0,1],[0,1,0]])

Eigenvector_Centrality(example_metrics)



