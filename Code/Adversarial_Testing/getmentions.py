"""
Get a dictionary of mentions and their counts in a conll file, for a given entity tag
e.g, get all PERSON entities in a dataset
"""

import collections
import pprint

def get_conll_data(filepath, sep="\t"):
    """Load CoNLL-2003 (English) data split.
    Returns:
        two list of lists - sentences, tags
    """
    fh = open(filepath, encoding="utf-8")
    sentences = []
    tags = []
    tempsen = []
    tempnet = []
    for line in fh:
        if len(line)>1 and not line.startswith("# id"):
            splits = line.strip().split(sep)
            if len(splits) > 1:
                tempsen.append(splits[0].strip())
                tempnet.append(splits[-1].strip())
        else:
                sentences.append(tempsen)
                tags.append(tempnet)
                tempsen = []
                tempnet = []
    fh.close()
    return sentences, tags

"""
Get mentions from a list of tokens and a corresponding list of
BIO-2 labels. Return a list of (start offset, end offset, entity
type) tuples.
"""
def get_mentions_from_sent(tokens, labels):
    assert len(tokens) == len(labels)
    i = 0
    mentions = []
    while i < len(tokens):
        if labels[i][0] == 'B':
            etype = labels[i][2:]
            start = i
            end = i+1
            if end < len(tokens):
                while labels[end][0] == 'I':
                    end += 1
                    if end == len(tokens):
                        break
            mentions.append((tokens[start:end], etype))
            i = end
        else:
            i += 1
    return mentions

#change these three lines each time
fp = "/Users/Vajjalas/Downloads/NERProjects-Ongoing/Ontonotes/ontonotes-bio/bio-everything/onto.test.ner"
netype = "FAC"
sep = "\t"

sentences, tags = get_conll_data(fp, sep=sep)
print(len(sentences), len(tags))
all_mentions = {} #mention, count
for i in range(0,len(sentences)):
    sen_mens = get_mentions_from_sent(sentences[i], tags[i]) #list of tuples
    for (men, etype) in sen_mens:
        if etype == netype:
            temp = " ".join(men)
            all_mentions[temp] = all_mentions.get(temp, 0) + 1

pprint.pprint(sorted(all_mentions.items(), key=lambda x: x[1], reverse=True))

print(len(all_mentions))