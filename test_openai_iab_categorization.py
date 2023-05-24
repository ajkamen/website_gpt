#!/usr/bin/env python3
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# standard imports
import os, sys, pprint, traceback

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# openai APIs.To install:
#     pip install openai
import openai

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_key = 'YOUR_API_KEY_HERE' # put your api key for chat GPT here
openai.api_key = api_key

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# .............. model parameters ...................
engine = "text-davinci-003" # chatgpt model
max_tokens = 2000
n = 1
stop = None
temperature = 0.5

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_prompt(prompt, engine=engine, max_tokens=max_tokens, n=n, stop=stop, temperature=temperature):
    return openai.Completion.create(prompt=prompt, engine=engine, max_tokens=max_tokens, n=n, stop=stop, temperature=temperature)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_page(page, categories=None, engine=engine, max_tokens=max_tokens, n=n, stop=stop, temperature=temperature):
    if(categories==None):
        prompt="categorize the web page" + page + " using IAB 2.2 categories. Do not use numbers"
    else:
        prompt = "categorize the web page" + page + " using categories from the following list: " + categories
    #original: tell me IAB category codes for this web page:
    return openai.Completion.create(prompt=prompt, engine=engine, max_tokens=max_tokens, n=n, stop=stop, temperature=temperature)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def prompt_ask(prompt):
    completion = process_prompt(prompt=prompt)
    return(completion.choices[0].text)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def page_ask(page, categories=None):
    completion = process_page(page=page, categories=categories)
    return(completion.choices[0].text)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'''
              Usage:
                  {sys.argv[0]} -p       <prompt phrase>
                  {sys.argv[0]} --prompt <prompt phrase>
                  {sys.argv[0]} page urls
        ''')

    # process one prompt phrase
    if len(sys.argv) > 1 and sys.argv[1] in ['-p', '--prompt']:
        prompt = ' '.join(sys.argv[2:])
        completion = process_prompt(prompt=prompt)
        print(completion.choices[0].text)
        sys.exit(0)

    # process page urls
    for page in sys.argv[1:]:
        completion = process_page(page=page)
        print(completion.choices[0].text)

    # ................... Obsolete tests [[[[[
    #completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=4000, n=1, stop=None, temperature=0.5)
    #print(completion.choices[0].text)

    #prompt = "tell me IAB category codes for this web page: https://disneyworld.disney.go.com/events-tours/epcot/epcot-international-food-and-wine-festival/"
    #completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=4000, n=1, stop=None, temperature=0.5)
    #print(completion.choices[0].text)

	#engines = openai.Engine.list()
	#completion = openai.Completion.create(engine="ada", prompt="Hello world")
	#print(completion.choices[0].text)
	#completion = openai.Completion.create(engine="ada", prompt="categorize whit web page using IAB categories: https://github.com/openai/openai-python")
	#print(completion.choices[0].text)
	#print(completion.choices)
	#completion = openai.Completion.create(engine="chatgpt", prompt="categorize  web page using IAB categories: https://github.com/openai/openai-python")
	#completion = openai.Completion.create(engine="gpt", prompt="categorize  web page using IAB categories: https://github.com/openai/openai-python")
	#completion = openai.Completion.create(engine="ada", prompt="categorize using IAB categories: https://github.com/openai/openai-python")
	#print(completion.choices)
	#completion = openai.Completion.create(engine="text-similarity-davinci-001", prompt="categorize using IAB categories: https://github.com/openai/openai-python")
	#print(completion.choices)
	#completion = openai.Completion.create(engine="text-similarity-davinci-001", prompt="IAB categories: https://github.com/openai/openai-python")
	#print(completion.choices)
    # ................... Obsolete tests ]]]]]

