#Evaluate Flair conll03-EN and conll03-DE models
from flair.data import Sentence, Token
from flair.models import SequenceTagger
from seqeval.metrics import classification_report
from seqeval.metrics import f1_score

tagger = SequenceTagger.load("flair/ner-german")  # -fast")
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

#CHECK: https://pythontechworld.com/issue/flairnlp/flair/2729
def eval_flair(mypath, sep):
    flair_netags = []
    gold_sen, gold_ner = read_file(mypath, sep)
    for sen in gold_sen:
        temp_tags = []
        actual_sen = Sentence(sen)  # pass a list of tokens if you want to use pre-tokenized sentence.
        tagger.predict(actual_sen)
        temp_tags = []

        # transfer entity labels to token level
        for entity in actual_sen.get_spans('ner'):
            prefix = 'B-'
            for token in entity:
                token.set_label('ner-bio', prefix + entity.tag, entity.score)
                prefix = 'I-'
        for token in actual_sen:
            temp_tags.append(token.get_label().value)

        flair_netags.append(temp_tags)
        if len(flair_netags)%100 == 0:
            print(str(len(flair_netags)), " sentences processed so far out of ", str(len(gold_sen)))
    print("Classification report for Flair NER: ")
    print(classification_report(gold_ner, flair_netags, digits=4))

print("Flair model's performance on standard test set")
mypath1 = "../code/Adversarial_Testing/generated_datasets/Original Test data/conll_deu_test.txt"
eval_flair(mypath1, sep="\t")

print("Flair model's performance on random sampling dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/random_sampling/perturb_conll_deu_test.txt"
eval_flair(mypath2, sep="\t")

print("Flair model's performance on faker dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/faker_per+loc/faker_conll_deu_test.conll"
eval_flair(mypath2, sep="\t")

print("Flair model's performance on masking dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/Masking/masked_conll_deu.txt"
eval_flair(mypath2, sep="\t")

"""
print("Flair model's performance on paraphrased dataset")
mypath2 = "../code/Adversarial_Testing/generated_datasets/paraphrases/conll03-test-pp.conll"
eval_flair(mypath2, sep="\t")
"""
