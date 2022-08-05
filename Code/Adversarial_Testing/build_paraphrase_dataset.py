"""
Get a sample of sentences to select paraphrase candidates from a given conll file.
"""
from selenium import webdriver
import collections
import pprint
import random
from quillbot import *
import time

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
        if len(line) > 1 and sep in line and not line.startswith("# id") and not line.startswith("-DOCSTART"):
            splits = line.strip().split(sep)
            if len(splits) > 1:
                tempsen.append(splits[0].strip())
                tempnet.append(splits[-1].strip())
        else:
            if tempsen and tempnet:
                sentences.append(tempsen)
                tags.append(tempnet)
                tempsen = []
                tempnet = []
    fh.close()
    print("Num sentences in this dataset: ", len(sentences))
    return sentences, tags

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
def get_subset(tokens, labels, netypes, sample_size):
    data_size = len(tokens)
    sub_sents = []
    sub_sents_tags = []
    netype = random.sample(netypes,1)[0]
    for i in range(0, data_size):
        #if "B-"+netype in labels[i]:
        if "B-" in " ".join(labels[i]):
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
Not using now: Use quillbot to get final paraphrased sentences - interactive
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
        try:
            my_pp_labels = tag_paraphrase(my_old_tokens, my_old_tags, my_pp_tokens)
        except:
            tmp2 = input("Something isn't right. Check the tokenization and entities "
                        "in the paraphrased text manually and enter the text again:  \n")
            my_pp_tokens_new = tmp2.split()
            print(my_pp_tokens_new)
            my_pp_labels = tag_paraphrase(my_old_tokens, my_old_tags, my_pp_tokens_new)
        print(my_pp_labels)
        pp_tokens.append(my_pp_tokens)
        pp_tags.append(my_pp_labels)
    return pp_tokens, pp_tags

"""
Calls functions from quillbot.py to simulate a browser based call to quillbot.
"""
def collect_pp_selenium(final_sentences, final_tags):
    pp_tokens = []  # list of list of tokens
    pp_tags = []  # list of list of tags
    size = len(final_sentences)

    driver = webdriver.Chrome('/Users/vajjalas/Downloads/chromedriver')
    for i in range(0, size):
        time.sleep(10)
        my_pp_tokens = format_sentence(get_paraphrase(final_sentences[i], driver))
        my_old_tokens = final_sentences[i].split()
        my_old_tags = final_tags[i].split()
        try:
            my_pp_labels = tag_paraphrase(my_old_tokens, my_old_tags, my_pp_tokens)
            pp_tokens.append(my_pp_tokens)
            pp_tags.append(my_pp_labels)
        except:
            print("Skipping: ", final_sentences[i])
            continue
    driver.close()
    return pp_tokens, pp_tags

#tokens, tags: space separated strings
def write_dataset(fp, pp_tokens, pp_tags):
    fw = open(fp, "w", encoding="utf-8")
    assert(len(pp_tokens) == len(pp_tags))
    for i in range(len(pp_tokens)):
        fw.write(pp_tokens[i])
        fw.write("\n")
        fw.write(pp_tags[i])
        fw.write("\n\n")
    fw.close()
    print("File written to: ", fp)

def main():
    #change these five lines each time appropriately
    #TODO: Make them args later.
    fpin = "/Users/Vajjalas/Downloads/NERProjects-Ongoing/Summer2022CoOp/wnut17/wnut17test.conll"
    netypes =["PROD", "LOC", "GRP", "PER", "CORP", "CW"] #multiconer
    fpout = "../../tmp/" + "wnut" + "-forpp.conll"
    sep = "\t" #space for multiconer
    sample_size = 600

    #sampling a bunch of sentences to paraphrase on quillbot or other such venues
    tokens,labels = get_conll_data(fpin, sep)
    #print("Choosing sentences for the NE type: ", netype)
    #print("******\n")
    #final_sentences, final_tags = select_from_subset(tokens, labels, netype, sample_size)
    final_sentences, final_tags = get_subset(tokens, labels, netypes, sample_size)
    write_dataset(fpout, final_sentences, final_tags)
    print("Number of sentences in the selected sample: ", len(final_sentences))
    for sen in final_sentences:
        print(sen)
        print()

    #Use the above line instead of select_from_subset, if you just want to send everything to quillbot.
    """
    pp_tokens, pp_tags = collect_pp_selenium(final_sentences, final_tags)
    print("Collected paraphrases, writing to disk")
    write_paraphrased_dataset(fpout, pp_tokens, pp_tags)
    print("Wrote PP dataset for ", netype)
    """

    print("DONE")

if __name__ == "__main__":
    main()