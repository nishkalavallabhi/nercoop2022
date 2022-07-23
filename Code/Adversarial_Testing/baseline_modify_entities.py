import csv
import pandas as pd
# from faker import Faker
import random

mypath = "mconer_test.conll"
# mypath = "wnut17test.conll"

#anything to edit
# mycat = 'PERSON' #PERSON, ORG, GPE
# #GPE is countries, cities, states; ORG: companies, agencies, institutions;
# fake = Faker('en_IN') #This can be changed to many other options. 
myoutput = "perturb_mconer-wnut_test.conll" #CHANGE THIS

fh = open(mypath, encoding="utf-8")
fw = open(myoutput, "w", encoding="utf-8")


def read_file_multi(filepath):
    numcols = 2 #change here for 3 col vs 4 col conll format.
    fh = open(filepath, encoding="utf-8")
    sentences = []
    netags = []
    tempsen = []
    tempnet = []
    for line in fh:
       if line.strip() == "":
          if tempsen and tempnet:
              sentences.append(tempsen)
              netags.append(tempnet)
              tempsen = []
              tempnet = []
       else:
          splits = line.strip().split("\t")
          tempsen.append(splits[0])
          tempnet.append(splits[numcols-1])
    fh.close()
    print("Num sentences in: ", filepath, ":", len(sentences))
    return sentences, netags

def read_file_wnut17(filepath):
    numcols = 2 #change here for 3 col vs 4 col conll format.
    fh = open(filepath, encoding="utf-8")
    sentences = []
    netags = []
    tempsen = []
    tempnet = []
    for line in fh:
       if line.strip() == "":
          if tempsen and tempnet:
              sentences.append(tempsen)
              netags.append(tempnet)
              tempsen = []
              tempnet = []
       else:
          splits = line.strip().split("\t")
          tempsen.append(splits[0])
          tempnet.append(splits[numcols-1])
    fh.close()
    print("Num sentences in: ", filepath, ":", len(sentences))
    return sentences, netags

words, tags = read_file_wnut17("wnut17test.conll")
print(len(words))
# print("Words:",words[0])
# print("tags:",tags[0])
ent_dict = {}
for i in range(len(tags)):
    for j in range(len(tags[i])):
        if tags[i][j] not in ent_dict:
            ent_dict[tags[i][j]] = [words[i][j]]
        else:
            # print(ent_dict)
            ent_dict[tags[i][j]].append(words[i][j])

for i in range(len(tags)):
    for j in range(len(tags[i])):
        if tags[i][j][2:] not in ent_dict:
            ent_dict[tags[i][j]][2:] = [words[i][j]]
        else:
            # print(ent_dict)
            if tags[i][j][0] == "I":
                ent_dict[tags[i][j-1]][2:][words[i][j]]
            ent_dict[tags[i][j]][2:].append(words[i][j])

# print("Ent_Dict:",ent_dict['B-PER'][-1])

numcols = 2
# for line in fh:
#     splits = line.strip().split("\t")
#     if len(splits) == 2:
#         if splits[numcols-1] != 'O':
#             #Lines commented below are for GPE. 
#             temp = splits[0]
#             rand = random.choice(ent_dict[splits[numcols - 1]])
#             if rand != temp:
#                 splits[0] = rand 
#             else:
#                 splits[0] = random.choice(ent_dict[splits[numcols - 1]])
#             temp = splits[0]
#             # print("Gotta remove:",temp, " Type:", splits[numcols - 1])
#             # print("Dict:",ent_dict[splits[numcols - 1]])
#             if temp in ent_dict[splits[numcols - 1]]:
#                 ent_dict[splits[numcols - 1]].remove(temp)
#         # splits[0] = fake.name_female().split()[0]
#             #splits[0] = random.choice([fake.county(), fake.country(), fake.city()]).split()[0]
#         # elif splits[numcols-1] == 'I-'+mycat:
#         #     splits[0] = fake.last_name_female().split()[0]
#             #splits[0] = fake.city_suffix().split()[0]
#         print("\t".join(splits))
#         fw.write("\t".join(splits))
#         fw.write("\n")
#     else:
#         fw.write("\n")



for line in fh:
    splits = line.strip().split("\t")
    if len(splits) == 2:
        if splits[numcols-1] != 'O':
            #Lines commented below are for GPE. 
            temp = splits[0]
            if len(ent_dict[splits[numcols - 1]]) != 0:
                rand = random.choice(ent_dict[splits[numcols - 1]])
                splits[0] = rand 
            else:

            temp = splits[0]
            # print("Gotta remove:",temp, " Type:", splits[numcols - 1])
            # print("Dict:",ent_dict[splits[numcols - 1]])
            if temp in ent_dict[splits[numcols - 1]]:
                ent_dict[splits[numcols - 1]].remove(temp)
        # splits[0] = fake.name_female().split()[0]
            #splits[0] = random.choice([fake.county(), fake.country(), fake.city()]).split()[0]
        # elif splits[numcols-1] == 'I-'+mycat:
        #     splits[0] = fake.last_name_female().split()[0]
            #splits[0] = fake.city_suffix().split()[0]
        print("\t".join(splits))
        fw.write("\t".join(splits))
        fw.write("\n")
    else:
        fw.write("\n")

fh.close()
fw.close()
print("DONE")