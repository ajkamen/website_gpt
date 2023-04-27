import sys, os, pprint, traceback, time, re
import csv
import sqlite3
import json
import pandas as pd, sqlite3, csv


from test_openai_iab_categorization import *
from relevad_generated_prebid_maps import *
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SAFE_PRAGMAS = True
PRAGMA_MMAP_SIZE = 1000*1000*1000 # 1bln bytes
PRAGMA_CACHE_SIZE = 1*1000*1000  # 1mln pages

#ISOLATION_LEVEL = None       # default: "DEFERRED"  # see https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions
ISOLATION_LEVEL  = "DEFERRED" # default: "DEFERRED"  # see https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions
                              # see also https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
debug = True
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def set_pragmas(con):
    """Execute sqlite3 pragmas for better performance

    Args:
        con (sqlite database connection): sqlite database connection
    """
    con.execute('pragma journal_mode = WAL')
    con.execute('pragma synchronous = normal')
    con.execute('pragma temp_store = memory')
    con.execute(f'pragma mmap_size = {PRAGMA_MMAP_SIZE}')
    con.execute(f'pragma cache_size = {PRAGMA_CACHE_SIZE}')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_loadplan(dbname: str, dbtable: str, debug: int=debug):
    #t = time.time()
    with sqlite3.connect(dbname, isolation_level=ISOLATION_LEVEL) as con:
        set_pragmas(con)

        cur = con.cursor()

        while True:
            # ..... Get a record from the database
            res = cur.execute("BEGIN")
            res = cur.execute("SELECT page, status, updated_at FROM openai_loadplan WHERE status NOT IN ('d', 'x', 'p') LIMIT 1");
            for page, status, updated_at in res.fetchall():
                print(f'{page=} {status=} {updated_at}')
                break
            else: # no records found
                return

            # ~~~~~~~~~ set status to in-progress ASAP
            cur.execute("UPDATE openai_loadplan SET status = 'p' WHERE page = ?", (page,))
            cur.execute("COMMIT")

            # ~~~~~~~~ call openai
            try:
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

                print("final gpt answer output: ", answer)




                status = 'd' if answer else 'f'
            except Exception as e:
                status = 'f'
                answer = ''
                print("ERROR: ~~~~~ {e=}")
                traceback.print_exc()

            # ~~~~~ update status
            res = cur.execute("BEGIN")
            cur.execute("UPDATE openai_loadplan SET answer = ?, status = ? WHERE page = ?", (answer, status, page))
            cur.execute("COMMIT")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def page_ask(page:str, categories:str=None) -> str:
    """
    Return openai answer, emtpy or None means failure
    """
    answer = page_ask(page, categories)
    return answer # TODO: Arik

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    dbname = 'openai.db'
    dbtable = 'openai_loadplan'



    process_loadplan(dbname=dbname, dbtable=dbtable)

    #dt = time.time() - t
    #dt = round(dt,3)
    #print(f' Total time for {len(fnames)} files: {dt} sec')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print(f'''
                  Usage:
                      {sys.argv[0]} <csv of websites filename>
            ''')
        sys.exit(0)


    filename=sys.argv[1]

    try:
        df = pd.read_csv(filename, header=None)
        conn = sqlite3.connect("openai.db")
        conn.execute('BEGIN')
        df.to_sql('temp_table', conn, if_exists='replace', index=False)
        conn.execute("INSERT INTO openai_loadplan(page) SELECT * from temp_table WHERE 1 ON CONFLICT(page) DO UPDATE SET status='u'")
        conn.execute('DROP TABLE temp_table')
        conn.execute("DELETE from openai_loadplan WHERE page LIKE '%googlesyndication%';")
        conn.execute('COMMIT')
        conn.close()


        main()
    except Exception as e:
        print(f'~~~~~~~~~~~~ ERROR: Exception {e=}')
        traceback.print_exc()
        sys.exit(255) # forces xargs to stop
