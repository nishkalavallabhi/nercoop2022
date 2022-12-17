# encoding: utf-8


import os
from pytorch_lightning import Trainer
import yaml
from pathlib import Path
from yaml.loader import Loader

# from trainer_spanPred import BertLabeling # old evaluation version
# from trainer_spanPred_newEval import BertLabeling # new evaluation version
from trainer import BertNerTagger # start 0111
def evaluate(ckpt, hparams_file):
	"""main"""

	
	# trainer = Trainer(distributed_backend="dp")
	args = yaml.load(Path(hparams_file).read_text(), Loader=Loader)
	args['data_dir'] = 'data/conll_en'
	args['proportion'] = 1.0
	with open("hparams_file.yml", 'w') as outfile:
    	   yaml.dump(args, outfile, default_flow_style=False)
	model = BertNerTagger.load_from_checkpoint(
		checkpoint_path=ckpt,
		hparams_file="hparams_file.yml",
		map_location=None,
		batch_size=1,
		max_length=128,
		#workers=0
	)
	print("0 % TRAIN DATA")
	test_dataloader = BertNerTagger(args).get_dataloader("test")
	trainer = Trainer(gpus=[0], distributed_backend="dp")
	trainer.test(model=model, test_dataloaders=test_dataloader)


if __name__ == '__main__':

	root_dir1 = "output/train_logs"

	# datas = ['notenw','notewb','notebc','notemz','notetc','notebn','conll02dutch'] #
	# # datas = ['conll02spanish']  #
	# datas = ['wnut17']  #
	# for data in datas:
	# 	root_dir = os.path.join(root_dir1, data)
	# 	files = os.listdir(root_dir)
	# 	for file in files:
	# 		print('file:',file)
	# 		if "spanPred_bert" in file:
	# 			fmodel = os.path.join(root_dir,file)
	# 			fnames = os.listdir(fmodel)
	# 			ckmodel = ''
	# 			for fname in fnames:
	# 				if '.ckpt' in fname:
	# 					ckmodel= fname
	# 			CHECKPOINTS= os.path.join(fmodel,ckmodel)
	# 			HPARAMS = fmodel+"/lightning_logs/version_0/hparams.yaml"
	# 			evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)





	# # 0125
	# # conll03 bert-large, 9245 evaluation
	# midpath = "conll03/spanPred_bert-large-uncased_prunTrue_spLenTrue_spMorphFalse_SpWtFalse_value1_25149666_9245"
	# model_names = ["epoch=18.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ",mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" +mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# # 0125
	# # conll03 bert-large, 9245 evaluation
	# midpath = "wnut16/spanPred_bert-large-uncased_prunTrue_spLenFalse_spMorphFalse_SpWtFalse_value1_12635765"
	# model_names = ["epoch=11.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ",mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" +mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# 0129
	# # conll03 bert-large, 9252 evaluation
	# midpath = "conll03/spanPred_dev2train_bert-large-uncased_maxSpan4prunFalse_spLenTrue_spMorphFalse_SpWtFalse_value1_35462812"
	# model_names = ["epoch=18.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ",mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" +mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# # 0129
	# # conll03 bert-large, base 9157, prune evaluation
	# midpath = "conll03/spanPred_bert-large-uncased_maxSpan4prunFalse_spLenFalse_spMorphFalse_SpWtFalse_value1_61661034"
	# model_names = ["epoch=13.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ",mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" +mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams_prune.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# # conll03 bert-large, base+len 9222, prune evaluation
	# midpath = "conll03/spanPred_bert-large-uncased_maxSpan4prunFalse_spLenTrue_spMorphFalse_SpWtFalse_value1_09854370"
	# model_names = ["epoch=13.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ", mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" + mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams_prune.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# # # 0130
	# # wnut17 bert-large, base 9157, prune evaluation
	# midpath = "wnut17/spanPred_bert-large-uncased_prunFalse_spLenTrue_spMorphFalse_SpWtFalse_value1_96521534"
	# model_names = ["epoch=26.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ", mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" + mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams_prune.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)
	#
	# # # 0130
	# # wnut17 bert-large, base 9157, prune evaluation
	# midpath = "wnut17/spanPred_bert-large-uncased_prunFalse_spLenFalse_spMorphFalse_SpWtFalse_value1_09063161"
	# model_names = ["epoch=13.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ", mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" + mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams_prune.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# 0130
	# # conll03 bert-large, base 9321, prune evaluation
	# midpath = "conll03/spanPred_dev2train_bert-large-uncased_prunTrue_spLenFalse_spMorphFalse_SpWtFalse_value1_35932770_9321"
	# model_names = ["epoch=5.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ", mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" + mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams_prune.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

# # conll03 bert-large, base 9321, prune evaluation
# 	midpath = "conll03/spanPred_dev2train_bert-large-uncased_prunTrue_spLenTrue_spMorphTrue_SpWtFalse_value1_76851666_9318"
# 	model_names = ["epoch=14.ckpt"]
# 	for mn in model_names:
# 		print("model-name: ", mn)
# 		CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" + mn
# 		HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams_prune.yaml"
# 		evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

#

	# # conll02spanish bert-large, base 0.873509, prune evaluation
	# midpath = "conll02spanish/spanPred_bert-base-multilingual-uncased_maxSpan4prunFalse_spLenFalse_spMorphFalse_SpWtFalse_value1_62640970"
	# model_names = ["epoch=5_v0.ckpt"]
	# for mn in model_names:
	# 	print("model-name: ", mn)
	# 	CHECKPOINTS = "/home/jlfu/SPred/train_logs/" + midpath + "/" + mn
	# 	HPARAMS = "/home/jlfu/SPred/train_logs/" + midpath + "/lightning_logs/version_0/hparams.yaml"
	# 	evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)

	# 0125
	# conll03 bert-large, 9245 evaluation
	#midpath = "notetc/spanPred_bert-large-uncased_prunFalse_spLenTrue_spMorphFalse_SpWtFalse_value1_52887159"
	midpath = "multi_new/multi_es_nl_deu/spanner_bert-base-multilingual-uncased_spMLen_usePruneTrue_useSpLenTrue_useSpMorphTrue_SpWtTrue_value0.5_42512787"
	model_names = ["epoch=6.ckpt"]
	for mn in model_names:
		print("model-name: ", mn)
		CHECKPOINTS = "output/train_logs/" + midpath + "/" + mn
		HPARAMS = "output/train_logs/" + midpath + "/lightning_logs/version_0/hparams.yaml"
		evaluate(ckpt=CHECKPOINTS, hparams_file=HPARAMS)



