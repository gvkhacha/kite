from structures import DocID, Tokenizer
from collections import defaultdict

import interact_files

import lxml.html.diff
import lxml.etree

import sys, io


def tokenizeDoc(doc: DocID, tokensList: list, imgIndex: dict) -> None:
	""" Reads document's file and parses through tokens
	For now, only considers occurances
	"""
	t = Tokenizer(doc, tokensList, imgIndex) #Tokenizer adds to tokenslist and imgindex
	t.findAllTokens()


def addTokensToIndex(tokens: list, index: dict):
	"""Takes text tokens found in self._tokens and adds to index:
	tokens : [(token, docID, weight )]
	index: {token: [(docID, weight)]} with no duplicates
	index is defaultdict[list] -> can append any time
	"""
	for token, docid, weight in tokens:
		if token in index.keys():
			found = False
			for i in range(len(index[token])):
				if index[token][i][0] == docid:
					#If the same (token, docID) is in the index, add the weight
					found = True
					index[token][i] = (docid, index[token][i][1] + weight)
			if not found:
				#If it was not found, add it raw
				index[token].append((docid, weight))
		else:
			index[token].append((docid, weight))


def _prettyPrintIndex(index: dict):
	for token, postings in index.items():
		print("{}".format(token))
		for i, k in postings:
			print("\t{}: {}".format(i, k))


def _prettyPrintImgIndex(index: dict):
	for tup, postings in index.items():
		title, alt = tup
		print("{}, {}".format(title, alt))
		for url, priority in postings:
			print("\t{} : {}".format(url, priority))


def main(tokensList: list, index: dict, imgIndex: dict):
	for l in interact_files.readFromBook():
		d = DocID(l)
		print('NEXT DOC!\n\tID:{}\n'.format(d.getID()))
		if d.getID() in index:
			continue
		else:
			tokenizeDoc(d, tokensList, imgIndex)

	addTokensToIndex(tokensList, index)
	_prettyPrintIndex(index)
	# print('\n\n')
	# _prettyPrintImgIndex(imgIndex)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		index = interact_files.loadIndexFromFile('main')
		imgIndex = interact_files.loadIndexFromFile('img')
	elif sys.argv[1] in {'-r', 'reload'}:
		tokensList = [] # [(token, docID, priority)]
		""" Index isn't necessarily needed until we need to merge...Maybe better to keep it
		out of memory, but either way is okay"""
		index = defaultdict(list) # {token : [(docID, priority)]}
		imgIndex = defaultdict(list) # {(title, imgAlt): [(srcurl, priority)]}
		interact_files.resetIndexFiles()
	else:
		raise Warning("Invalid command line input")

	try:
		main(tokensList, index, imgIndex)
	except KeyboardInterrupt:
		pass
	finally:
		interact_files.saveIndexToFile(index, 'main')
		interact_files.saveIndexToFile(imgIndex, 'img')