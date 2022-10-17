**General Overview**
-  [Sequence Labeling chapter](https://web.stanford.edu/~jurafsky/slp3/8.pdf) in Jurafsky and Martin textbook  
- [Transfer learning in NLP](https://aclanthology.org/N19-5004/), NAACL 2019 Tutorial  
- [Domain Adaptation survey](https://aclanthology.org/2020.coling-main.603.pdf), COLING 2020  
- [A Survey of Data Augmentation Approaches for NLP](https://aclanthology.org/2021.findings-acl.84.pdf), ACL Findings, 2021  
- [Prompt based learning](https://arxiv.org/abs/2107.13586) - a survey of prompt based learning paradigm in NLP  
- [A Survey in Adversarial Defences and Robustness in NLP](https://arxiv.org/abs/2203.06414)  
- [Weak supervision](https://www.snorkel.org/blog/weak-supervision), a general overview on Snorkel blog.   
- [Few shot learning](https://analyticsindiamag.com/an-introductory-guide-to-few-shot-learning-for-beginners/) - an overview blog post. [a listing of papers on the topic](https://github.com/zhjohnchan/awesome-few-shot-learning-in-nlp#survey)
- [Huggingface Course](https://huggingface.co/course/chapter1/1)  
- [A Primer on Pretrained Multilingual Language Models](https://arxiv.org/abs/2107.00676), ArXiv, 2021.  

**NER: Overview of main approaches:**    
- [Named Entity Recognition: A Literature Survey](https://www.cfilt.iitb.ac.in/resources/surveys/rahul-ner-survey.pdf), 2014 Technical report.   
- [A Survey on Recent Advances in Named Entity Recognition from Deep Learning models](https://arxiv.org/pdf/1910.11470.pdf), COLING 2018  
- [SpanNER: Named Entity Re-/Recognition as Span Prediction](https://aclanthology.org/2021.acl-long.558/), ACL 2021. [Code](https://github.com/neulab/SpanNER)  
- [Named Entity Recognition without Labelled Data: A Weak Supervision Approach](https://aclanthology.org/2020.acl-main.139/), ACL 2020  [Code](https://github.com/NorskRegnesentral/skweak)   

**NER Datasets**
- [from nlpprogress.com](http://nlpprogress.com/english/named_entity_recognition.html)  
- [multiconer shared task datasets](https://multiconer.github.io/)
- [HIPE 2022 shared task datasets](https://github.com/hipe-eval/HIPE-2022-data)

(several of these papers below share their code repo - I am not adding them - we can always look for them if needed. There is no guarantee the code works, though)  
**NER in various low resource settings**  
[Few-NERD: A Few-Shot Named Entity Recognition Dataset](https://arxiv.org/abs/2105.07464), ACL 2021    
[DoCoGen: Domain Counterfactual Generation for Low Resource Domain Adaptation](https://arxiv.org/abs/2202.12350), ACL 2022
[code](https://github.com/nitaytech/DoCoGen)     
[Few-shot Named Entity Recognition with Self-describing Networks](https://arxiv.org/abs/2203.12252), ACL 2022   
[CONTaiNER: Few-Shot Named Entity Recognition via Contrastive Learning](https://arxiv.org/abs/2109.07589), ACL 2022  
[Good Examples Make A Faster Learner: Simple Demonstration-based Learning for Low-resource NER](https://arxiv.org/abs/2110.08454), ACL 2022  
[MELM: Data Augmentation with Masked Entity Language Modeling for Low-Resource NER](https://arxiv.org/abs/2108.13655), ACL 2022    
[Label Semantics for Few Shot Named Entity Recognition](https://arxiv.org/abs/2203.08985), Findings of ACL 2022. 
[Automatic Creation of Named Entity Recognition Datasets by Querying Phrase Representations](https://arxiv.org/abs/2210.07586), ArXiv, Oct 2022.   

**Data Augmentation, Adversarial inputs, and other ways of transforming NER datasets**  
[SeqMix: Augmenting Active Sequence Labeling via Sequence Mixup](https://rongzhizhang.org/pdf/emnlp20_SeqMix.pdf), EMNLP 2020    
[Counterfactual Generator: A Weakly-Supervised Method for Named Entity Recognition](https://aclanthology.org/2020.emnlp-main.590/), EMNLP 2020    
[A Rigorous Study on Named Entity Recognition: Can Fine-tuning Pretrained Model Lead to the Promised Land?](https://aclanthology.org/2020.emnlp-main.592.pdf), EMNLP 2020  
[Entity-Switched Datasets: An Approach to Auditing the In-Domain Robustness of Named Entity Recognition Models](https://arxiv.org/abs/2004.04123), ArXiv, 2020  
[RockNER: A Simple Method to Create Adversarial Examples for Evaluating the Robustness of Named Entity Recognition Models](https://aclanthology.org/2021.emnlp-main.302/), EMNLP 2021      
[What do we really know about State of the Art NER?](), LREC 2022    
[Leveraging Expert Guided Adversarial Augmentation For Improving Generalization in Named Entity Recognition](https://arxiv.org/abs/2203.10693), Findings of ACL 2022.  

**other SOTA NER**  
[Interpretability Analysis for Named Entity Recognition to Understand System Predictions and How They Can Improve](https://aclanthology.org/2021.cl-1.5/), CL 2021   
[Partially Supervised Named Entity Recognition via the Expected Entity Ratio Loss](https://transacl.org/ojs/index.php/tacl/article/view/2981), TACL 2021.   
[Context-aware adversarial training for name regularity bias in named entity recognition](https://aclanthology.org/2021.tacl-1.36/), TACL 2021.  
[kNN-NER: Named Entity Recognition with Nearest Neighbor Search](https://arxiv.org/abs/2203.17103), ArXiv, 2022  
[Parallel Instance Query Network for Named Entity Recognition](https://arxiv.org/abs/2203.10545), to appear in ACL 2022  
[A Unified MRC Framework for Named Entity Recognition](https://aclanthology.org/2020.acl-main.519.pdf), ACL 2020  
[MINER: Improving Out-of-Vocabulary Named Entity Recognition from an Information Theoretic Perspective](https://arxiv.org/abs/2204.04391), ACL 2022   

**Multi/Cross-lingual NER**    
[An Unsupervised Multiple-Task and Multiple-Teacher Model for Cross-lingual Named Entity Recognition](), ACL 2022.  
[Composable Sparse Fine-Tuning for Cross-Lingual Transfer](https://arxiv.org/abs/2110.07560), ACL 2022. [Code](https://github.com/cambridgeltl/composable-sft)    
[Language-Family Adapters for Multilingual Neural Machine Translation](https://arxiv.org/abs/2209.15236), ArXiv, Sep 2022.  
[Lifting the Curse of Multilinguality by Pre-training Modular Transformers](https://aclanthology.org/2022.naacl-main.255.pdf), NAACL 2022.  
[Sources of Transfer in Multilingual Named Entity Recognition](https://aclanthology.org/2020.acl-main.720) (Mueller et al., ACL 2020).  
[Unsupervised cross-lingual model transfer for named entity recognition with contextualized word representations](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0257230), PLoS One, 2021.  
[Language Contamination Helps Explain the Cross-lingual Capabilities of English Pretrained Models](https://arxiv.org/abs/2204.08110), EMNLP 2022.  
[Zero-Resource Cross-Lingual Named Entity Recognition](https://ojs.aaai.org/index.php/AAAI/article/view/6237), AAAI 2020.  

Others:
[SpanNER](https://github.com/neulab/SpanNER). 
[SpanBERT](https://github.com/facebookresearch/SpanBERT). 
[ByT5](https://github.com/google-research/byt5). 
[SetFit](https://huggingface.co/blog/setfit). 

