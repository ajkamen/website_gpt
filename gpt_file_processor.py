#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# standard imports
import os, sys, pprint, traceback, time

# import openai api
from test_openai_iab_categorization import *

#import csv file reader
import csv

max_rep=100
x=1 #temporary variables for limiting large files

if len(sys.argv) != 3:
	print(f'''
              Usage:
                  {sys.argv[0]} -p       <prompt filename/path>
                  {sys.argv[0]} -w       <websites filename/path>
        ''')
	sys.exit(0)

if sys.argv[1]=="-p":
	filename=sys.argv[2]
	prompts_file=open(filename, 'r')

	output_prompts=open("output_prompts.csv", 'w')
	output_writer=csv.writer(output_prompts, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for prompt in prompts_file:
		if prompt =='\n':
			continue
		if(prompt[-1]==','):
			prompt=prompt[:-1]
		response=prompt_ask(prompt)
		output_writer.writerow([prompt, response])
		if(x>max_rep):
			break
		x+=1
		print("prompts completed: ", x-1)
		time.sleep(10) #limited tokens per minute


	print("finished prompts")
	prompts_file.close()
	output_prompts.close()


elif sys.argv[1]=="-w":
	filename=sys.argv[2]
	categories_file=open("categories.txt", 'r')
	categories=categories_file.readline()
	categories_file.close()

	sites_file=open(filename, 'r')

	output_sites=open("output_sites.csv", 'w')
	output_writer=csv.writer(output_sites, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

	for site in sites_file:
		if(x>max_rep):
			break
		if site =='\n':
			continue
		if(site[-1]==','):
			site=site[:-1]
		response=page_ask(site, categories)
		output_writer.writerow([site, response])


		print("sites completed: ", x)
		x+=1
		time.sleep(10)

	print("finished sites")
	sites_file.close()
	output_sites.close()


else:
	print(f'''
              Invalid keyword. Usage:
                  {sys.argv[0]} -p       <prompt filename/path>
                  {sys.argv[0]} -w       <websites filename/path>
        ''')
	sys.exit(0)