import skweak
import random
import argparse


def read_file(filepath):
    numcols = 2 #change here for 3 col vs 4 col conll format.
    fh = open(filepath, encoding="utf-8")
    sentences = []
    netags = []
    tempsen = []
    tempnet = []
    for line in fh:
       if line.strip() == "":
          if tempsen and tempnet:
              sentences.append(tempsen)
              netags.append(tempnet)
              tempsen = []
              tempnet = []
       else:
       	 if len(line.strip().split("\t")) == 2:
	         splits = line.strip().split("\t")
	         tempsen.append(splits[0])
	         tempnet.append(splits[numcols-1])
    fh.close()
    print("Num sentences in: ", filepath, ":", len(sentences))
    return sentences, netags

def get_entities(words, tags):
	ent_dict = {}
	for i in range(len(words)):
		for j in range(len(words[i])):
			if tags[i][j][0] == 'B':
				# print("B tag:",words[i][j])
				if tags[i][j][2:] not in ent_dict:
					n = 1
					item = words[i][j]
					# print("Item outside loop:", item, len(words[i]))
					while j+n < len(words[i]):
						# print("Going inside loop")
						print(tags[i][j+n])
						if tags[i][j+n][0] == "I":
							item = item+" "+words[i][j+n]
							n = n + 1
							# print("I tag found",item)
						else:
							break
						# print("ITEM:",item)
					ent_dict[tags[i][j][2:]] = [item]
				else:
					n = 1
					item = words[i][j]
					while j+n < len(words[i]):
						if tags[i][j+n][0] == 'I':
							item = item+" "+words[i][j+n]
							n = n + 1
							# print("I tag found",item)
						else:
							break
					ent_dict[tags[i][j][2:]].append(item)

	print("Fetched entities")
	return ent_dict




