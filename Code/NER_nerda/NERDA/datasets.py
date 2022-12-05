import csv
from itertools import compress
from more_itertools import windowed

def get_conll_data(filepath, sep="\t", allow_long_sentences=False, test=False, prefix=None, prop = None) -> dict:
    """Load CoNLL-2003 (English) data split.
    Returns:
        dict: Dictionary with word-tokenized 'sentences' and named
        entity 'tags' in IOB format.
    """
    # set to default directory if nothing else has been provided by user.
    # read data from file.
    # fh = open(filepath, encoding="utf-8")
    # threshold = 100
    # steps = 100
    # sentences = []
    # tags = []
    # tempsen = []
    # tempnet = []
    # for line in fh:
    #     if len(line)>1 and  not line.startswith("# id"):
    #         splits = line.strip().split(sep)
    #         if len(splits) > 1:
    #             tempsen.append(splits[0].strip())
    #             tempnet.append(splits[-1].strip())
    #         # print("Inside get_conll_data top:",tempsen)
    #     else:
    #         print("Going into else:")
    #         if tempsen and tempnet:
    #           if allow_long_sentences:
    #             if len(tempsen) > threshold:
    #                 moresens = [list(filter(None,list(item))) for item in list(windowed(tempsen, n=threshold, step=steps))]
    #                 if test:
    #                     morenets = [[] for item in list(windowed(tempnet, n=threshold, step=steps))]
    #                 else:
    #                     morenets = [list(filter(None, list(item))) for item in list(windowed(tempnet, n=threshold, step=steps))]
    #                 sentences.extend(moresens)
    #                 tags.extend(morenets)
    #           else:
    #             sentences.append(tempsen)
    #             if test:
    #                 tags.append([])
    #             else:
    #                 tags.append(tempnet)
    #             print("Inside get_conll_data:",sentences)
    #           tempsen = []
    #           tempnet = []
    # print("No. of sentences:",len(sentences))        
    # fh.close()
    numcols = 2 #change here for 3 col vs 4 col conll format.
    fh = open(filepath, encoding="utf-8")
    sentences = []
    netags = []
    tempsen = []
    tempnet = []
    for line in fh:
        if not line.startswith("# id"):
            if line.strip() == "":
                if tempsen and tempnet:
                    sentences.append(tempsen)
                    netags.append(tempnet)
                    tempsen = []
                    tempnet = []
            else:
                splits = line.strip().split()#split("\t")
                # print(len(splits))
                tempsen.append(splits[0])
                tempnet.append(splits[numcols-1])
    fh.close()
    print("Num sentences in: ", filepath, ":", len(sentences))
    # return sentences, netags
    if prefix == 'train':
     size = len(sentences)
     print("Proportion inside datasets.py:", prop)
     index = int(prop * size)
     sentences = sentences[:index]
     netags = netags[:index]
    return {'sentences': sentences, 'tags': netags}


def get_conll_data_for_test(filepath, sep="\t") -> dict:
    """Load CoNLL-2003 (English) data split. But ignores sentence length issues (handles during prediction)
    Returns:
        dict: Dictionary with word-tokenized 'sentences' and named
        entity 'tags' in IOB format.
    """
    # set to default directory if nothing else has been provided by user.
    # read data from file.
    fh = open(filepath, encoding="utf-8")
    sentences = []
    tags = []
    tempsen = []
    tempnet = []
    for line in fh:
        if len(line)>1 and  not line.startswith("# id"):
            splits = line.strip().split(sep)
            if len(splits) > 1:
                tempsen.append(splits[0].strip())
                tempnet.append(splits[-1].strip())
        else: #perhaps we can consider only this, as test set won't have predictions
            if tempsen and tempnet:
                sentences.append(tempsen)
                tags.append([])
            tempsen = []
    fh.close()
    return {'sentences': sentences, 'tags': tags}



