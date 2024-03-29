

What do we know so far about Adversarial inputs for NER 

What are some simple, existing methods to generate adversarial test sets for NER?
  
- Using existing gazetteers and lists for replacement. 
    - Faker (Vajjala and Balasubramaniam, 2022). 
    - Country specific lists (Agarwal et.al, 2020. https://arxiv.org/pdf/2004.04123.pdf - Entity Switched Datasets paper). 
    - Sampling, gazetteers, random replacement (Yan et.al., 2022. https://aclanthology.org/2022.naacl-main.37.pdf. They probably used a random sampling method like us, but for MRC, not NER). 
    - RockNER (using entity linking to choose the appropriate entities) Lin et.al., https://aclanthology.org/2021.emnlp-main.302.pdf. 

- Changing the context a little bit
   - using a masked language model (in RockNER paper). 
   
What we do:
- Random sampling and replacement within the test set (as a strong baseline). 
- Using faker for PER/LOC
- Masking with LMs   
- Paraphrasing with quillbot (manually)
- Random sampling + masking

Test datasets:   
English: conll-03, wnut, multiconer 
German: conll-03, multiconer. 
Hindi: multiconer

NER methods to compare original and modified test sets: generic BERT fine tuning approach, dataset specific pre-existing models:  
CONLL-03 EN/DE: Stanza, Flair, tner 
WNUT: tner 
Multiconer-EN: tner
Multiconer-HI: tner?

If everything is setup and running smoothly, we can look into one or two other languages later on (say Hindi - multiconer)

Other relevant papers: Robustness Gym https://aclanthology.org/2021.naacl-demos.6.pdf. 

Paper structure:
- describing the implemented methods to generate adversarial input. 
- testing with multiple datasets. 
- probably pick a dataset or two and do more analysis on the performance (e.g., using nervaluate or looking more in detail into individual categories). 
- summarize conclusions. 
