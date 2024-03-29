from typing import Iterable, Tuple
import re, json, os
import snips_nlu_parsers
from skweak.base import CombinedAnnotator, SpanAnnotator
from skweak.spacy import ModelAnnotator, TruecaseAnnotator
from skweak.heuristics import FunctionAnnotator, TokenConstraintAnnotator, SpanConstraintAnnotator, SpanEditorAnnotator
from skweak.gazetteers import GazetteerAnnotator, extract_json_data
from skweak.doclevel import DocumentHistoryAnnotator, DocumentMajorityAnnotator
from skweak.aggregation import MajorityVoter
from skweak import utils
from spacy.tokens import Doc, Span  # type: ignore
from examples.ner import data_utils

# Data files for gazetteers
# WIKIDATA = os.path.dirname(__file__) + "/../../data/wikidata_tokenised.json"
WIKIDATA_SMALL = "data/wikidata_small_tokenised.json"
COMPANY_NAMES = "data/company_names_tokenised.json"
GEONAMES = "data/geonames.json"
CRUNCHBASE = "data/crunchbase.json"
# PRODUCTS = os.path.dirname(__file__) + "/../../data/products.json"
FIRST_NAMES = "data/first_names.json"
# FORM_FREQUENCIES = os.path.dirname(__file__) + "/../../data/form_frequencies.json"


############################################
# Combination of all annotators
############################################


