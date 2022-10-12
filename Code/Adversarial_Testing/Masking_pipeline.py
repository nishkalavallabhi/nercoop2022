import pandas as pd
import numpy as np
import random
from transformers import pipeline
import argparse


#Feed datasets tagged with sentence IDs and column titles
#Install transformers

class SentenceGetter(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
     
        agg_func = lambda s: [(w, t) for w, t in zip(s["Word"].values.tolist(),
                                                           s["Tag"].values.tolist())]
        self.grouped = self.data.groupby("Sent_ID").apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try:
            s = self.grouped["{}".format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None



class TransformerAugmenter():
    """
    Use the pretrained masked language model to generate more
    labeled samples from one labeled sentence.
    """
    
    def __init__(self):
        self.num_sample_tokens = 5
        self.fill_mask = pipeline(
            "fill-mask",
            model="bert-base-uncased"
        )
    
    def generate(self, sentence, num_replace_tokens=3):
        """Return a list of n augmented sentences."""
              
        # run as often as tokens should be replaced
        augmented_sentence = sentence.copy()
        masks = []
        for i in range(num_replace_tokens):
            # join the text
            text = " ".join([w[0] for w in augmented_sentence])
            # pick a token
            replace_token = random.choice(augmented_sentence)
            c=0
            while replace_token[1] != 'O' or replace_token[0] in masks :
               replace_token = random.choice(augmented_sentence)
               c = c + 1
               if c>len(augmented_sentence):
                 break
            masks.append(replace_token[0])
            # mask the picked token
            masked_text = text.replace(
                replace_token[0],
                f"{self.fill_mask.tokenizer.mask_token}",
                1            
            )
            # fill in the masked token with Bert
            res = self.fill_mask(masked_text)[random.choice(range(self.num_sample_tokens))]
            # create output samples list
            tmp_sentence, augmented_sentence = augmented_sentence.copy(), []
            for w in tmp_sentence:
                if w[0] == replace_token[0]:
                    # print(res['token_str'])
                    # print(w)
                    # print(w[1])
                    # print(w[2])
                    augmented_sentence.append((res["token_str"].replace("Â", ""), w[1]))
                else:
                    augmented_sentence.append(w)
            text = " ".join([w[0] for w in augmented_sentence])
        return [sentence, augmented_sentence] 


def write_to_disk(new_file_name, aug_sentences):
  fw = open("new_conll03_test.txt", "w", encoding="utf-8")
  for i in aug_sentences:
    for j in i:
      print(j[0])
      fw.write(j[0].strip()+"\t"+j[1])
      fw.write("\n")
    fw.write("\n")
  print("Wrote to disk !")

def main(args):

  data = pd.read_csv(args.input_file, sep="\t")
  data = data.fillna(method="ffill")

  # Replace double quotes(") with '$#$' in all the input test sentences before feeding it to the argparser
  for i in range(len(data["Word"])):
    if data['Word'][i] == "$#$":
      data['Word'][i] = '"'
  getter = SentenceGetter(data)
  sentences = getter.sentences

  augmenter = TransformerAugmenter()
  aug_sentences = []
  for i in sentences:
    aug = augmenter.generate(i, num_replace_tokens=3)
    aug_sentences.append(aug)

  write_to_disk(args.output_file, aug_sentences)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", help="Name or path of the input test file", required=True)
    parser.add_argument("--output_file", help="Name or path of the modified output test file", required=True)
    args=parser.parse_args()
    main(args)



