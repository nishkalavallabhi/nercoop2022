import itertools
import json
from typing import Dict, Iterable, List, Tuple
import os
import spacy
from spacy.tokens import Doc, Span  # type: ignore
import spacy
from spacy.training import Example
from spacy.tokens import DocBin
import torch
from tner import TransformersNER
from .base import SpanAnnotator

####################################################################
# Labelling source based on neural models
####################################################################

class Standardiser(SpanAnnotator):

  def __init__(self):
      super(Standardiser, self).__init__("")

  def __call__(self, doc):
      """Annotates one single document"""     
            
      for source in doc.spans:
            
          new_spans = []  
          for span in doc.spans[source]:
              if "\n" in span.text:
                  continue
              elif span.label_ in {"person", "PERSON", "PER", "per"}:
                  new_spans.append(Span(doc, span.start, span.end, label="PER"))

              elif span.label_ in {"group", "GROUP", "GRP", "grp", "NORP", "norp", "ORG", "org"}:
                  new_spans.append(Span(doc, span.start, span.end, label="GRP"))

              elif span.label_ in {"corporation", "CORPORATION", "CORP", "FAC", "fac"}:
                  new_spans.append(Span(doc, span.start, span.end, label="CORP"))

              elif span.label_ in {"location", "GPE", "LOCATION", "gpe", "loc"}:
                  new_spans.append(Span(doc, span.start, span.end, label="LOC"))

              # elif span.label_ in {"EVENT", "FAC", "LANGUAGE", "LAW", "NORP", "WORK_OF_ART", "creative-work"}:
              #     new_spans.append(Span(doc, span.start, span.end, label="MISC"))

              elif span.label_ in {"product", "PRODUCT", "PROD"}:
                  new_spans.append(Span(doc, span.start, span.end, label="PROD"))

              elif span.label_ in {"WORK_OF_ART", "creative-work", "work of art", "work-of-art", "work_of_art"}:
                  new_spans.append(Span(doc, span.start, span.end, label="CW"))
              else:
                  new_spans.append(span)         
          doc.spans[source] = new_spans      
      return doc
class ModelAnnotator(SpanAnnotator):
    """Annotation based on a spacy NER model"""

    def __init__(self, name:str, model_path:str, 
                 disabled:List[str]=["parser", "tagger", "lemmatizer", "attribute_ruler"]):
        """Creates a new annotator based on a Spacy model. """
        
        super(ModelAnnotator, self).__init__(name)
        self.model = spacy.load(model_path, disable=disabled)


    def find_spans(self, doc: Doc) -> Iterable[Tuple[int, int, str]]:
        """Annotates one single document using the Spacy NER model"""

        # Create a new document (to avoid conflicting annotations)
        doc2 = self.create_new_doc(doc)
        # And run the model
        for _, proc in self.model.pipeline:
            doc2 = proc(doc2)
        # Add the annotation
        for ent in doc2.ents:
            yield ent.start, ent.end, ent.label_

    def pipe(self, docs: Iterable[Doc]) -> Iterable[Doc]:
        """Annotates the stream of documents based on the Spacy model"""
        print("calling pipe method..")
        stream1, stream2 = itertools.tee(docs, 2)

        # Remove existing entities from the document
        stream2 = (self.create_new_doc(d) for d in stream2)
        
        # And run the model
        for _, proc in self.model.pipeline:
            stream2 = proc.pipe(stream2)
        
        for doc, doc_copy in zip(stream1, stream2):

            doc.spans[self.name] = []

            # Add the annotation
            for ent in doc_copy.ents:
                doc.spans[self.name].append(Span(doc, ent.start, ent.end, ent.label_))
            # print("Entities:",doc.ents)
            # print(self.name)
            yield doc

    def create_new_doc(self, doc: Doc) -> Doc:
        """Create a new, empty Doc (but with the same tokenisation as before)"""

        return spacy.tokens.Doc(self.model.vocab, [tok.text for tok in doc], #type: ignore
                               [tok.whitespace_ for tok in doc])