class NERAnnotator(CombinedAnnotator):
    """Annotator of entities in documents, combining several sub-annotators (such as gazetteers,
    spacy models etc.). To add all annotators currently implemented, call add_all(). """

    def add_all(self):
        """Adds all implemented annotation functions, models and filters"""

        print("Loading shallow functions")
        self.add_shallow()
        print("Loading Spacy NER models")
        self.add_models()
        print("Loading gazetteer supervision modules")
        self.add_gazetteers()
        print("Loading document-level supervision sources")
        self.add_doc_level()

        return self

    def add_shallow(self):

    	proper_detector = skweak.heuristics.TokenConstraintAnnotator("proper_detector", skweak.utils.is_likely_proper, "ENT")

    	nnp_detector = TokenConstraintAnnotator("nnp_detector", lambda tok: tok.tag_ in {"NNP", "NNPS"}, "ENT")

        # Detection based on dependency relations (compound phrases)
        compound = lambda tok: utils.is_likely_proper(tok) and utils.in_compound(tok)
        compound_detector = TokenConstraintAnnotator("compound_detector", compound, "ENT")

        for annotator in [proper_detector, proper2_detector, nnp_detector, compound_detector]:
            annotator.add_incompatible_sources(exclusives)
            annotator.add_gap_tokens(["'s", "-"])
            self.add_annotator(annotator)

            # We add one variants for each NE detector, looking at infrequent tokens
            infrequent_name = "infrequent_%s" % annotator.name
            self.add_annotator(SpanConstraintAnnotator(infrequent_name, annotator.name, utils.is_infrequent))
    
		
		full_name_detector = SpanConstraintAnnotator("full_name_detector", "proper_detector",
                                                     FullNameDetector(), "PERSON")

		company_detector = skweak.heuristics.FunctionAnnotator("company_detector", company_detector_fun)

		other_org_detector = skweak.heuristics.FunctionAnnotator("other_org_detector", other_org_detector_fun)

		misc_detector = FunctionAnnotator("misc_detector", misc_generator)

     	return self

    def add_gazetteers(self, full_load=True):


    	company_tries = extract_json_data(COMPANY_NAMES) 
        
        wiki_small_tries = extract_json_data(WIKIDATA_SMALL)

        geo_tries = extract_json_data(GEONAMES)

        for name, tries in {"wiki_small":wiki_small_tries,
                            "geo":geo_tries, "company":company_tries}.items():
            
            # For each KB, we create two gazetters (case-sensitive or not)
            cased_gazetteer = GazetteerAnnotator("%s_cased"%name, tries, case_sensitive=True)
            uncased_gazetteer = GazetteerAnnotator("%s_uncased"%name, tries, case_sensitive=False)
            cased_gazetteer.add_incompatible_sources(exclusives)
            uncased_gazetteer.add_incompatible_sources(exclusives)
            self.add_annotators(cased_gazetteer, uncased_gazetteer)
                
            # We also add new sources for multitoken entities (which have higher confidence)
            multitoken_cased = SpanConstraintAnnotator("multitoken_%s"%(cased_gazetteer.name), 
                                                       cased_gazetteer.name, lambda s: len(s) > 1)
            multitoken_uncased = SpanConstraintAnnotator("multitoken_%s"%(uncased_gazetteer.name), 
                                                         uncased_gazetteer.name, lambda s: len(s) > 1)
            self.add_annotators(multitoken_cased, multitoken_uncased)
                
        return self

	def add_doc_level(self):
	        """Adds document-level supervision sources"""

        self.add_annotator(Standardiser())

        maj_voter = MajorityVoter("doclevel_voter", ["LOC", "MISC", "ORG", "PER"], 
                                  initial_weights={"doc_history":0, "doc_majority":0})
        maj_voter.add_underspecified_label("ENT", {"LOC", "MISC", "ORG", "PER"})     
        self.add_annotator(maj_voter)   
           
        self.add_annotator(DocumentHistoryAnnotator("doc_history_cased", "doclevel_voter", ["PER", "ORG"]))
        self.add_annotator(DocumentHistoryAnnotator("doc_history_uncased", "doclevel_voter", ["PER", "ORG"],
                                                    case_sentitive=False))
        
        maj_voter = MajorityVoter("doclevel_voter", ["LOC", "MISC", "ORG", "PER"],
                                  initial_weights={"doc_majority":0})
        maj_voter.add_underspecified_label("ENT", {"LOC", "MISC", "ORG", "PER"})
        self.add_annotator(maj_voter)

        self.add_annotator(DocumentMajorityAnnotator("doc_majority_cased", "doclevel_voter"))
        self.add_annotator(DocumentMajorityAnnotator("doc_majority_uncased", "doclevel_voter", 
                                                     case_sensitive=False))
        return self

    def add_models(self):

        self.add_annotator(ModelAnnotator("core_web_md", "en_core_web_md"))
        self.add_annotator(TruecaseAnnotator("core_web_md_truecase", "en_core_web_md", FORM_FREQUENCIES))
       
		editor = lambda span: span[1:] if span[0].lemma_ in {"the", "a", "an"} else span
		self.add_annotator(SpanEditorAnnotator("edited_core_web_md", "core_web_md", editor))
        self.add_annotator(SpanEditorAnnotator("edited_core_web_md_truecase", "core_web_md_truecase", editor))
      	
    	return self 

    OTHER_ORG_CUE_WORDS = {"University", "Institute", "College", "Committee", "Party", "Agency",
                       "Union", "Association", "Organization", "Court", "Office", "National"}
	def other_org_detector_fun(doc):
	    for chunk in doc.noun_chunks:
	        if any([tok.text in OTHER_ORG_CUE_WORDS for tok in chunk]):
	            yield chunk.start, chunk.end, "ORG"

    def company_detector_fun(doc):
    for chunk in doc.noun_chunks:
        if chunk[-1].lower_.rstrip(".") in {'corp', 'inc', 'ltd', 'llc', 'sa', 'ag'}:
            yield chunk.start, chunk.end, "COMPANY"

    def misc_generator(doc):
    """Detects occurrences of countries and various less-common entities (NORP, FAC, EVENT, LANG)"""
    
    spans = set(doc.spans["proper_detector"])
    spans |= {doc[i:i+1] for i in range(len(doc))}
    
    for span in sorted(spans):

        span_text = span.text
        if span_text.isupper():
            span_text = span_text.title()
        last_token = doc[span.end-1].text

        if span_text in data_utils.COUNTRIES:
            yield span.start, span.end, "GPE"

        if len(span) <= 3 and (span in data_utils.NORPS or last_token in data_utils.NORPS 
                               or last_token.rstrip("s") in data_utils.NORPS):
            yield span.start, span.end, "NORP"
    
        if span in data_utils.LANGUAGES and doc[span.start].tag_=="NNP":
            yield span.start, span.end, "LANGUAGE"
            
        if last_token in data_utils.FACILITIES and len(span) > 1:
            yield span.start, span.end, "FAC"     

        if last_token in data_utils.EVENTS  and len(span) > 1:
            yield span.start, span.end, "EVENT"   

    class Standardiser(SpanAnnotator):
    """Annotator taking existing annotations and standardising them
    to fit the ConLL 2003 tag scheme"""

    def __init__(self):
        super(Standardiser, self).__init__("")

    def __call__(self, doc):
        """Annotates one single document"""     
               
        for source in doc.spans:
               
            new_spans = []  
            for span in doc.spans[source]:
                if "\n" in span.text:
                    continue
                elif span.label_=="person":
                    new_spans.append(Span(doc, span.start, span.end, label="PER"))
                elif span.label_ in {"ORGANIZATION", "ORGANISATION", "COMPANY", "corporation"}:
                    new_spans.append(Span(doc, span.start, span.end, label="ORG"))
                elif span.label_ in {"location"}:
                    new_spans.append(Span(doc, span.start, span.end, label="LOC"))
                elif span.label_ in {"EVENT", "FAC", "LANGUAGE", "LAW", "NORP", "PRODUCT", "WORK_OF_ART", "creative-work", "group", "product"}:
                    new_spans.append(Span(doc, span.start, span.end, label="MISC"))
                else:
                    new_spans.append(span)         
            doc.spans[source] = new_spans      
        return doc