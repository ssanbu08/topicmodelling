# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 20:36:03 2017

@author: anbarasan.selvarasu
"""
from time import time
import re
import logging


import pandas as pd


from configurations import Configurations

def process_user():
    print("Process User")
    ## any user processing logic goes here
    
def process_business(business,isopen=True,top_cities=15):
     print("Processing Business....")
     
     business_filtered = business[ [isinstance(i,str) for i in business['categories']] ]
     business_filtered['categories_2'] = [re.sub(r'[\[\]\']','',category) for category in business_filtered['categories']]
     business_filtered['categories_3'] = [i.split(",") for i in business_filtered['categories_2']]
     business_restaurant = business_filtered[['Restaurants' in i for i in business_filtered['categories_3']] ]
     
     ## Add isopen()
     business_restaurant_open = business_restaurant[business_restaurant['is_open']==1]
     
     ## Get business of top n cities     
     Region=business_restaurant_open["city"]
     vc = Region.value_counts()[:top_cities]
     cities = vc.index.tolist()
     business_restaurant_open_top20 = business_restaurant_open[business_restaurant_open['city'].isin(cities)]     
     return business_restaurant_open_top20
     
          
def process_reviews(reviews, filtered_business,usefulness=1 ):
    print("Processing Reviews....")
    #Filter for selected business    
    reviews_restaurant = reviews[reviews['business_id'].isin(filtered_business)] 
    # Filter for reviews that has atleast 1 useful vote
    reviews_restaurant_up = reviews_restaurant[reviews_restaurant['useful'] >usefulness] 
    return reviews_restaurant_up
     
     # filter short reviews
     
def prepare_master_file(users,business,reviews):
     print("Preparing Master file....")
     ###### Create master file ########
     rev_bus = pd.merge(reviews, business, on='business_id', how='left')
     rev_bus_user = pd.merge(rev_bus, users, on='user_id', how='left')
     return rev_bus_user   
 
     

    
def main():
    #print("hello world") 
       logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
       
       t0 = time()
       print("Loading Users....")
       users = pd.read_csv(Configurations.USERS_FILE)
       print("done in %0.3fs." % (time() - t0))
       print("No of users :",users.shape[0])
          
       t0 = time()
       print("Loading Business....")
       business = pd.read_csv(Configurations.BUSINESS_FILE,chunksize = 20000)
       business_df = []
       chunk_no=1
       for df in business:
           
          # process each data frame
           #if chunk_no<3:
               return_df =  process_business(df)
               business_df.append(return_df)
               #business_df = pd.concat([business_df,return_df],ignore_index=True)
               print ("rows in chunk %d" % (df.shape[0]))
               print ("rows processed %d" % (return_df.shape[0]))
               return_df.head
               print("processed chunk %d  in %0.3fs." % (chunk_no, (time() - t0))) 
               chunk_no+=1
           #else:
               #break
           
       business_df_2 = pd.concat(business_df,ignore_index = True)
       print ("No of rows processed Business %d" % (business_df_2.shape[0]))
       restnt_buss_ids = business_df_2['business_id'].unique()
       
      

 
      
       t0 = time()
       print("Loading reviews....")
       reviews = pd.read_csv(Configurations.REVIEWS_FILE,chunksize = 20000)
       reviews_df = []
       chunk_no=1
       for df in reviews:
           # process each data frame
           #if chunk_no<3:
               return_df =  process_reviews(df,restnt_buss_ids) 
               reviews_df.append(return_df)
               print ("There are %d rows of data" % (return_df.shape[0]))
               print("processed chunk %d  in %0.3fs." % (chunk_no, (time() - t0))) 
               chunk_no+=1
           #else:
              # break
       reviews_df_2 = pd.concat(reviews_df,ignore_index = True)
       print ("No of rows processed Reviews %d" % (reviews_df_2.shape[0]))
       
       master_df = prepare_master_file(users,business_df_2,reviews_df_2)
       master_df.to_csv(Configurations.MASTER_FILE)
       print ("No of rows in Master %d" % (reviews_df_2.shape[0]))
   
#           
#       t0 = time()
#       prepare_master_file()
#==============================================================================
 

    
    
    
if __name__ == "__main__":
    main()

    
    

