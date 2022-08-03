from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import pyperclip

def get_paraphrase(sentence, driver):
	link = "https://quillbot.com/"
	# driver = webdriver.Chrome('/Users/vajjalas/Downloads/chromedriver')
	if "QuillBot AI" not in driver.title:
		driver.get(link)
	input_text = driver.find_element("id","inputText")
	input_text.clear()
	input_text.send_keys(sentence)
	# input_text.submit()
	button = driver.find_element("xpath","//*[@id='InputBottomQuillControl']/div/div/div/div[2]/div/div/div/div/button")
	button.click()
	time.sleep(10)

	copy_button = driver.find_element("xpath", "//*[@id='outputBottomQuillControls-default']/div/div/div/div/div[2]/div/div[3]/button")
	copy_button.click()

	pyperclip.waitForPaste()
	data = pyperclip.paste()
	print(data)
	return str(data)
	# driver.close()

def format_sentence(sentence):
	new_mod = []
	mod_sen = sentence.split()
	temp_w = mod_sen.copy()
	for i in mod_sen:
		l=[]
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

#example = "Gandhi was born in Gujarat."
#formatted_sentence = format_sentence(get_paraphrase(example))
#print(formatted_sentence)