# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 11:34:18 2017

@author: anbarasan.selvarasu
"""

class Configurations:
    def __init__(self):
        pass
    
    REVIEWS_JSON = "data/yelp_academic_dataset_review.json"
    USERS_JSON = "data/yelp_academic_dataset_user.json"
    BUSINESS_JSON = "data/yelp_academic_dataset_business.json"
    
    REVIEWS_FILE = "data/reviews.csv"
    USERS_FILE = "data/users.csv"
    BUSINESS_FILE = "data/business.csv"
    
    MASTER_FILE = "data/master.csv"
    PROCESSED_FILE = "data/processed.csv"
    
    LDA_MODEL_FILE = "models/"
    
    ID2WORD_FILE = "models/model_lda_15.lda.id2word"
    LOAD_LDA = "models/model_lda_15.lda"