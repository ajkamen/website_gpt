import sys, os, pprint, traceback, time, re
import csv
import sqlite3
import json
import pandas as pd, sqlite3, csv


from test_openai_iab_categorization import *
from relevad_generated_prebid_maps import *


def query_gpt(page:str):
    answer="tier 1: "
    tier_1_categories=""
    for key in iab_codes2names_map:
        if len(key.split('-'))==1:
            tier_1_categories += iab_codes2names_map[key]
            tier_1_categories += ", "
    # print("tier 1 cats are: ", tier_1_categories)

    tier_1_answer = page_ask(page, tier_1_categories)
    time.sleep(1) #one second sleep ensures we don't overflow the amoutn of tokens allowed per second
    answer+=tier_1_answer
    split_tier_1=re.split('; |, |: |\n', tier_1_answer)
    # print("split tier 1: ", split_tier_1)
    tier_1_list=tier_1_categories.split(", ")
    # print("categories to compare against: ", tier_1_list)
    parent_list_ids=[]
    for x in split_tier_1:
        if x and x in tier_1_list:
            # print("category found: ", x)
            bare_id=iab_names2codes_map[x].replace("IAB",'')
            parent_list_ids.append(bare_id)
    # print("tier 1 parent list ids: ", parent_list_ids)
    tier_2_categories=""
    for key in iab_codes2names_map:
        split_ids=key.split('-')
        if len(split_ids)>1:
            if split_ids[1] in parent_list_ids:
                temp_category=iab_codes2names_map[key]
                temp_category=temp_category.split('/')[1]
                tier_2_categories += temp_category
                tier_2_categories += ", "
    # print("tier 2 cat: ", tier_2_categories)
    if(tier_2_categories):
        answer +="\ntier 2: "
        tier_2_answer=page_ask(page, tier_2_categories)
        time.sleep(1)
        answer+=tier_2_answer

        split_tier_2=re.split('; |, |: |\n', tier_2_answer)
        tier_2_list=tier_2_categories.split(", ")
        parent_list_ids_2=[]
        for x in split_tier_2:
            if x and x in tier_2_list:
                # print("category found (tier 2): ", x)
                for temp_key in iab_codes2names_map:
                    parent=iab_codes2names_map[temp_key]
                    if x in parent and len(parent.split('/'))==2:
                        bare_id=iab_names2codes_map[parent].split('-')[0]
                        bare_id=bare_id.replace("IAB", '')
                        parent_list_ids_2.append(bare_id)
        tier_3_categories=""
        for key in iab_codes2names_map:
            split_ids=key.split('-')
            if len(split_ids)>1:
                if split_ids[1] in parent_list_ids_2:
                    temp_category=iab_codes2names_map[key]
                    temp_category=temp_category.split('/')[2]
                    tier_3_categories += temp_category
                    tier_3_categories += ", "
        # print("tier 3 cat: ", tier_3_categories)
        if(tier_3_categories):
            answer +="\ntier 3: "
            tier_3_answer=page_ask(page, tier_3_categories)
            time.sleep(1)
            answer+=tier_3_answer
    answer+="\n\n"

    # print("final gpt answer output: ", answer)
    return(answer)

