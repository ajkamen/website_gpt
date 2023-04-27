import sys, os, pprint, traceback, time, re, math
import csv
import sqlite3
import json
import pandas as pd, sqlite3, csv

from relevad_generated_prebid_maps import *
from nlp_gpt_query import *


def output(filename):
    df = pd.read_csv(filename, header=None)

    df.columns=df.iloc[0]
    # for col in df.columns:
    #   print(col)

    websites=df["page"]
    unprocessed_answers=df["answer"]
    # print(unprocessed_answers.to_string())
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
        if website_index!=0:
            # print(test_list)
            # print(websites[website_index])
            testframe.loc[website_index,0]=websites[website_index]
            for i in range(len(test_list)):
                testframe.loc[website_index,i+1]=test_list[i]
        website_index+=1
    testframe.rename(columns={0:'Website', 1:'Category 1', 2:'Category 2', 3:'Category 3', 4:'Category 4', 5:'Category 5', 6:'Category 6'},  inplace=True)
    # print(testframe)
    testframe.to_csv('test_output.csv')


def websites(filename):
    df = pd.read_csv(filename, usecols = [0], header=None)

    unprocessed_answers=[]
    for page in df[0]:
        print(page)
        if page==0:
            continue
        unprocessed_answers.append(query_gpt(page))

    # print(df.to_string())
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
            testframe.loc[website_index,0]=df[0].iloc[website_index]
            for i in range(len(test_list)):
                testframe.loc[website_index,i+1]=test_list[i]
        website_index+=1
    testframe.rename(columns={0:'Website', 1:'Category 1', 2:'Category 2', 3:'Category 3', 4:'Category 4', 5:'Category 5', 6:'Category 6'},  inplace=True)
    # print(testframe)
    testframe.to_csv('test_output.csv')



if __name__ == '__main__':

    if len(sys.argv) != 3:
        print(f'''
                  Usage:
                      {sys.argv[0]} -w <csv of websites filename>
                      {sys.argv[0]} -o <output of independent categorization>
            ''')
        sys.exit(0)


    filename=sys.argv[2]

    if sys.argv[1]=='-0':
        output(filename)
    elif sys.argv[1]=='-w':
        websites(filename)
    else:
        print(f'''
                  Usage:
                      {sys.argv[0]} -w <csv of websites filename>
                      {sys.argv[0]} -o <output of independent categorization>
            ''')
        sys.exit(0)




