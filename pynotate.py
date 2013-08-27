#! /usr/local/bin/python2

import xml.dom.minidom as dom
from xml.dom.minidom import parse, parseString
import re
from nltk_helper import *

file = "TreasureIsland-excerpt.xml"

class Annotator:

    def __init__(self, file):
        self.file = file
        self.xmlObj = dom.parse(self.file)
        #print(self.xmlObj.toxml("utf-8"))

    def printXML(self):
		self.file = file
		print(self.xmlObj.toxml("utf-8"))

    def clean_up(self, parent):
    	#get rid of empty nodes which were created when removing original paragraphs
		self.parent = parent
		for child in list(self.parent.childNodes):
			if child.nodeType == child.TEXT_NODE and child.data.strip()=="":
				self.parent.removeChild(child)

    def remove_whites(self, string):
    	#i may have to check for other string issues here
    	#apostrophes etc. 
    	self.string = string
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
			#print(p_text.encode("utf-8"))

			# send to NLTK
			nltk_analyze = NLTK_Helper ()
			analyzed_p = nltk_analyze.process(p_text)
			#print analyzed_p.encode("utf-8")
			xml_p = parseString("<p>"+analyzed_p.encode("utf-8")+"</p>").getElementsByTagName("p")[0]

			# replace in xml
			parent.removeChild(orig_p)
			parent.appendChild(xml_p)
			self.clean_up(parent)


#main body of the program
annotate = Annotator(file)
annotate.edit_paragraphs()
annotate.printXML()
