import nltk

class NLTK_Helper:
	def __init__(self):
		pass

	def process(self, p):
		self.p = p
		tree_with_entities = self.found_entities(self.p)
		self.dic_of_token = self.make_paragraph_tagged(tree_with_entities)
		self.string_tagged = self.make_string_tagged(self.dic_of_token)
		return self.string_tagged

	def found_entities(self, paragraph=""):
		paragraph = self.p
		paragraph = paragraph.replace(".", " ." )
		paragraph = paragraph.replace("\n","")
		raw_tokenized = nltk.word_tokenize(paragraph)
		raw_text_withpostags = nltk.pos_tag(raw_tokenized)
		raw_text_with_entities = nltk.ne_chunk(raw_text_withpostags)
		return raw_text_with_entities

	def make_paragraph_tagged(self, tree):
		#could be done in recoursive way
		token_analyzed_list = {}
		self.tree = tree
		for i,node in enumerate(self.tree):
			#print(str(node) + " idx " + str(i))
			if isinstance(node,tuple):
				#print(str(node) + " is a tuple ")
				token_analyzed_list[i] = node[0]
			elif isinstance(node, nltk.tree.Tree):
				tmp_str = str(node)
				#print(tmp_str +" len: " +str(len(node)))
				literal = self.make_literal(node)
				if "PERSON" in tmp_str:
					#testare quanti levelli ci sono
					token_analyzed_list[i] = "<persName>"+literal+"</persName>"
				#print("this from node: " + str(node[0][0]))
				elif "GPE" in tmp_str:
					#testare quanti livelli
					literal = self.make_literal(node)
					token_analyzed_list[i] = "<placeName>"+literal+"</placeName>"
				else:
					token_analyzed_list[i] = node[0][0]

		return token_analyzed_list

	def make_literal(self, node):
		lenght = len(node)
		# multi-words are not universal now. Thay are just for two words
		if lenght == 2:
			literal = str(node[0][0]) +" " + str(node[1][0])
		else:
			literal = node[0][0]
		return literal

	def make_string_tagged(self, tokens_as_dic):
		count = 0
		list_of_word = []
		while (count < len(tokens_as_dic)):
			list_of_word.append(tokens_as_dic[count])
			count+=1
		return " ".join(list_of_word).replace(" .",".").replace(" !","!").replace(" ,", ",").replace(" \"", "\"").replace(" ;", ";").replace("`` ", '"').replace("'' ",'"')



###########################################
# To test the NLTK_Helper while developing
# without having to deal with XML files
# use the code below:

#test = NLTK_Helper()
#raw_text = "Mike likes pizza from United States ! And Lars (on the other hand)... doesn't like it!"
#processed_text = test.process(raw_text)
#print(processed_text)


##########################################