class TransformerAnnotator(SpanAnnotator):
    def __init__(self, name:str, model_path:str):
        print("Loading TNER model...")
        super(TransformerAnnotator, self).__init__(name)
        # path_parent = os.path.dirname(os.getcwd())
        # os.chdir(path_parent)
        if "data" in model_path:
            self.trainer = TransformersNER("./"+model_path)
        else:
            self.trainer = TransformersNER(model_path)
        print("Loaded TNER ")

    def find_spans(self, doc: Doc) -> Iterable[Tuple[int, int, str]]:
        """Annotates one single document using the Spacy NER model"""
        print("Calling Prediction...")
        s = str(doc)
        s = self.trainer.predict([s])
        z = s[0]['entity']
        enti = {}
        json = []
        word = z[0]['mention']
        li = word.split()
        enti["entities"] = [((z[0]['position'][0], int(z[0]['position'][1]), z[0]['type']))]
        z = z[1:]
        for i in z:
            enti["entities"].append((i['position'][0], i['position'][1], i['type']))
        json.append([s[0]['sentence'], enti])   
        nlp = spacy.blank("en")
        db = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])
        for text, annotations in json:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            db.add(example.reference)
        dbb = db.to_bytes()
        nlp = spacy.blank("en")
        doc_bin = DocBin().from_bytes(dbb)
        doc2 = list(doc_bin.get_docs(nlp.vocab))[0]
        print("finished passing the model...")
        print("Entities in ann:",doc2.ents)

        # yield doc2
        for ent in doc2.ents:
            yield ent.start, ent.end, ent.label_

    def pipe(self, docs: Iterable[Doc]) -> Iterable[Doc]:
        """Annotates the stream of documents based on the Spacy model"""
        print("calling pipe..")
        # stream1, stream2 = itertools.tee(docs, 2)

        # # Remove existing entities from the document
        # stream2 = (self.create_new_doc(d) for d in stream2)
        
        # # And run the model
        # for _, proc in self.model.pipeline:
        #     stream2 = proc.pipe(stream2)
        new_docs = []
        docs1 = []
        s1, s2 = itertools.tee(docs, 2)
        # s1 = (self.create_new_doc(d) for d in s1)
        # for d in docs:
        #     print("INside loop")
        #     s = self.find_spans(d)
        #     yield s
        print("calling predictions")
        for d in s1:
            d = str(d)
            # print(d)
            docs1.append(self.trainer.predict([d]))
            # print(self.trainer.predict([d]))

        print("predictions done")
        # s = str(doc)
        # docs = self.trainer.predict(docs)
        for doc in docs1:
            # doc.spans[self.name] = []
            # Add the annotation
            # print("prediction:",doc)
            z = doc[0]['entity']
            enti = {}
            json = []
            word = z[0]['mention']
            li = word.split()
            enti["entities"] = [((z[0]['position'][0], int(z[0]['position'][1]), z[0]['type']))]
            z = z[1:]
            for i in z:
                enti["entities"].append((i['position'][0], i['position'][1], i['type']))
            json.append([doc[0]['sentence'], enti])
            nlp = spacy.blank("en")
            db = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])
            for text, annotations in json:
              # print()
              example = Example.from_dict(nlp.make_doc(text), annotations)
              db.add(example.reference)
            dbb = db.to_bytes()
            nlp = spacy.blank("en")
            doc_bin = DocBin().from_bytes(dbb)
            doc2 = list(doc_bin.get_docs(nlp.vocab))[0]
            new_docs.append(doc2)
        # print(new_docs[0].ents)
        # s2 = new_docs
        s2, s3 = itertools.tee(new_docs, 2)
        # for s in s2:
        #     s.ents = ""
        # print(new_docs[0].ents)
        print("Added Entities..")
        c = 0
        # for d in new_docs:
        #     print(d.ents)
        for doc, doc_copy in zip(s2, new_docs):

            doc.spans[self.name] = []
            # Add the annotation
            # print("Doc:",doc)
            # print("Doc_Copy:", doc_copy)
            # print("Doc number:",c)
            c = c + 1
            # print("copy ents:",doc_copy.ents)
            for ent in doc_copy.ents:
                # print(ent.start)
                # print(ent.label_)
                # print("doc:",doc)
                # print("doc_copy:",doc_copy)
               
                print(Span(doc, ent.start, ent.end, ent.label_))
                doc.spans[self.name].append(Span(doc, ent.start, ent.end, ent.label_))
            print("Entities:",doc.ents)
            print("NAME:",self.name)
            yield doc
        
        
    def create_new_doc(self, doc: Doc) -> Doc:
        """Create a new, empty Doc (but with the same tokenisation as before)"""

        return spacy.tokens.Doc(self.model.vocab, [tok.text for tok in doc], #type: ignore
                               [tok.whitespace_ for tok in doc])
