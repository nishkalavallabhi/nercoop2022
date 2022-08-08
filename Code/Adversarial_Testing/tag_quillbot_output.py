from build_paraphrase_dataset import *

def write_paraphrased_dataset(fpout, pp_sens, pp_labels):
    fh = open(fpout, "w")
    for i in range(0, len(pp_sens)):
        for j in range(0, len(pp_sens[i])):
            fh.write(pp_sens[i][j] + "\t" + pp_labels[i][j])
            fh.write("\n")
        fh.write("\n")
    fh.close()


def format_sentence(sentence):
    new_mod = []
    mod_sen = sentence.split()
    temp_w = mod_sen.copy()
    for i in mod_sen:
        l = []

        # i = i.lower() #Uncomment this line for Multiconer test set

        if "'" in i and i.count('.') == 1:
            l = i.split("'")
            l.insert(1, "'")
            l.append('.')
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]

        elif i.count('.') == 1:
            l = i.split(".")
            l.append(".")
            if "" in l:
                l.remove("")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]
        # new_mod.append(temp_w)

        elif i.count('?') == 1:
            l = i.split("?")
            l.append("?")
            if "" in l:
                l.remove("")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]
        # new_mod.append(temp_w)

        elif ")" in i:
            l = i.split(")")
            l.append(")")
            if "" in l:
                l.remove("")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]

        elif "(" in i:
            l = i.split("(")
            l.append("(")
            if "" in l:
                l.remove("")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]


        elif "'" in i:
            l = i.split("'")
            l.insert(1, "'")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]

        elif "," in i:
            l = i.split(",")
            l.append(",")
            if "" in l:
                l.remove("")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]

        elif i.count('.') == 1:
            l = i.split(".")
            l.append(".")
            if "" in l:
                l.remove("")
            d = []
            for z in l:
                d.append(i)
                temp_w.insert(temp_w.index(i), z)
                # print("mod:",temp_w)
            if len(d) != 0:
                del temp_w[temp_w.index(d[0])]
    # new_mod.append(temp_w)
    return temp_w

def main():
    #CHANGE THESE THREE SENTENCES
    path1 = "../../tmp/wnut-forpp.conll"
    path2 = "../../tmp/wnut-pp.conll"
    path3 = "../../tmp/wnut-test-pp.conll"

    #Read the original sentences, tags set:
    orig_sentences = [] #list of list of tokens
    orig_tags = [] #list of list of tags
    #senflag = False
    tempsen = ""
    temptags = ""
    for line in open(path1):
        if len(line) > 1:
            if len(tempsen) > 1:
                temptags = line.strip()
                orig_tags.append(temptags.split())
                orig_sentences.append(tempsen.split())
                tempsen = ""
                tempflag = ""
            else:
                tempsen = line.strip()

    #Read the paraphrased output file:
    paraphrases = [] #list of list of tokens
    for line in open(path2):
        if len(line) > 1:
            paraphrases.append(format_sentence(line.strip()))# - DO THIS ONLY FOR WNUT, Multiconer!

    print(len(paraphrases))
    print(len(orig_sentences))
    assert(len(orig_sentences) == len(orig_tags))
    assert(len(paraphrases) == len(orig_sentences))

    pp_labels = [] #list of list of tags
    pp_sens = [] #final pp sentences

    num_discarded_sentences = 0
    for i in range(0, len(orig_sentences)):
        try:
            pp_labels_sen = tag_paraphrase(orig_sentences[i], orig_tags[i], paraphrases[i])
            pp_labels.append(pp_labels_sen)
            pp_sens.append(paraphrases[i])
        except:
            print("The following sentence is not getting added to the paraphrased dataset: ")
            print("Original: ", " ".join(orig_sentences[i]))
            print("Paraphrased: ", " ".join(paraphrases[i]))
            num_discarded_sentences += 1
            print()
            continue

    print("Number of discarded sentences: ", num_discarded_sentences)

    write_paraphrased_dataset(path3, pp_sens, pp_labels)


if __name__ == "__main__":
    main()