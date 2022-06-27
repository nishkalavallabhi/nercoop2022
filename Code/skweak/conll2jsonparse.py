import pandas as pd
class GetSentence(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
     
        agg_func = lambda s: [(w, t) for w, t in zip(s["Word"].values.tolist(),
                                                           s["tag"].values.tolist())]
        self.grouped = self.data.groupby("Sent_ID").apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try:
            s = self.grouped["{}".format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None

data = pd.read_csv("new_data.txt", sep="\t").fillna(method="ffill")
getter = GetSentence(data)
sentences = [[word[0] for word in sentence] for sentence in getter.sentences]
print(sentences[:10])

TRAIN_DATA = []
ent = []
for l in range(len(sent)):
  dict = {}
  text = ""
  text = text+sent[l][0]
  dict["entities"] = [((0, len(sent[l][0]), lab[l][0]))]
  sent[l] = sent[l][1:]
  lab[l] = lab[l][1:]
  for i in range(len(sent[l])):
    # print("l:",l)
    # print("i:",i)
    word = sent[l][i].strip()
    text=text + " "+word
    dict["entities"].append((text.rfind(word), int(text.rfind(word)) + len(word), lab[l][i]))
    ent.append(dict)
  print(dict)
  TRAIN_DATA.append([text, dict])
  with open("data/final_sent_train.json", 'w') as fp:
    json.dump(TRAIN_DATA, fp)