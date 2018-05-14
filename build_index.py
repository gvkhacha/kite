from structures import DocID
from collections import defaultdict

import interact_files

import lxml.html.diff
import lxml.etree
from bs4 import BeautifulSoup, Comment

import sys, io



def tokenizeDoc(doc: DocID, index: dict, imgIndex: dict) -> [(str, int)]:
	""" Reads document's file and parses through tokens
	For now, only considers occurances
	Return: [(token, occurances)]
	"""
	htmlFile = None
	try:
		htmlFile = open(doc.getPath())
		print("HALLO")
		soup = BeautifulSoup(htmlFile, 'lxml')
		comments=soup.find_all(string=lambda text:isinstance(text,Comment))
		title = soup.title
		if title != None:
			title = title.text #remove <title> tag
		# for i in soup.descendants:
		# 	print(i.name)
		# 	print('\n-------\n')

		# 	if i.name == None:
		# 		if i in comments:
		# 			print("Found a comment")
		# 		else:
		# 			#At text content, can start getting data. 
		# 			# COULD start considering parents i.parent.name == h1 -> Better to do it before?
		# 			print("Found some text-not comment")
		# 	elif i.name == 'img':
		# 		#Found an image, add to image index
		# 		pass
		# 	print('\n-------\n')
		# 	print(i)
		# 	print('\n-------\n')
		# 	# print(repr(i))
			# print(type(i))
	except:
		# print(doc.getPath())
		raise #Not sure yet... re-raise
	finally:
		if htmlFile:
			htmlFile.close()



def prettyPrintIndex(index: dict):
	for doc, postings in index.items():
		print("{}: ".format(doc))
		for token, count in postings:
			print("\t{} : {}".format(token, count))


def main(index: dict):
	for l in interact_files.readFromBook():
		d = DocID(l)
		print('NEXT DOC!\n\tID:{}\n'.format(d.getID()))
		if d.getID() in index:
			continue
		else:
			tokenizeDoc(d, index)
	prettyPrintIndex(index)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		index = interact_files.loadIndexFromFile('main')
		imgIndex = interact_files.loadIndexFromFile('img')
	elif sys.argv[1] in {'-r', 'reload'}:
		index = defaultdict(list) # {token : [(docID, priority)]}
		imgIndex = defaultdict(list) # {(title, imgAlt): [(srcurl, priority)]}
		interact_files.resetIndexFiles()
	else:
		raise Warning("Invalid command line input")

	try:
		main(index)
	except KeyboardInterrupt:
		pass
	finally:
		interact_files.saveIndexToFile(index)