
**Task 0: General overview:**
(1-2 weeks. May 2022)
Reading on  
- sequence labeling  
- transfer learning: pre-train + fine-tune paradigm  (huggingface course)
- prompt based learning    
- data augmentation  
- adversarial inputs  
- few-shot learning etc  
(Some relevant readings are listed in Readings.md under "General Overview".)

**Task 1: Understanding NER**
(2 weeks - May 2022)
- Understand NER problem and typical approaches followed 
- Learn to use a few existing NLP libraries with off the shelf NER models (e.g., spacy, flair, stanza, huggingface, tner)  
- identify some problem areas based on evaluation and observation (e.g., sensitivity to certain kinds of inputs, not doing well for some NE tags compared to others etc)
- exercise: Understand how to *train* a NER model, taking a standard dataset and using Spacy or such existing library to train.    
("NER overview" section in Readings.md will be useful here)

**Task 2: Understanding various topics in NER context** 
(1-2 weeks -May 2022)  
- weak supervision (familiarity with libraries such as: skweak, knodle, flying squid, astra)  
- domain adaptation, few short learning  
- prompt based learning
- exercise: how can you create more examples to identify NORP (see description in Onotonotes dataset guidelines) in CONLL-03 NER corpus (it doesn't have that category annotated specifically). 

**Task 3: Multilingual NER exercise**  
(1 week - June 2022)  
- Fine-tuning a BERT model for multiple languages and comparing (multiconer dataset?)   
- goal: to familiarize with the training, tuning, comparisons process  
- can use multiconer dataset or anyother.  
-libraries that support training and fine-tuning language models for NER such as [tner](https://github.com/asahi417/tner) , [NERDA](https://github.com/ebanalyse/NERDA/tree/main/src/NERDA), [ACE](https://github.com/Alibaba-NLP/ACE), Flair, Spacy etc  
- Exercise: training a multilingual ner model?

**Task 4: Experiments with improving modeling process**
(June and July 2022)
Some ideas to choose from:  
- Learning the context instead of memorization  
- Explore Multilingual NER
- WeakSupervision 
- Exploring methods to get better at predicting NE tags that are under-represented in the training set (see Fewshot NER, SOTA NER sections for related readings)  
- Adopting NER to other scenarios: same tag set, new domain; slightly different tag set, new domain 
(I am currently interested in 1--3 above, but we can look at new ideas that come up in the first two months).

**Task 5: Concluding the project**  
Final round of experiments, Wrap up, report writing and code cleanup  
(August 2022)






