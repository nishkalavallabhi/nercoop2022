import spacy
from seqeval.metrics import classification_report

def get_tags(path, nlp):
	samples= list(skweak.utils.docbin_reader(path))
	s_tags = []
	t_tags = []
	for e in samples:
	  t_tags_temp = []
	  for l in e:
	    if l.ent_iob_ and l.ent_type_:
	        ne = l.ent_iob_+"-"+l.ent_type_
	    else:
	      ne = l.ent_iob_
	    t_tags_temp.append(ne)
	  t_tags.append(t_tags_temp)
	  s_tags_temp = []
	  for t in nlp(e):
	    if t.ent_iob_ and t.ent_type_:
	        tag = t.ent_iob_+"-"+t.ent_type_
	    else:
	      tag = t.ent_iob_
	    s_tags_temp.append(tag)
	  s_tags.append(s_tags_temp)
	  return (t_tags, s_tags)

#EVALUATION
nlp = spacy.load("data/model-best")
path = "data/wnut17test.spacy"
t_tags, s_tags = get_tags(path)
print("Classification report for Spacy NER: ")
print(classification_report(t_tags, s_tags, digits=4))