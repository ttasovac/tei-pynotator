#! /usr/local/bin/python2

import xml.dom.minidom as dom
from xml.dom.minidom import parse, parseString
import nltk

file = "TreasureIsland-excerpt.xml"

# NAMED ENTITIES FUNCTION
def found_entities(paragraph=""):
	paragraph = paragraph.replace(".", " ." )
	paragraph = paragraph.replace("\n","")
	raw_tokenized = nltk.word_tokenize(paragraph)
	raw_text_withpostags = nltk.pos_tag(raw_tokenized)
	raw_text_with_entities = nltk.ne_chunk(raw_text_withpostags)
	return raw_text_with_entities

def make_paragraph_tagged(tree):
	#could be done in recoursive way
	token_analyzed_list = {}
	for i,node in enumerate(tree_with_entities):
		#print(str(node) + " idx " + str(i))
		if isinstance(node,tuple):
			#print(str(node) + " is a tuple ")
			token_analyzed_list[i] = node[0]
		elif isinstance(node, nltk.tree.Tree):
			tmp_str = str(node)
			#print(tmp_str +" len: " +str(len(node)))
			literal = make_literal(node)
			if "PERSON" in tmp_str:
				#testare quanti levelli ci sono
				token_analyzed_list[i] = "<persName>"+literal+"</persName>"
			#print("this from node: " + str(node[0][0]))
			elif "GPE" in tmp_str:
				#testare quanti livelli
				literal = make_literal(node)
				token_analyzed_list[i] = "<placeName>"+literal+"</placeName>"
			else:
				token_analyzed_list[i] = node[0][0]

	return token_analyzed_list

def make_literal(node):
	lenght = len(node)
	# multi-words are not universal now. Thay are just for two words
	if lenght == 2:
		literal = str(node[0][0]) +" " + str(node[1][0])
	else:
		literal = node[0][0]
	return literal

def make_string_tagged(tokens_as_dic):
	count = 0
	list_of_word = []
	while (count < len(tokens_as_dic)):
		list_of_word.append(tokens_as_dic[count])
		count+=1
	return " ".join(list_of_word).replace(" .",".").replace(" !","!").replace(" ,", ",").replace(" \"", "\"").replace(" ;", ";").replace("`` ", '"').replace("'' ",'"')

# END OF NAMED ENTITIES 


parsedObject = dom.parse(file)

for text_node in parsedObject.getElementsByTagName("text"):
	for paragraph in text_node.getElementsByTagName("p"):
		#need to know parent in order for replacing paragraph later
		parent = paragraph.parentNode
			
		#pure text that we are sending to NLPT
		par_text = paragraph.firstChild.nodeValue

		#this is where we call named entitiy recognition functions
		tree_with_entities = found_entities(par_text)
		dic_of_token = make_paragraph_tagged(tree_with_entities)
		string_tagged = "<p>"+make_string_tagged(dic_of_token)+"</p>"

		#here we have to turn the string into an xml node
		parsed_par_as_doc = parseString(string_tagged.encode("utf-8"))
		
		#here we are removing the original paragraph
		parent.removeChild(paragraph)
		parsed_par = parsed_par_as_doc.getElementsByTagName("p")[0]

		#here we are adding the funky new paragraph to the xml tree
		parent.appendChild(parsed_par)

	import re
	linebreak = re.compile(r"\n+")
	#print parsed_par.toxml("utf-8")
	mystring = parsedObject.toprettyxml().encode("utf-8")
	mystring = linebreak.sub("\n", mystring)
	print mystring		
