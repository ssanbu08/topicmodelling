# Topic Modelling
Topic Modelling using LDA to understand the subtopics in reviews

0. json_to_csv.py : converts json file from /data folder and saves it back as csv in the same folder.

1. loading_reviews.py : Loads the business,users and reviews file and process it by aplying various filters to reduce the size of reviews to handle
   2.1 Business are filtered for Restaurants that are open. Cities with more number of restaurants are identified and only Restaurants in those cities are taken for analysis.
   2.2 Reviews that have atleast one useful vote are considered

2. preprocessing.py : Does linguistic processing of review text like 
   3.1 stopword removal
   3.2 remove special characters
   3.3 pos tagging
   3.4 lemmatization
   3.5 filter for tokens that have only 'NN'&'NNS', i.e Noun singular and plural

   after preprocessing step each review is represented by a set of tokens ,that is a noun.

3. word2vec.py : uses gensim library to perform LDA on processed reviews and store the resulting model to local directory

4. nmf.py : Performs topic modelling using Non-Negative Matrix Factorization.

5. validation.py : Analyse the model results by listing the words per topic.

6. classifier.py : classifies any new review submitted through the LDA model trained by using Gensim.

7. cofigurations.py : Conatins all file related configurations .This file must be changed based on your data location.By Default it looks for files /data location form the current directory. 

7. Dockerfile : contains the instructions to create a docker image.

Steps to create a docker image:

Step 1: Download the github repository  to your local .

Step 2: create folders /data , /models inside the repository downloaded.

Step 3 : Open the command prompt and navigate to the repository 

Step 4 : Execute the following command to build an image locally
docker build -t topicmodel .

Step 5:  Execute the following command to create a container from the image
docker run -t -i --name YelpBuild3 -v D:/Yelp/Code/Iteration_3/data:/src/data topicmodel /bin/bash

*Note :
   --name <name_of_container>
    -v <src_dirc : dest_dir_in_container>
    Image name : topicmodel
    In mapping volumes ,the  source directory should contain all json files.
 
Step 6: On successfully building your container ,navigate to the source folder.
cd src

Step 7: Once you are inside the src directory ,execute the following commands step by step.
python json_to_csv.py
python loading_reviews.py
python preprocessing.py
python word2vec.py
python nmf.py
python validation.py
python classifier.py


###Configurations

1) Edit the variables in the `configurations.py` 
2) Run `python3 frequent_queries.py`

###Risks

1) Line 86: there might be encoding error for the `'` in the csv files so might need to try diff encoding.
