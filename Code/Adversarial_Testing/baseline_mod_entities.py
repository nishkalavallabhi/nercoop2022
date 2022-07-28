import skweak
import random

# path = "mconer_test.spacy"
# path = "wnut17test.spacy"
# path = "ontonotes_test.spacy"
path = "conll_deu_test.spacy"
# path = "conll03_test.spacy"

samples= list(skweak.utils.docbin_reader(path))
ent_dict = {}
for e in samples:
	  t_tags_temp = []
	  for l in range(len(e)):
	    if e[l].ent_iob_ and e[l].ent_type_:
	    	if e[l].ent_iob_ == "B":
	    		if e[l].ent_type_ not in ent_dict:
	    			n=1
	    			item = str(e[l])
	    			while l+n < len(e):
		    			if e[l+n].ent_iob_ == "I":
		    				item = str(e[l])+" "+str(e[l+n])
		    				n = n + 1
		    			else:
		    				break
		    		ent_dict[str(e[l].ent_type_)] = [item]
	    		else:
	    			n=1
	    			item = str(e[l])
	    			while l+n < len(e):
		    			if e[l+n].ent_iob_ == "I":
		    				item = str(e[l])+" "+str(e[l+n])
		    				n = n + 1
		    			else:
		    				break
	    			ent_dict[str(e[l].ent_type_)].append(item)


wor = []
ta = []
for e in samples:
	words_temp = []
	tags_temp = []
	ents = []
	for l in range(len(e)):
		# ents = []
		if e[l].ent_iob_ and e[l].ent_type_:
			if e[l].ent_iob_ == "B":
				n=1
				item = str(e[l])
				# start = e[l].start
				# end = e[l].end
				while l+n < len(e):
					if e[l+n].ent_iob_ == "I":
						item = item +" "+str(e[l+n])
						# end = end + len(e[l+n])
						n = n + 1
					else:
						break
				print("Item:",item)
				print("Type:",e[l].ent_type_)
				ents.append((item, e[l].ent_type_))

		 		
	line = str(e)
	old_l = str(e)
	print("BEFORE:",line)
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
			 			print("Item inside:", new)
			 			break
			 		else:
			 			new = 'sad'

			elif len(i[0].split()) == 2:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		
			 		else:
			 			new = 'sad'
			elif len(i[0].split()) == 3:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		else:
			 			new = 'sad'
			elif len(i[0].split()) == 4:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 4 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		else:
			 			new = 'sad'

			elif len(i[0].split()) == 5:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 5 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 4 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		else:
			 			new = 'sad'
			elif len(i[0].split()) == 6:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 6 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 4 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 5 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		else:
			 			new = 'sad'
			elif len(i[0].split()) == 7:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 7 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 4 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 5 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 6 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		else:
			 			new = 'sad'
			elif len(i[0].split()) == 9:
				for z in reversed(ent_dict[i[1]]):
			 		if len(z.split()) == 7 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 2 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break

			 		elif len(z.split()) == 3 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 4 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 5 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		elif len(z.split()) == 6 and line.find(z) == -1:
			 			new = z
			 			print("Item inside:", new)
			 			break
			 		else:
			 			new = 'sad'

			# print("SPLITS:",len(i[0].split()))
			if new == "sad":
				print("SAD ENCOUNTERED")
				new = random.choice(ent_dict[i[1]])
			if new in ent_dict[i[1]]:
			 	ent_dict[i[1]].remove(new)
			line = line.replace(i[0], new)
			# if line.lower().find(i[0].lower()) != -1:
			# 	line.replace()
			# line = line.replace(i[0].lower(), new)
			# line = line.upper().replace(i[0].upper(), new)

			s = line.split()

			if len(s) > len(t):
				for q in range(len(new.split()) - len(i[0].split())):
					count = s.count(new)
					while count !=0:
						if len(new.split()) == 1:
							t.insert(s.split().index(new.split()[0]), "O")
						elif len(new.split()) == 2:
							for f in range(len(s.split())):
								print(s.split()[f]+' '+s.split()[f+1])
								if s.split()[f]+' '+s.split()[f+1] == new:
									t.insert(f, "O")
									break
						elif len(new.split()) == 3:
							for f in range(len(s.split())):
								if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2] == new:
									t.insert(f, "O")
									break
						elif len(new.split()) == 4:
							for f in range(len(s.split())):
								if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3] == new:
									t.insert(f, "O")
									break
						elif len(new.split()) == 5:
							for f in range(len(s.split())):
								if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4] == new:
									t.insert(f, "O")
									break
						elif len(new.split()) == 6:
							for f in range(len(s.split())):
								if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4]+' '+s.split()[f+5] == new:
									t.insert(f, "O")
									break
						elif len(new.split()) == 7:
							for f in range(len(s.split())):
								if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4]+' '+s.split()[f+5]+' '+s.split()[f+6] == new:
									t.insert(f, "O")
									break
						elif len(new.split()) == 9:
							for f in range(len(s.split())):
								if s.split()[f]+' '+s.split()[f+1]+' '+s.split()[f+2]+' '+s.split()[f+3]+' '+s.split()[f+4]+' '+s.split()[f+5]+' '+s.split()[f+6]+' '+s.split()[f+7]+' '+s.split()[f+8] == new:
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
					# print("VAL:",old_l.index(val))
					print("Old:",i[0])
					print(old_l.split())
					# print(len(s))
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
								print(old_l.split())
								print(old_l.split()[f])
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
			old_l = ' '.join(word for word in s.copy())		
			# print("New:", new)
			# print("Old:", i[0])
			# print(old_l)
			# print(s)
			# print(t)
			# print(len(t))
			# print(len(s))
			# if len(t) != len(s):
			# 	print("ERROR!")


			# print("S:",s)
			x = 0
			for g in new.split():
				if g not in s:
					# print("old:", i[0])
					# print("New:", new)
					# print("Sentence:", s)
					break
				if x == 0:
					t[s.index(g)] = "B-"+i[1]
				if x > 0:
					t[s.index(g)] = "I-"+i[1]
				x = x + 1
				# print(t)
				# print(s)
				# print("--------------")	 


				
			# print("T:",t)



	# print(s)
	# print(t)
	# print(len(t))
	# # print(len(s))
	# if len(t) != len(s):
	# 	# wor.append(s)
	# 	# ta.append(t) 
	# 	print("ERROR")
	# 	break
	wor.append(s)
	ta.append(t)

	  		
	  	    	
# print("No. of words:",ta[1])
print(len(wor))
print(len(ta))
# print(ta[0])
fw = open("perturb_conll_deu_test_v1.txt", "w", encoding="utf-8")
# fw = open("perturb_ontonotes_test_v1.txt", "w", encoding="utf-8")
# fw = open("perturb_wnut17_test_v1.conll", "w", encoding="utf-8")
# fw = open("perturb_conll03_test.conll", "w", encoding="utf-8")
for i in range(len(wor)):
	for j in range(len(wor[i])):
		# print(i)
		# print(j)
		fw.write(wor[i][j]+"\t"+ta[i][j])
		fw.write("\n")
	fw.write("\n")
print("Wrote to disk !")



