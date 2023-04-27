import sys, os, pprint, traceback, time, re, math
import csv
import sqlite3
import json
import pandas as pd, sqlite3, csv

from .relevad_generated_prebid_maps import *
from .nlp_gpt_query import *


def file_processor(elements):

    unprocessed_answers=[]
    for page in elements:
        # print(page)
        if page==0:
            continue
        unprocessed_answers.append(query_gpt(page))
    website_index=0

    testframe=pd.DataFrame(columns=[0, 1, 2, 3, 4, 5, 6])
    for x in unprocessed_answers:
        if type(x) != str:
            continue
        # print(x)

        test_list=[]
        split_x=re.split('; |, |: |\n', x)
        while "" in split_x:
            split_x.remove("")
        # print(split_x)

        for y in split_x:
            if len(test_list) >=6:
                break
            for key in iab_names2codes_map.keys():
                if y in key:
                    split_key=key.split('/')
                    len_split=len(split_key)
                    if y==split_key[len_split-1]:
                        test_list.append(key)
                        break
        if website_index!=-1:
            # print(test_list)
            # print(websites[website_index])
            testframe.loc[website_index,0]=elements[website_index]
            for i in range(len(test_list)):
                testframe.loc[website_index,i+1]=test_list[i]
        website_index+=1
    testframe.rename(columns={0:'Website', 1:'Category 1', 2:'Category 2', 3:'Category 3', 4:'Category 4', 5:'Category 5', 6:'Category 6'},  inplace=True)
    # print(testframe)
    return testframe

def single_element_processor(element:str):

    x=query_gpt(element)
    website_index=0

    # print(x)

    test_list=[]
    split_x=re.split('; |, |: |\n', x)
    while "" in split_x:
        split_x.remove("")
    # print(split_x)

    for y in split_x:
        if len(test_list) >=6:
            break
        for key in iab_names2codes_map.keys():
            if y in key:
                split_key=key.split('/')
                len_split=len(split_key)
                if y==split_key[len_split-1]:
                    test_list.append(key)
                    break

    return test_list