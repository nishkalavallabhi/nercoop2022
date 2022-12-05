import subprocess


# Arguements to be passed:
# Mandatory args - train_file, test_file, dev_file
# Optional args - seed, epochs, save_model, prop
# prop -> proportion of train data to be considered. 0.2 is 20%, 04, 40% and so on. For full train data use "--prop 1"

#subprocess.run(f"python train_mbert.py --train_file multi_es_nl_deu/multi_train.txt --dev_file multi_es_nl_deu/multi_dev.txt --test_file multi_es_nl_deu/multi_test.txt --seed 342 --epochs 10 --prop 1 --save_model x_lingual/mbert_es_nl_deu.bin", shell=True)

subprocess.run(f"python train_mbert.py --train_file conll_en/conll_en_train.txt --dev_file conll_en/conll_en_dev.txt --test_file conll_en/conll_en_test.txt --seed 42 --epochs 8 --prop 1", shell=True) # --save_model x_lingual/multi_three_xlm.bin", shell=True)

subprocess.run(f"python train_mbert.py --train_file conll_en/conll_en_train.txt --dev_file conll_en/conll_en_dev.txt --test_file conll_en/conll_en_test.txt --seed 42 --epochs 3 --prop 0.2", shell=True) #--save_model x_lingual/multi_three_xlm.bin", shell=True)

subprocess.run(f"python train_mbert.py --train_file conll_en/conll_en_train.txt --dev_file conll_en/conll_en_dev.txt --test_file conll_en/conll_en_test.txt --seed 42 --epochs 6 --prop 0.8", shell=True) #--save_model x_lingual/multi_three_xlm.bin", shell=True)

subprocess.run(f"python train_mbert.py --train_file conll_en/conll_en_train.txt --dev_file conll_en/conll_en_dev.txt --test_file conll_en/conll_en_test.txt --seed 42 --epochs 4 --prop 0.4", shell=True) #--save_model x_lingual/multi_three_xlm.bin", shell=True)

subprocess.run(f"python train_mbert.py --train_file conll_en/conll_en_train.txt --dev_file conll_en/conll_en_dev.txt --test_file conll_en/conll_en_test.txt --seed 42 --epochs 5 --prop 0.6", shell=True) #--save_model x_lingual/multi_three_xlm.bin", shell=True)

