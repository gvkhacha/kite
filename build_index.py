from structures import DocID, Parser
from collections import defaultdict

import interact_files

import lxml.html.diff
import lxml.etree

import sys, io



def tokenizeDoc(doc: DocID, index: dict) -> [(str, int)]:
	""" Reads document's file and parses through tokens
	For now, only considers occurances
	Return: [(token, occurances)]
	"""
	htmlFile = None
	try:
		htmlFile = open(doc.getPath())
		p = Parser()
		p.feed(htmlFile.read())
		index[doc.getID()].extend(p.getTokens().items())
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
		x = DocID(l)
		tokenizeDoc(x, index)
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