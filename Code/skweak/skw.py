import pandas as pd
import numpy as np
from tqdm import tqdm, trange
import itertools 
from typing import Iterable, Tuple
import re, json, os
# import snips_nlu_parsers
from skweak.base import CombinedAnnotator, SpanAnnotator
from skweak.spacy import ModelAnnotator, TruecaseAnnotator
from skweak.heuristics import FunctionAnnotator, TokenConstraintAnnotator, SpanConstraintAnnotator, SpanEditorAnnotator
from skweak.gazetteers import GazetteerAnnotator, extract_json_data
from skweak.doclevel import DocumentHistoryAnnotator, DocumentMajorityAnnotator
from skweak.aggregation import MajorityVoter
from skweak import utils
from spacy.tokens import Doc, Span
import spacy
import skweak
import LabelNer

docs = list(skweak.utils.docbin_reader("data/btca.spacy"))
# docs = list(skweak.utils.docbin_reader("data/wnut17train.spacy"))
# docs = list(skweak.utils.docbin_reader("data/mconer_train.spacy"))
for doc in docs:
  doc.ents = ""
full_annotator = LabelNer.NERAnnotator().add_all()

docs = list(full_annotator.pipe(docs))
unified_model = skweak.aggregation.HMM("hmm", ["LOC", "ORG", "MISC", "PER"])
unified_model.add_underspecified_label("ENT", ["LOC", "CORP", "MISC", "PER"]) 
# unified_model = skweak.aggregation.HMM("hmm", ["LOC", "CORP", "PER", "PROD", "GRP", "CW"])
# unified_model.add_underspecified_label("ENT", ["LOC", "CORP", "PER", "PROD", "GRP", "CW"]) 
# We then run Baum-Welch on the model (can take some time)
unified_model.fit(docs*9)
docs = list(unified_model.pipe(docs))
print("Done !")
for doc in docs:
    doc.ents = doc.spans["hmm"]
    # for d in doc.ents:
    #   print(d.label_)

skweak.utils.docbin_writer(docs, "data/weak_btc.spacy")  
# skweak.utils.docbin_writer(docs, "data/weak_wnut17.spacy")
# skweak.utils.docbin_writer(docs, "data/weak_mconer.spacy")

print("Wrote DocBin file to disk !")
# print(skweak.utils.display_entities(docs[0], "hmm"))