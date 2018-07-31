# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from configurations import Configurations
from time import time
import collections
import csv
import simplejson as json


def read_and_write_file(json_file_path, csv_file_path, column_names):
    """Read in the json dataset file and write it out to a csv file, given the column names."""
    with open(csv_file_path, 'w') as fout:
        csv_file = csv.writer(fout)
        csv_file.writerow(list(column_names))
        with open(json_file_path, encoding="utf8") as fin:
            for line in fin:
                line_contents = json.loads(line)
                csv_file.writerow(get_row(line_contents, column_names))

def get_superset_of_column_names_from_file(json_file_path):
    """Read in the json dataset file and return the superset of column names."""
    column_names = set()
    with open(json_file_path, encoding="utf8") as fin:
        for line in fin:
            line_contents = json.loads(line)
            column_names.update(
                    set(get_column_names(line_contents).keys())
                    )
    return column_names

def get_column_names(line_contents, parent_key=''):
    """Return a list of flattened key names given a dict.
    Example:
        line_contents = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        will return: ['a.b', 'a.c']
    These will be the column names for the eventual csv file.
    """
    column_names = []
    for k, v in line_contents.items():
        column_name = "{0}.{1}".format(parent_key, k) if parent_key else k
        if isinstance(v, collections.MutableMapping):
            column_names.extend(
                    get_column_names(v, column_name).items()
                    )
        else:
            column_names.append((column_name, v))
    return dict(column_names)

def get_nested_value(d, key):
    """Return a dictionary item given a dictionary `d` and a flattened key from `get_column_names`.
    
    Example:
        d = {
            'a': {
                'b': 2,
                'c': 3,
                },
        }
        key = 'a.b'
        will return: 2
    
    """
    if '.' not in key:
        if key not in d:
            return None
        return d[key]
    base_key, sub_key = key.split('.', 1)
    if base_key not in d:
        return None
    sub_dict = d[base_key]
    return get_nested_value(sub_dict, sub_key)

def get_row(line_contents, column_names):
    """Return a csv compatible row given column names and a dict."""
    row = []
    for column_name in column_names:
        line_value = get_nested_value(
                        line_contents,
                        column_name,
                        )
        if isinstance(line_value, str):
            row.append('{0}'.format(line_value.encode('utf-8')))
        elif line_value is not None:
            row.append('{0}'.format(line_value))
        else:
            row.append('')
    return row
    

def main():
    print("Conversion started")
    reviews_json = Configurations.REVIEWS_JSON
    users_json = Configurations.USERS_JSON
    business_json = Configurations.BUSINESS_JSON
    
    reviews_csv = Configurations.REVIEWS_FILE
    users_csv = Configurations.USERS_FILE
    business_csv = Configurations.BUSINESS_FILE
    
    print("Converting Business file.....")
    t0 = time()    
    column_names = get_superset_of_column_names_from_file(business_json)
    read_and_write_file(business_json, business_csv, column_names)  
    print("processed  in %0.3fs." % ((time() - t0)))
    
    print("Converting users file.....")
    t0 = time()    
    column_names = get_superset_of_column_names_from_file(users_json)
    read_and_write_file(users_json, users_csv, column_names)
    print("processed  in %0.3fs." % ((time() - t0)))
    
    print("Converting Reviews file.....")
    t0 = time()    
    column_names = get_superset_of_column_names_from_file(reviews_json)
    read_and_write_file(reviews_json, reviews_csv, column_names)
    print("processed  in %0.3fs." % ((time() - t0)))

      
     
     
     



    
if __name__ == '__main__':
    """Convert a yelp dataset file from json to csv."""

    main()
    
'''
## REVIEWS ###
json_file = "D:/Yelp/Data/yelp_academic_dataset_review.json"
csv_file = 'C:/Users/anbarasan.selvarasu/Documents/Yelp/reviews.csv'
column_names = get_superset_of_column_names_from_file()
read_and_write_file(json_file, csv_file, column_names)

### USERS ####
json_file = "D:/Yelp/Data/yelp_academic_dataset_user.json"
csv_file = 'C:/Users/anbarasan.selvarasu/Documents/Yelp/users.csv'
column_names = get_superset_of_column_names_from_file(json_file)
read_and_write_file(json_file, csv_file, column_names)

### Business ####
json_file = "D:/Yelp/Data/yelp_academic_dataset_business.json"
csv_file = 'C:/Users/anbarasan.selvarasu/Documents/Yelp/business.csv'
column_names = get_superset_of_column_names_from_file(json_file)
read_and_write_file(json_file, csv_file, column_names)

'''