class TruecaseAnnotator(ModelAnnotator):
    """Spacy model annotator that preprocess all texts to convert them to a 
    "truecased" representation (see below)"""

    def __init__(self, name:str, model_path:str, form_frequencies:str,
                 disabled:List[str]=["parser", "tagger", "lemmatizer", "attribute_ruler"]):
        """Creates a new annotator based on a Spacy model, and a dictionary containing
        the most common case forms for a given word (to be able to truecase the document)."""
        
        super(TruecaseAnnotator, self).__init__(name, model_path, disabled)
        with open(form_frequencies) as fd:
            self.form_frequencies = json.load(fd)

    def create_new_doc(self, doc: Doc, min_prob: float = 0.25) -> Doc:
        """Performs truecasing of the tokens in the spacy document. Based on relative 
        frequencies of word forms, tokens that 
        (1) are made of letters, with a first letter in uppercase
        (2) and are not sentence start
        (3) and have a relative frequency below min_prob
        ... will be replaced by its most likely case (such as lowercase). """

        if not self.form_frequencies:
            raise RuntimeError(
                "Cannot truecase without a dictionary of form frequencies")

        tokens = []
        spaces = []
        doctext = doc.text
        for tok in doc:
            toktext = tok.text

            # We only change casing for words in Title or UPPER
            if tok.is_alpha and toktext[0].isupper():
                cond1 = tok.is_upper and len(toktext) > 2  # word in uppercase
                cond2 = toktext[0].isupper(
                ) and not tok.is_sent_start  # titled word
                if cond1 or cond2:
                    token_lc = toktext.lower()
                    if token_lc in self.form_frequencies:
                        frequencies = self.form_frequencies[token_lc]
                        if frequencies.get(toktext, 0) < min_prob:
                            alternative = sorted(
                                frequencies.keys(), key=lambda x: frequencies[x])[-1]

                            # We do not change from Title to to UPPER
                            if not tok.is_title or not alternative.isupper():
                                toktext = alternative

            tokens.append(toktext)

            # Spacy needs to know whether the token is followed by a space
            if tok.i < len(doc)-1:
                spaces.append(doctext[tok.idx+len(tok)].isspace())
            else:
                spaces.append(False)

        # Creates a new document with the tokenised words and space information
        doc2 = Doc(self.model.vocab, words=tokens, spaces=spaces) #type: ignore
        return doc2


class LabelMapper(SpanAnnotator):
    """When using ModelAnnotators, e.g. spacy_lg models, often the
    labels introduced is not what one is looking for. This function takes in
    a dict of labels to replace and desired label to replace with, e.g. 
    {
        ('FAC','GPE'):"LOC",
        ('NORP'):"ORG",
        ('DATE','EVENT', ..., 'WORK_OF_ART'): "MISC"
    }
    """

    def __init__(
        self,
        name: str,
        mapping: Dict[Iterable[str], str],
        sources: Iterable[str],
        inplace: bool = True,
    ):
        """Creates a new annotator that looks at the labels of certain
        span groups (specified by 'sources') for each doc. If the label 
        is found in the mapping dictionary, it is replaced accordingly.
        If the inplace flag is active, the labels are modified in their
        respective span groups. If inactive, creates a new span group
        for all relabelled spans."""

        super().__init__(name)
        self.sources = sources
        self.inplace = inplace

        # populate mapping dict
        self.mapping = {}
        for k, v in mapping.items():
            if isinstance(k, str):
                self.mapping[k] = v
            else:
                for key in k:
                    self.mapping[key] = v


    def find_spans(self, doc: Doc) -> Iterable[Tuple[int, int, str]]:
        """Loops through the spans annotated by the other source and runs the
        editor function on it. Unique because it doesn't return spans but instead
        edits the span groups in place!"""

        for source in set(self.sources).intersection(doc.spans):
            
            new_group = []
            for span in doc.spans[source]:

                if span.label_ in self.mapping:

                    span = Span(
                        doc,
                        span.start,
                        span.end,
                        self.mapping.get(span.label_)
                    )

                if self.inplace:
                    new_group.append(span)
                else:
                    yield span.start, span.end, span.label_
                    
            if self.inplace:
                doc.spans[source] = new_group
