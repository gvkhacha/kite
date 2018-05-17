from structures import DocID, Tokenizer
from collections import defaultdict

import interact_files

import lxml.html.diff
import lxml.etree

import sys, io, time

ANALYTICS = dict()

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


def main(index: dict, imgIndex: dict):
	try:
		docCountPrev = 0
		docCountCont = 0
		searchTime = time.time()

		contPoint = index.get('& LAST DOC &', 0)
		tokensList = [] # [(token, docID, priority)]
		for l in interact_files.readFromBook():
			d = DocID(l)
			# print('NEXT DOC!\n\tID:{}\n'.format(d.getID()))
			if docCountCont < contPoint:
				docCountPrev += 1
				docCountCont += 1
			else:
				docCountCont += 1
				t = Tokenizer(d, tokensList, imgIndex) #Tokenizer adds to tokenslist and imgindex
				t.findAllTokens()
	except KeyboardInterrupt:
		print("Keyboard Interrupt. Writing files and shutting down.")
	finally:
		print("Finishing program. Do not shut down.")
		ANALYTICS['searchTime'] = time.time() - searchTime
		ANALYTICS['docCountPrev'] = docCountPrev
		ANALYTICS['docCountCont'] = docCountCont - docCountPrev
		tokenTime = time.time()

		addTokensToIndex(tokensList, index)

		ANALYTICS['tokenTime'] = time.time() - tokenTime
		saveTime = time.time()

		index['& LAST DOC &'] = docCountCont
		interact_files.saveIndexToFile(index, 'main')
		interact_files.saveIndexToFile(imgIndex, 'img')


		ANALYTICS['saveTime'] = time.time() - saveTime
		for i, k in ANALYTICS.items():
			print("{} : {}".format(i, k))
	# _prettyPrintIndex(index)
	# print('\n\n')
	# _prettyPrintImgIndex(imgIndex)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		loadTime = time.time()
		index = interact_files.loadIndexFromFile('main')
		imgIndex = interact_files.loadIndexFromFile('img')

		ANALYTICS['load'] = time.time() - loadTime

	elif sys.argv[1] in {'-r', 'reload'}:
		""" Index isn't necessarily needed until we need to merge...Maybe better to keep it
		out of memory, but either way is okay"""
		index = defaultdict(list) # {token : [(docID, priority)]}
		imgIndex = defaultdict(list) # {(title, imgAlt): [(srcurl, priority)]}
		interact_files.resetIndexFiles()
	else:
		raise Warning("Invalid command line input")

	main(index, imgIndex)