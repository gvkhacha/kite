from structures import DocID
from collections import defaultdict

import interact_files

import lxml.html.diff
import lxml.etree
from bs4 import BeautifulSoup

import sys, io



def tokenizeDoc(doc: DocID, index: dict) -> [(str, int)]:
	""" Reads document's file and parses through tokens
	For now, only considers occurances
	Return: [(token, occurances)]
	"""
	htmlFile = None
	try:
		htmlFile = open(doc.getPath())
		print("HALLO")
		soup = BeautifulSoup(htmlFile, 'lxml')
		# print(soup.find_all('img'))
		# print(soup.children)
		for i in soup.descendants:
			# print(i.name)
			print(i)
			# print(repr(i))
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
		if d.getID() in index:
			continue
		else:
			tokenizeDoc(d, index)
	prettyPrintIndex(index)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		index = interact_files.loadIndexFromFile()
	elif sys.argv[1] in {'-r', 'reload'}:
		index = defaultdict(list)
		interact_files.resetIndexFile()
	else:
		raise Warning("Invalid command line input")

	try:
		main(index)
	except KeyboardInterrupt:
		pass
	finally:
		interact_files.saveIndexToFile(index)