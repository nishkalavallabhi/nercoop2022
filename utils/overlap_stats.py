"""
Functions to estimate entity and mention level overlaps in the dataset splits.
"""


"""
Get unique entity tokens of a given category in a file
"""
def get_all_ents(filepath, cat, sep="\t"):
    allents = []
    numsents = 0
    fh = open(filepath, encoding="utf-8")
    for line in fh:
      if line and not line.startswith("#"):
        splits = line.strip().split(sep)
        entity = splits[0]
        tag = splits[-1]
        if cat in tag:
            allents.append(entity)
      elif line.startswith("#"):
          numsents +=1
    fh.close()
    print("Num sents: ", numsents)
    return set(allents)



"""
get overlaps between two entity lists - first is train, second is dev/test
"""
def get_percent_overlap(set1, set2):
    overlap = len(set2.intersection(set1))/len(set2)
    return overlap

#getting percentage overlaps using get_percent_overlap and get_all_ents
"""
dir = "/Users/Vajjalas/Downloads/NERProjects-Ongoing/Summer2022CoOp/multiconer2022/Hi-Hindi/"
lang = "hi"

path1 = dir+lang+"_train.conll"
path2 = dir+lang+"_test.conll"
tagset = ["PER", "CW", "CORP", "PROD", "LOC", "GRP"]
for tag in tagset:
    print("Token level Overlap between train and test for the tag: ", tag)
    myset1 = get_all_ents(path1, tag, " ")
    myset2 = get_all_ents(path2, tag, " ")
    print(len(myset1), len(myset2))
    print(get_percent_overlap(myset2, myset1))
"""
