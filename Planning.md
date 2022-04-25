

**Task 1: Understanding NER**
(2-3 weeks weeks? - May 2022)
- Understand the problem and typical approaches followed 
- Learn to use a few existing NLP libraries   
    1. with off the shelf models (e.g., spacy, flair, stanza, huggingface)  
- identify some problem areas based on evaluation and observation (e.g., sensitivity to certain kinds of inputs, not doing well for some NE tags compared to others etc)
- exercise: Understand how to *train* a NER model, taking a standard dataset and using Spacy or such existing library to train.    

**Task 2: Understanding various topics in NER context** 
(2-3 weeks? -May 2022)  
- weak supervision (familiarity with libraries such as: skweak, knodle, flying squid, astra)  
- domain adaptation, few short learning  
- prompt based learning
- exercise: how can you create more examples to identify NORP (see description in Onotonotes dataset guidelines) in CONLL-03 NER corpus (it doesn't have that category annotated specifically). 

**Task 3: Multilingual NER exercise**  
(2 weeks? - June 1-15 2022)  
- Fine-tuning a BERT model for multiple languages and comparing   
- goal: to familiarize with the training, tuning, comparisons process  
- can use multiconer dataset or anyother.  
-libraries that support training and fine-tuning language models for NER such as [tner](https://github.com/asahi417/tner) , [NERDA](https://github.com/ebanalyse/NERDA/tree/main/src/NERDA), [ACE](https://github.com/Alibaba-NLP/ACE), Flair, Spacy etc  
- Exercise: training a multilingual ner model?

**Task 4: Experiments with improving modeling process**  
- Exploring methods to get better at predicting NE tags that are under-represented in the training set
- Learning the context instead of memorization
- Adopting NER to other scenarios: same tag set, new domain; slightly different tag set, new domain
- WeakSupervision 
(June, July 2022)

**Task 5: Concluding the project**  
Final round of experiments, Wrap up, report writing and code cleanup  
(August 2022)






