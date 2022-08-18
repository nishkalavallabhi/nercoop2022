from more_itertools import windowed
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast
import numpy as np
from transformers import DistilBertForTokenClassification
from transformers import DistilBertForTokenClassification, Trainer, TrainingArguments
import torch
import evaluate
from seqeval.metrics import f1_score, precision_score, recall_score, classification_report



def get_conll_data(filepath, sep="\t", allow_long_sentences=False, test=False) -> dict:
    """Load CoNLL-2003 (English) data split.
    Returns:
        dict: Dictionary with word-tokenized 'sentences' and named
        entity 'tags' in IOB format.
    """
    # set to default directory if nothing else has been provided by user.
    # read data from file.
    fh = open(filepath, encoding="utf-8")
    threshold = 100
    steps = 99
    sentences = []
    tags = []
    tempsen = []
    tempnet = []
    for line in fh:
        if len(line)>1 and  not line.startswith("# id"):
            splits = line.strip().split(sep)
            if len(splits) > 1:
                tempsen.append(splits[0].strip())
                tempnet.append(splits[-1].strip())
        else:
            if tempsen and tempnet:
              if allow_long_sentences:
                if len(tempsen) > threshold:
                    moresens = [list(filter(None,list(item))) for item in list(windowed(tempsen, n=threshold, step=steps))]
                    if test:
                        morenets = [[] for item in list(windowed(tempnet, n=threshold, step=steps))]
                    else:
                        morenets = [list(filter(None, list(item))) for item in list(windowed(tempnet, n=threshold, step=steps))]
                    sentences.extend(moresens)
                    tags.extend(morenets)
              else:
                sentences.append(tempsen)
                if test:
                    tags.append([])
                else:
                    tags.append(tempnet)
              tempsen = []
              tempnet = []
    fh.close()
    return {'sentences': sentences, 'tags': tags}


def encode_tags(tags, encodings):
    labels = [[tag2id[tag] for tag in doc] for doc in tags]
    encoded_labels = []
    for doc_labels, doc_offset in zip(labels, encodings.offset_mapping):
        # create an empty array of -100
        doc_enc_labels = np.ones(len(doc_offset),dtype=int) * -100
        arr_offset = np.array(doc_offset)

        # set labels whose first offset position is 0 and the second is not 0
        doc_enc_labels[(arr_offset[:,0] == 0) & (arr_offset[:,1] != 0)] = doc_labels
        encoded_labels.append(doc_enc_labels.tolist())

    return encoded_labels


class NERDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)



def compute_metrics(p):
    metric = evaluate.load("seqeval")
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    # Remove ignored index (special tokens)
    true_predictions = [
        [list(unique_tags)[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [list(unique_tags)[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    final_results = {}
    for key, value in results.items():
        if isinstance(value, dict):
            for n, v in value.items():
                final_results[f"{key}_{n}"] = v
        else:
            final_results[key] = value
    return final_results


if __name__ == "__main__":

    data = get_conll_data("wiesp/wiesp_train.conll", allow_long_sentences=True) #Enter path of train data in conll format
    texts = data['sentences']
    tags = data['tags']
    unique_tags = set(tag for doc in tags for tag in doc)
    tag2id = {tag: id for id, tag in enumerate(unique_tags)}
    id2tag = {id: tag for tag, id in tag2id.items()}

    train_texts, val_texts, train_tags, val_tags = train_test_split(texts, tags, test_size=.2)

    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased')
    train_encodings = tokenizer(train_texts, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)
    val_encodings = tokenizer(val_texts, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)
    # test_encodings = tokenizer(test_texts, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)

    train_labels = encode_tags(train_tags, train_encodings)
    val_labels = encode_tags(val_tags, val_encodings)
    # test_labels = encode_tags(test_tags, test_encodings)

    train_encodings.pop("offset_mapping") # we don't want to pass this to the model
    val_encodings.pop("offset_mapping")

    train_dataset = NERDataset(train_encodings, train_labels)
    val_dataset = NERDataset(val_encodings, val_labels)

   

    model = DistilBertForTokenClassification.from_pretrained('distilbert-base-cased', num_labels=len(unique_tags))


    training_args = TrainingArguments(
        output_dir='hugging_face/resultsx',          # output directory
        num_train_epochs=5,              # total number of training epochs
        per_device_train_batch_size=16,  # batch size per device during training
        per_device_eval_batch_size=64,   # batch size for evaluation
        warmup_steps=500,                # number of warmup steps for learning rate scheduler
        weight_decay=0.01,               # strength of weight decay
        logging_dir='hugging_face/logs1',            # directory for storing logs
        logging_steps=10,
    )


    trainer = Trainer(
        model=model,                         # the instantiated 🤗 Transformers model to be trained
        args=training_args,                  # training arguments, defined above
        train_dataset=train_dataset,         # training dataset
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics             # evaluation dataset
    )

    trainer.train()
    checkpoint_path = "hugging_face/wiesp_checkpoint"
    trainer.save_model(checkpoint_path)

    metrics = trainer.evaluate()
    print(metrics)