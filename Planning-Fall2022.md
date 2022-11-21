
until 31st August: WIESP Shared task, report writing etc.  

Sep: Wrapping up adversarial testing, may be do adversarial fine-tuning experiments, writing up and submitting the paper to ACL Rolling Review.  

End of Sep, 1st week of Oct: Reading on cross-lingual transfer.  

Oct-Nov: explore cross-lingual transfer approaches for NER.  
(few shot or zero shot. Goal: how can we reuse NER model trained on one language on another language). 

***********

Notes on 17 Oct 2022:  
- Following approaches in [Sources of Transfer in Multilingual Named Entity Recognition](https://aclanthology.org/2020.acl-main.720) (Mueller et al., ACL 2020)
 and [Unsupervised cross-lingual model transfer for named entity recognition with contextualized word representations](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0257230) (Yan et.al, Plos One, 2021) 
 with the [CONLL-2002 (Spanish, Dutch)](https://huggingface.co/datasets/conll2002) and [CONLL-2003 (English, German)](https://huggingface.co/datasets/conll2003) NER datasets
 
 (comparing monolingual models with multilingual models and multilingual+fine-tuned to a language models, zero-shot transfer with models trained on 1-n
  source languages, exploring adapter approaches (e.g., one large transformer model +adapters for each language NER) etc.  

- Extend the experiments to multiconer dataset.    

- Explore other architectures for NER (using transformer model embeddings as just initial step).   

- Check if using pre-trained modular transformers ([Pfeiffer et.al., NAACL 2022](https://aclanthology.org/2022.naacl-main.255.pdf)) + fine-tuning on NER task is any better than using regular pre-trained models+fine-tuning or pre-trained models+adapters  

- [SpanNER](https://github.com/neulab/SpanNER), [SpanBERT](https://github.com/facebookresearch/SpanBERT) approaches - will they be useful?   
 
***********

Notes on 25th october 2022:  
- Check on the ensemble implementations in SpanNER and [Hassan et.al., Multcioner shared task paper, 2022](https://aclanthology.org/2022.semeval-1.218/). 
- explore [Xformers](https://github.com/facebookresearch/xformers), and whether it is relevant?   
- How to follow an ensembling approach in this situation:  
    * Multiple full NER models   
    * NER models trained on slices of data grouped by some criterion?  (e.g., difficult slices (what is difficulty?), per category slices etc). 
************

Notes on 26th October 2022:
I spent sometime thinking about what models you should train and experiment on. Here is what I am thinking right now: replicate the Mueller et.al. (2020) paper’s models (i.e., word CRF, char CRF, byte to span, mbert+finetune), and add a bunch of pre-trained language models trained with word/subword/character tokenizations (mbert, xlnet, may be one more multilingual model, and tokenizer free ones (byt5, any other) - for these, you can look at both full fine tuning as well as adapters. Finally: modular transformers (NAACL 2022 paper Pfeiffer et.al) and SpanNER approaches too.  Everything in monolingual, multilingual, zero shot, and multilingual+language specific finetuning setups. - Lot of experiments to do, but most of this is straight forward…. We are primarily looking at stringing together existing implementations, and not re-inventing anything from scratch.

************. 

Notes on 21st November 2022:
<img width="655" alt="Screen Shot 2022-11-21 at 9 59 16 AM" src="https://user-images.githubusercontent.com/7221440/203087359-9f954bb2-7385-4cb4-91c3-ad933b7e4a09.png">

*********

Dec: Wrapping up, writing up a report.  
