import random
import spacy
from spacy.util import minibatch, compounding
from pathlib import Path
from spacy.training.example import Example

f = open("data/final_sent_train.json")
TRAIN_DATA = json.load(f)

for _, annotations in TRAIN_DATA:
  for ent in annotations.get("entities"):
    # print(ent[2])
    ner.add_label(ent[2])
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# TRAINING THE MODEL
with nlp.disable_pipes(*unaffected_pipes):

  # Training for 30 iterations
  for iteration in range(30):

    # shuufling examples  before every 
    # nlp.begin_training()
    random.shuffle(TRAIN_DATA)
    losses = {}
    # batch up the examples using spaCy's minibatch
    # batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in spacy.util.minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001)):
      for text, annotations in batch:
          # create Example
          doc = nlp.make_doc(text)
          example = Example.from_dict(doc, annotations)
          # Update the model
          # print("Anno: ",annotations)
          nlp.update([example], losses=losses, drop=0.5)
          print("Losses: ", losses)
 
        
