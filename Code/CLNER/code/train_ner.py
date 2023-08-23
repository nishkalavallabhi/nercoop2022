from datasets import load_dataset
from transformers import AutoTokenizer

wnut = load_dataset("wnut_17")
label_list = wnut["train"].features[f"ner_tags"].feature.names
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

