# -*- coding= utf-8 -*-
"""
Created on Sun Mar 12 11=34=18 2017

@author= anbarasan.selvarasu
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

    # Hyperparameters for the Vectorizer
    NUM_TOPICS = 20
    NUM_BELOW = 5
    NUM_ABOVE = 0.05
    NUM_FEATURES = 10000
    NUM_WORDS = 30

    # Zeroth index is min no. of grams and first index is max no. of grams
    N_GRAMS = (1, 2)

    # Types of words to get (NN: noun) etc
    POS_TAGS = ["NN", "NNS"]

    # Input CSV location
    INPUT_FILE = "data/yelp.csv"

    # Output CSV location
    OUTPUT_FILE = INPUT_FILE[INPUT_FILE.find("/") + 1:INPUT_FILE.find(".")] + "_processed.csv"

    # Base64 encoded image txt
    ENCODED_IMAGE_FILE = "fifa-world-cup.txt"

    # wordcloud location
    WORDCLOUD_IMAGE_FILE = "building_PNG9.png"
