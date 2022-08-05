import csv
import pandas as pd
from faker import Faker
import random
import argparse

#Install Faker library before running this

def replace_entities(input_file, output_file):

    fake = Faker(['en-US', 'en-CA', 'en-IN']) #This can be changed to many other options. 
    # fake = Faker(['de', 'de-AT', 'de-CH', 'de-DE']) #Uncomment for german test set
    fh = open(input_file, encoding = "utf-8")
    fw = open(output_file, "w", encoding="utf-8")
    numcols = 2
    for line in fh:
        splits = line.strip().split("\t")
        if len(splits) == 2:
            if splits[numcols - 1] == 'B-'+'PER':
                #Lines commented below are for GPE. 
                splits[0] = fake.first_name().split()[0]
                
            elif splits[numcols - 1] == 'I-'+'PER':
                splits[0] = fake.last_name().split()[0]
            elif splits[numcols - 1] == 'B-'+'LOC':
                splits[0] = random.choice([fake.country(), fake.city()]).split()[0]
            elif splits[numcols - 1] == 'I-'+'LOC':
                splits[0] = fake.city_suffix().split()[0]
            print("\t".join(splits))
            fw.write("\t".join(splits))
            fw.write("\n")
        else:
            fw.write("\n")

    fh.close()
    fw.close()
    print("DONE")


def main(args):
    replace_entities(args.input_file, args.output_file)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", help="Name or path of the input test file", required=True)
    parser.add_argument("--output_file", help="Name or path of the modified output test file", required=True)
    args=parser.parse_args()
    main(args)