import os, sys, pprint, traceback, time, shutil


filename = "IAB categories names only all tiers.csv"

iabs=open(filename, 'r')
current_dir=os.getcwd()
new_dir="Tier 1"
tier_0_path=os.path.join(current_dir, new_dir)
if os.path.isdir(tier_0_path):
	shutil.rmtree(tier_0_path)
os.mkdir(tier_0_path)
tier_1_cat_list=""

for line in iabs:
	split_line=line.split(",")
	tier_1_cat=split_line[0]
	split_line.pop(0)
	tier_1_path=os.path.join(tier_0_path, tier_1_cat)
	if not os.path.isdir(tier_1_path):
		os.mkdir(tier_1_path)
	if tier_1_cat not in tier_1_cat_list:
		tier_1_cat_list+=tier_1_cat
		tier_1_cat_list+=", "
iabs.close()

print("got to the txt")
os.chdir(tier_1_path)
tier_1_txt=open("list of tier 1 categories.txt", 'w')
tier_1_txt.write(tier_1_cat_list) #not working for some reason?
tier_1_txt.close()
print("the list was: "+tier_1_cat_list)