def replace_entities(ent_dict, words, tags):
	wor = []
	ta = []


	for i in range(len(words)):
		ents = []
		for j in range(len(words[i])):
			if tags[i][j][0] == 'B':
				n = 1
				item = words[i][j]
				while j+n < len(words[i]):
					# print(len(words[i]))
					# print(words[i][j+n])
					if tags[i][j+n][0] == 'I':
						item = item + " "+words[i][j+n]
						n = n+ 1
					else:
						break
				ents.append((item, tags[i][j][2:]))


	# for e in samples:
	# 	words_temp = []
	# 	tags_temp = []
	# 	ents = []
	# 	for l in range(len(e)):
	# 		# ents = []
	# 		if e[l].ent_iob_ and e[l].ent_type_:
	# 			if e[l].ent_iob_ == "B":
	# 				n=1
	# 				item = str(e[l])
	# 				# start = e[l].start
	# 				# end = e[l].end
	# 				while l+n < len(e):
	# 					if e[l+n].ent_iob_ == "I":
	# 						item = item +" "+str(e[l+n])
	# 						# end = end + len(e[l+n])
	# 						n = n + 1
	# 					else:
	# 						break
	# 				# print("Item:",item)
	# 				# print("Type:",e[l].ent_type_)
	# 				ents.append((item, e[l].ent_type_))

			 		
		line = " ".join(words[i])
		old_l = " ".join(words[i])
		# print("BEFORE:",line)
		# print(ents)
		w = []
		t = []
		temp_t = []
		for o in range(len(line.split())):
		  t.append("O")
		# print(len(ents))
		# print("INITIAL:",len(t))
		s = line.split()
		if len(ents) != 0:
			for i in ents:
				if len(i[0].split()) == 1:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 1 and line.find(z) == -1 :
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		else:
				 			new = 'sad'

				elif len(i[0].split()) == 2:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		
				 		else:
				 			new = 'sad'
				elif len(i[0].split()) == 3:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		else:
				 			new = 'sad'
				elif len(i[0].split()) == 4:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 4 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		else:
				 			new = 'sad'

				elif len(i[0].split()) == 5:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 5 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 4 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		else:
				 			new = 'sad'
				elif len(i[0].split()) == 6:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 6 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 4 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 5 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		else:
				 			new = 'sad'
				elif len(i[0].split()) == 7:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 7 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 4 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 5 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 6 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		else:
				 			new = 'sad'
				elif len(i[0].split()) == 9:
					for z in reversed(ent_dict[i[1]]):
				 		if len(z.split()) == 7 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 2 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break

				 		elif len(z.split()) == 3 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 4 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 5 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		elif len(z.split()) == 6 and line.find(z) == -1:
				 			new = z
				 			# print("Item inside:", new)
				 			break
				 		else:
				 			new = 'sad'

				# print("SPLITS:",len(i[0].split()))
				if new == "sad":
					# print("SAD ENCOUNTERED")
					new = random.choice(ent_dict[i[1]])
				if new in ent_dict[i[1]]:
				 	ent_dict[i[1]].remove(new)

				# supp = line.find(i[0])
				# if supp != -1:
				# 	supp = line.split().index(i[0])
				# if line.count(new)
				print("Before replacing:",i[0],"new:", new)
				# li = line.split()
				# pos = li.index(i[0])
				

				line = line.replace(" "+i[0]+" ", " "+new+" ", 1)
				# print("After replacing:",line)
				

				# if line.lower().find(i[0].lower()) != -1:
				# 	line.replace ()
				# line = line.replace(i[0].lower(), new)
				# line = line.upper().replace(i[0].upper(), new)
				# if supp != -1:
				# 	new = new + 
				s = line.split()
				# s = line

				if len(s) > len(t):
					s = line
					for q in range(len(new.split()) - len(i[0].split())):
						count = s.count(new)
						if count> 1:
							break
						while count !=0:
							# if len(new.split()) == 1:
							# 	t.insert(s.split().index(new.split()[0]), "O")
							if len(new.split()) == 2:
								for f in range(len(s.split())):
									print("Inside split:",s)
									print(s.split()[f])
									print("new:",new)
									print(s.split()[f]+' '+s.split()[f+1])
									if s.split()[f]+' '+s.split()[f+1] == new:
										t.insert(f, "O")
	
										break
							elif len(new.split()) == 3:
								for f in range(len(s.split())):
									if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2] == new:
										t.insert(f, "O")
										t.insert(f, "O")
										
										break
							elif len(new.split()) == 4:
								for f in range(len(s.split())):
									if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3] == new:
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										
										break
							elif len(new.split()) == 5:
								for f in range(len(s.split())):
									if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4] == new:
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
									
										break
							elif len(new.split()) == 6:
								for f in range(len(s.split())):
									if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4]+' '+s.split()[f+5] == new:
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										
										break
							elif len(new.split()) == 7:
								for f in range(len(s.split())):
									if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4]+' '+s.split()[f+5]+' '+s.split()[f+6] == new:
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										
										break
							elif len(new.split()) == 9:
								for f in range(len(s.split())):
									if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4]+' '+s.split()[f+5]+' '+s.split()[f+6]+' '+s.split()[f+7]+' '+s.split()[f+8] == new:
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										t.insert(f, "O")
										break
							count = count - 1
						# t.insert(s.index(new.split()[0]), "O")
						# print("inserting into T",len(t))
				# print("OLD_L:",old_l)
				if len(s) < len(t):
					for q in range(len(i[0].split()) - len(new.split())):
						# val = i[0].split()[0]
						val = i[0]
						print("VAL:",old_l.index(val))
						print("Old:",i[0])
						print(old_l.split())
						print(len(s))
						count = old_l.count(val)
						c1 = old_l.split().count(val[-1])
						c2 = old_l.split().count(val[0])
						while count !=0:
							if len(val.split()) == 1:
								del t[old_l.split().index(val.split()[0])]
							elif len(val.split()) == 2:
								for f in range(len(old_l.split())):
									if old_l.split()[f]+' '+old_l.split()[f+1] == val:
										del t[f]
										break
							elif len(val.split()) == 3:
								for f in range(len(old_l.split())):
									# print(old_l.split())
									# print(old_l.split()[f])
									if old_l.split()[f]+' '+old_l.split()[f+1]+' '+old_l.split()[f+2] == val:
										del t[f]
										break
							elif len(val.split()) == 4:
								for f in range(len(old_l.split())):
									if old_l.split()[f]+' '+old_l.split()[f+1]+' '+old_l.split()[f+2]+' '+old_l.split()[f+3] == val:
										del t[f]
										break
							elif len(val.split()) == 5:
								for f in range(len(old_l.split())):
									if old_l.split()[f]+' '+old_l.split()[f+1]+' '+old_l.split()[f+2]+' '+old_l.split()[f+3]+' '+old_l.split()[f+4] == val:
										del t[f]
										break
							elif len(val.split()) == 6:
								for f in range(len(old_l.split())):
									if old_l.split()[f]+' '+old_l.split()[f+1]+' '+old_l.split()[f+2]+' '+old_l.split()[f+3]+' '+old_l.split()[f+4]+' '+old_l.split()[f+5] == val:
										del t[f]
										break
							elif len(val.split()) == 7:
								for f in range(len(old_l.split())):
									if old_l.split()[f]+' '+old_l.split()[f+1]+' '+old_l.split()[f+2]+' '+old_l.split()[f+3]+' '+old_l.split()[f+4]+' '+old_l.split()[f+5]+' '+old_l.split()[f+6] == val:
										del t[f]
										break
							elif len(val.split()) == 9:
								for f in range(len(old_l.split())):
									if old_l.split()[f]+' '+old_l.split()[f+1]+' '+old_l.split()[f+2]+' '+old_l.split()[f+3]+' '+old_l.split()[f+4]+' '+old_l.split()[f+5]+' '+old_l.split()[f+6]+' '+old_l.split()[f+7]+' '+old_l.split()[f+8] == val:
										del t[f]
										break
							count = count - 1



								# old_l.split()index(val.split()[0])

						# if c1 == c2:
						# 	while c2 != 0:
						# 		del t[old_l.split().index(val[0])]
						# 		c2 = c2 - 1
						# else:
						# 	while c1 != 0:
						# 		del t[old_l.split().index(val[-1])]
						# 		c1 = c1 - 1
						# if val in old_l.split():
						# 	del t[old_l.split().index(val)]
				s = line.split()
				old_l = ' '.join(word for word in s.copy())		
				print("New:", new)
				print("Old:", i[0])
				print(old_l)
				print(s)
				print(t)
				print(len(t))
				print(len(s))
				if len(t) != len(s):
					print("ERROR!")


				# print("S:",s)
				x = 0
				if len(s)!= len(t):
					break
				for g in new.split():
					if g not in s:
						print("old:", i[0])
						print("New:", new)
						print("Sentence:", s)
						break
					if x == 0:

						print("S:",len(s))
						print("g:",g, s.index(g))
						print(i[1])
						print("t:",t)
						t[s.index(g)] = "B-"+i[1]
					if x > 0:
						t[s.index(g)] = "I-"+i[1]
					x = x + 1
					print(t)
					print(s)
					print("--------------")	 


					
				# print("T:",t)



		# print(s)
		# print(t)
		print(len(t))
		print(len(s))
		if len(t) == len(s):
			wor.append(s)
			ta.append(t) 
			# print("ERROR")
			# break
		# wor.append(s)
		# ta.append(t)
	return wor, ta


	  		
	  	    	
# print("No. of sentences:",ta[1])
# print(len(wor))
# print(len(ta))

def write_to_disk(new_file_name, wor, ta):
	writer = open(new_file_name,"w", encoding="utf-8")
	print("No. of sentences:", len(wor))
	for i in range(len(wor)):
		for j in range(len(wor[i])):
			# print(i)
			# print(j)
			writer.write(wor[i][j]+"\t"+ta[i][j])
			writer.write("\n")
		writer.write("\n")
	print("Wrote to disk !")

def main(args):

	# samples= list(skweak.utils.docbin_reader(args.input_file))
	words, tags = read_file(args.input_file)
	entity_dict = get_entities(words, tags)
	# # print(entity_dict['PER'])
	words, tags = replace_entities(entity_dict, words, tags)

	write_to_disk(args.output_file, words, tags)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", help="Name or path of the input test file", required=True)
    parser.add_argument("--output_file", help="Name or path of the modified output test file", required=True)
    args=parser.parse_args()
    main(args)


