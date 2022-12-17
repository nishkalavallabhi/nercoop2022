from NERDA.models import NERDA
from NERDA.datasets import *
# from .preprocessing import create_dataloader
import sys
import argparse
import pprint


def main(args):

    #multiconer_tags = ['B-PER','I-PER', 'B-PROD', 'I-PROD', 'B-GRP', 'I-GRP', 'B-CW', 'I-CW','B-CORP', 'I-CORP','B-LOC', 'I-LOC']
    conll_tags = ['B-PER','I-PER','B-ORG','I-ORG','B-LOC', 'I-LOC', 'B-MISC', 'I-MISC']
    
    # sep = " "

    transformer = "bert-base-multilingual-uncased"
    print("training data path:",args.train_file)
    
    hyper = {'epochs' : int(args.epochs), 'warmup_steps' : 500, 'train_batch_size': 8, 'fixed_seed': int(args.seed), 'learning_rate': 0.00001}
    # print("Testing get_conll():",get_conll_data(args.train_file, sep).get('sentences'))
# dl_train = create_dataloader(sentences = get_conll_data(args.train_file).get('sentences'),
#                                  tags = get_conll_data(args.train_file).get('tags'), 
#                                  transformer_tokenizer = transformer_tokenizer, 
#                                  transformer_config = transformer_config,
#                                  max_len = max_len, 
#                                  batch_size = train_batch_size, 
#                                  tag_encoder = tag_encoder,
#                                  tag_outside = tag_outside,
#                                  num_workers = num_workers)
    sep = " "
    data = get_conll_data(args.train_file, sep)
    print("Output of get_conll_data():",len(data.get('sentences')))
    
    model = NERDA(dataset_training = get_conll_data(args.train_file, prefix='train', prop = float(args.prop)),
              dataset_validation = get_conll_data(args.dev_file),
              tag_scheme=conll_tags, transformer = transformer, max_len=512, hyperparameters = hyper)
    model.load_network_from_file("x_lingual/mbert_es_nl_deu.bin")
    print(str(model.transformer))
    print("Length of sampled train data:", len(get_conll_data(args.train_file).get('sentences')))
    print("Random seed:",args.seed)
    model.train()

    if args.load_model is not None:
        model.load_network_from_file(args.load_model)
        print("Loading model...")

    if args.save_model is not None:
        model.save_network(args.save_model)
        print("Saved the model")

    print("Testing on the labeled test set")
    test = get_conll_data(args.test_file)
    results, tags_true, tags_predicted = model.evaluate_performance(test)
    print(results)

    """
    padded = 0
    for i in range(0, len(test_tokens)):
        if len(test_tokens[i]) != len(tags_predicted[i]):
            #pad the predictions with 'O'
            tags_predicted[i] = tags_predicted[i] + ['O']*(len(test_tokens[i])-len(tags_predicted[i]))
    """
    # if args.save_preds is not None:
    #     save_preds(args.test_file, args.save_preds, tags_predicted)    

    print("DONE")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", help="Path for the training file in conll format", required=True)
    parser.add_argument("--dev_file", help="Path for the dev file with preds, in conll format", required=True)
    parser.add_argument("--test_file", help="Path for validation file without true values, in conll format", required=True) 
    parser.add_argument("--seed", help="Random Seed, if needed", default=None)
    parser.add_argument("--save_model", help="Path to save the model, if needed", default=None)
    parser.add_argument("--load_model", help="Path to load the model from, if needed", default=None)

    parser.add_argument("--epochs", help="Number of Epochs, if needed", default=None)
    parser.add_argument("--prop", help="Proportion of train data, if needed", default=None)
    args=parser.parse_args()
    main(args)
