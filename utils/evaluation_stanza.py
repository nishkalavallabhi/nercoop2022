#Evaluating performance with Spacy/Stanza (outside command line tools)
import spacy_stanza
from seqeval.metrics import classification_report
from seqeval.metrics import f1_score
import sys
import itertools

snlp = spacy_stanza.load_pipeline(name="de", processors={'ner': 'conll03'}, tokenize_pretokenized=True)
print("Models loaded, and they assume whitespace tokenized text")

def read_file(filepath, sep):
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
          splits = line.strip().split(sep)
          tempsen.append(splits[0])
          tempnet.append(splits[-1])
    fh.close()
    print("Num sentences in: ", filepath, ":", len(sentences))
    return sentences, netags

def eval_stanza(mypath, sep):
    stanza_netags = []
    gold_sen, gold_ner = read_file(mypath, sep)
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
mypath1 = "../code/Adversarial_Testing/generated_datasets/Original Test data/conll_deu_test.txt"
eval_stanza(mypath1, sep="\t")

"""
print("Stanza model's performance on random sampling dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/random_sampling/perturb_conll_deu_test.txt"
eval_stanza(mypath2, sep="\t")

print("Stanza model's performance on faker dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/faker_per+loc/faker_conll_deu_test.txt"
eval_stanza(mypath2, sep="\t")


print("Stanza model's performance on masking dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/Masking/masked_conll_deu.txt"
eval_stanza(mypath2, sep="\t")

#print("Stanza model's performance on paraphrased dataset")
#mypath2 = "../code/Adversarial_Testing/generated_datasets/paraphrases/conll03-test-pp.conll"
#eval_stanza(mypath2, sep="\t")
"""

