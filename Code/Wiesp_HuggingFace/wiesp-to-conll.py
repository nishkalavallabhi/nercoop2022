"""
Converts the WIESP Dataset format (jsonl) to conll format for NERDA, 
via Huggingface Datasets library
"""
import sys
from datasets import Dataset
from collections import Counter

"""
Takes two list of lists objects - tokens, netags.
saves a conll formatted file.
"""
def json_to_conll(mydataset, filepath):
    tokens_list = mydataset['tokens']
    if "ner_tags" not in mydataset.features:
        tags_list = []
        ner_ids = []
    else:
        tags_list = mydataset['ner_tags'] #What do you do when there are no labels? Add that part. 
        ner_ids = mydataset['ner_ids']
    fh = open(filepath, "w", encoding="utf-8")
    for i in range(0, len(tokens_list)):
        mydict = {}
        mydict["bibcode"] = mydataset['bibcode'][i]
        mydict["label_studio_id"] = mydataset['label_studio_id'][i]
        mydict["section"] = mydataset['section'][i]
        mydict["unique_id"] = mydataset['unique_id'][i]
        id_string = "# id " + str(mydict)
        fh.write(id_string)
        fh.write("\n")
        for j in range(0, len(tokens_list[i])):
            if "ner_tags" not in mydataset.features:
                fh.write(tokens_list[i][j] + "\t" + 'None' + '\t' + 'None')
            else:
                fh.write(tokens_list[i][j] + "\t" + str(ner_ids[i][j]) + "\t" + tags_list[i][j])
            fh.write("\n")
        fh.write("\n")
    fh.close()
    print("Wrote to: ", filepath)

#input and outputpaths as arguments
train_path = sys.argv[1]
train_conll = sys.argv[2] #"../../WIESP2022-NER/wiesp_train.conll"

wiesp_train = Dataset.from_json(path_or_paths=train_path)

json_to_conll(wiesp_train, train_conll)

print("DONE")



