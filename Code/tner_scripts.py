
#FINE-TUNING
from tner import TrainTransformersNER
trainer = TrainTransformersNER(
        checkpoint_dir='data/checkpoint_0',
        dataset='data/mconer_train',
        transformers_model='tner/tner-xlm-roberta-large-uncased-wnut2017',  
        random_seed=1234,
        lr=1e-5,
        total_step=1000,
        warmup_step=10,
        batch_size=16,
        max_seq_length=128)
trainer.train()

#EVALUATION 
#Replace the path in transformers_model with a checkpoint path to load a fine-tuned model locally
from tner import TrainTransformersNER
trainer = TrainTransformersNER(checkpoint_dir='data/checkpoint_w', transformers_model="tner/tner-xlm-roberta-large-uncased-wnut2017", batch_size=16)
trainer.test('data/mconer_train', batch_size_validation=1)

#CALLING PREDICTIONS
from pprint import pprint
trainer = TransformersNER(transformers_model="tner/tner-xlm-roberta-large-uncased-wnut2017")

test_sentences = [
    'I live in United States, but Leonardo Da Vinci painted Mona Lisa and asked me to move to Japan.',
    "I'm watching Cars movie on an Apple computer.",
    'I like to eat an apple.'
]
prediction = trainer.predict(test_sentences)
pprint(prediction)