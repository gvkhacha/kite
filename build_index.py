from structures import DocID, Tokenizer
from collections import defaultdict

import interact_files

import lxml.html.diff
import lxml.etree

import sys, io


def tokenizeDoc(doc: DocID, index: dict, imgIndex: dict) -> None:
	""" Reads document's file and parses through tokens
	For now, only considers occurances
	"""
	t = Tokenizer(doc, index, imgIndex)
	t.findAllTokens()




def _prettyPrintIndex(index: dict):
	for doc, postings in index.items():
		print("{}: ".format(doc))
		for token, count in postings:
			print("\t{} : {}".format(token, count))


def _prettyPrintImgIndex(index: dict):
	for tup, postings in index.items():
		title, alt = tup
		print("{}, {}".format(title, alt))
		for url, priority in postings:
			print("\t{} : {}".format(url, priority))


def main(index: dict, imgIndex: dict):
	for l in interact_files.readFromBook():
		d = DocID(l)
		print('NEXT DOC!\n\tID:{}\n'.format(d.getID()))
		if d.getID() in index:
			continue
		else:
			tokenizeDoc(d, index, imgIndex)
	_prettyPrintIndex(index)
	print('\n\n')
	_prettyPrintImgIndex(imgIndex)


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
		main(index, imgIndex)
	except KeyboardInterrupt:
		pass
	finally:
		interact_files.saveIndexToFile(index, 'main')
		interact_files.saveIndexToFile(imgIndex, 'img')