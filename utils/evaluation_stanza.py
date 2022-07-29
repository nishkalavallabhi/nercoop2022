#Evaluating performance with Spacy/Stanza (outside command line tools)
import spacy, stanza, spacy_stanza
from spacy.tokenizer import Tokenizer
from seqeval.metrics import classification_report
from seqeval.metrics import f1_score
import sys
import itertools

def read_file(filepath):
    fh = open(filepath)
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
          tempnet.append(splits[-1])
    fh.close()
    print("Num sentences in: ", filepath, ":", len(sentences))
    return sentences, netags

def eval_stanza(mypath):
    snlp = spacy_stanza.load_pipeline(name="en", processors={'ner': 'conll03'}, tokenize_pretokenized=True)
    print("Models loaded, and they assume whitespace tokenized text")
    stanza_netags = []
    gold_sen, gold_ner = read_file(mypath)
    for sen in gold_sen:
        actual_sen = " ".join(sen)
        doc_stanza = snlp(actual_sen)
        temp_tags_stanza = []
        for token in doc_stanza:
            if token.ent_iob_ and token.ent_type_:
                tag = token.ent_iob_ + "-" + token.ent_type_
            else:
                tag = "O"

            temp_tags_stanza.append(tag)
        stanza_netags.append(temp_tags_stanza)
    print("Classification report for Stanza NER: ")
    print(classification_report(gold_ner, stanza_netags, digits=4))

print("Stanza model's performance on standard test set")
mypath1 = "/Users/Vajjalas/Downloads/NERProjects-Ongoing/conll-03-en/test.txt"
eval_stanza(mypath1)

print("Stanza model's performance on paraphrased dataset")
mypath2 = "../tmp/conll03netype-pp.conll"
eval_stanza(mypath2)
