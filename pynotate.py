#! /usr/local/bin/python2

import xml.dom.minidom as dom
from xml.dom.minidom import parse, parseString
from NLTK_helper import *

file = "TreasureIsland-excerpt.xml"

class Annotator:

    def __init__(self, file):
        self.file = file
        self.xmlObj = dom.parse(self.file)

    def printXML(self):
    	self.file = file
    	#xmlObj = self.parseXML()
    	#print(type(self.xmlObj))
    	print self.xmlObj.toxml("utf-8")

    def remove_whites(self, string):
    	#i may have to check for other string issues here
    	#apostrophes etc. 
    	self.string = string
    	import re
    	whites = re.compile(r"\s+")
    	sanitized = whites.sub(" ", self.string)
    	return sanitized

    def get_paragraphs (self):
		#returns a list of paragraph dom objects and its parent nodes 
		self.paragraphs = []
		for text_node in self.xmlObj.getElementsByTagName("text"):
			for paragraph in text_node.getElementsByTagName("p"):
				parent = paragraph.parentNode
				self.paragraphs.append([paragraph, parent])
			return self.paragraphs

    def edit_paragraphs (self):
		self.pars = self.get_paragraphs()
		for each in self.pars:
			orig_p = each[0]
			parent = each[1]
			p_text = self.remove_whites(orig_p.firstChild.nodeValue)

			# here we are sending the paragraph text to be processed by NLTK

			nltk_analyze = NLTK_Helper ()
			analyzed_p = nltk_analyze.process(p_text)
			xml_p = parseString("<p>"+analyzed_p.encode("utf-8")+"</p>").getElementsByTagName("p")[0]

			parent.removeChild(orig_p)
			parent.appendChild(xml_p)


#main body of the program
annotate = Annotator(file)
#annotate.printXML()
annotate.edit_paragraphs()
annotate.printXML()
