"""
Get a sample of sentences to select paraphrase candidates from a given conll file.
"""

import collections
import pprint
import random

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
Tags the paraphrased text obtained from quillbot. 
"""
def tag_paraphrase(tokens, labels, new_tokens):
    mentions = get_mentions_from_sent(tokens, labels)  # returns list of (mention,etype) tuples)
    new_labels = ["O"] * len(new_tokens)  # start with all "O"s and replace only those needed.
    for (mention, label) in mentions:
        new_labels[new_tokens.index(mention[0])] = "B-" + label
        for token in mention[1:]:
            new_labels[new_tokens.index(token)] = "I-" + label
    return new_labels

"""
Get mentions from a list of tokens and a corresponding list of
BIO-2 labels.
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

"""
Get a dictionary of mentions and their counts in a conll file, for a given entity tag
e.g, get all PERSON entities in a dataset
"""
def get_mentions_whole(fp, sep, netype):
    sentences, tags = get_conll_data(fp, sep=sep)
    print(len(sentences), len(tags))
    all_mentions = {}  # mention, count
    for i in range(0, len(sentences)):
        sen_mens = get_mentions_from_sent(sentences[i], tags[i])  # list of tuples
        for (men, etype) in sen_mens:
            if etype == netype:
                temp = " ".join(men)
                all_mentions[temp] = all_mentions.get(temp, 0) + 1

    pprint.pprint(sorted(all_mentions.items(), key=lambda x: x[1], reverse=True))
    print(len(all_mentions))

"""
Pick a subset of sentences for a given data type, to generate paraphrases.
tokens: list of strings
labels: corresponding list of labels
netype: targeted entity type
sample_size: size of the sample initially extracted. 
Returns: Two lists of space separated strings for tokens, tags 
"""
def get_subset(tokens, labels, netype, sample_size):
    data_size = len(tokens)
    sub_sents = []
    sub_sents_tags = []
    for i in range(0, data_size):
        if "B-"+netype in labels[i]:
            sub_sents.append(" ".join(tokens[i]))
            sub_sents_tags.append(" ".join(labels[i]))
    print("Total number of sentences; ", data_size)
    print("Number of sentences in the subset: ", len(sub_sents))
    sample_indices = random.sample(range(0, len(sub_sents)), sample_size)
    return [sub_sents[j] for j in sample_indices], [sub_sents_tags[j] for j in sample_indices]

"""
Chooses the final subset for paraphrasing via manual inspection.
tokens: list of strings
labels: corresponding list of labels
netype: targeted entity type
sample_size: size of the sample initially extracted. 
Returns: Two lists of space separated strings for tokens, tags 
"""
def select_from_subset(tokens, labels, netype, sample_size):
    sampled_sentences, sample_sentences_tags = get_subset(tokens, labels, netype, sample_size)
    final_sentences = []
    final_tags = []
    print(len(sampled_sentences))
    for i in range(0, sample_size):
        decision = input("Can we use this sentence? " + sampled_sentences[i] + ":  \n")
        if decision in ["y", "n"]:
            if decision == "y":
                final_sentences.append(sampled_sentences[i])
                final_tags.append(sample_sentences_tags[i])
        else:
            input("Only options are y or n. Enter y or n: \n")
    print("Selected ", str(len(final_sentences)), "for paraphrasing. Let us paraphrase with Quillbot slowly.")
    return final_sentences, final_tags

"""
NE Tag the paraphrased version of a sentence
- keep the tags for entities, and tag others as O
new_tokens, tokens, labels: list of strings
"""
def tag_paraphrase(tokens, labels, new_tokens):
    mentions = get_mentions_from_sent(tokens, labels) #returns list of (mention,etype) tuples)
    new_labels = ["O"]*len(new_tokens) #start with all "O"s and replace only those needed.
    for (mention, label) in mentions:
        new_labels[new_tokens.index(mention[0])] = "B-" + label
        for token in mention[1:]:
            new_labels[new_tokens.index(token)] = "I-" + label
    return new_labels

"""
Use quillbot to get final paraphrased sentences - interactive
Inputs: Two lists of space separated strings for tokens, tags 
Output: pp_tokens (list of list of tokens), pp_tags (list of list of tags)
"""
def collect_paraphrases(final_sentences, final_tags):
    """
    NE Tag the paraphrased version of a sentence
    - keep the tags for entities, and tag others as O
    new_tokens, tokens, labels: list of strings
    """
    pp_tokens = [] #list of list of tokens
    pp_tags = [] #list of list of tags
    size = len(final_sentences)
    for i in range(0,size):
        print(final_sentences[i])
        my_old_tokens = final_sentences[i].split()
        tmp = input("Get the paraphrase for the above sentence from quillbot, manually. \n")
        my_pp_tokens = tmp.split()
        print(my_pp_tokens)
        my_old_tags = final_tags[i].split()
        my_pp_labels = tag_paraphrase(my_old_tokens, my_old_tags, my_pp_tokens)
        print(my_pp_labels)
        pp_tokens.append(my_pp_tokens)
        pp_tags.append(my_pp_labels)
    return pp_tokens, pp_tags

def write_paraphrased_dataset(fp, pp_tokens, pp_tags):
    fw = open(fp, "w", encoding="utf-8")
    assert(len(pp_tokens) == len(pp_tags))
    for i in range(len(pp_tokens)):
        for j in range(0, len(pp_tokens[i])):
            fw.write(pp_tokens[i][j] + "\t" + pp_tags[i][j])
            fw.write("\n")
        fw.write("\n")
    fw.close()
    print("File written to: ", fp)

def main():
    #change these five lines each time appropriately
    fpin = "/Users/Vajjalas/Downloads/NERProjects-Ongoing/conll-03-en/test.txt"
    fpo = "../../tmp/pptest.conll"
    sep = " "
    netype = "PER"
    sample_size = 10

    #sampling a bunch of sentences to paraphrase on quillbot or other such venues
    tokens,labels = get_conll_data(fpin, sep)
    final_sentences, final_tags = select_from_subset(tokens, labels, netype, sample_size)
    pp_tokens, pp_tags = collect_paraphrases(final_sentences, final_tags)
    print("Collected paraphrases, writing to disk")
    write_paraphrased_dataset(fpo, pp_tokens, pp_tags)
    print("DONE")

if __name__ == "__main__":
    main()
