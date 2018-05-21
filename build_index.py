from structures import DocID, Tokenizer
from database import interact_files

from collections import defaultdict, Counter

import sys, io, time

ANALYTICS = dict()
DTRANS = dict() #Translation table to turn doc ID to objects

def addTokensToIndex(tokens: list, index: dict):
	"""Takes text tokens found in self._tokens and adds to index:
	tokens : [(token, docID, weight )]
	index: {token: [(docID, weight)]} with no duplicates
	index is defaultdict[Counter] -> can add any time
	"""
	for token, docid, weight in tokens:
		index[token][DTRANS[docid]] += weight

def main(index: dict, imgIndex: dict):
	try:
		docCountPrev = 0
		docCountCont = 0
		searchTime = time.time()

		contPoint = index.get('& LAST DOC &', 0)
		tokensList = [] # [(token, docID, priority)]
		for l in interact_files.readFromBook():
			d = DocID(l)
			DTRANS[d.getID()] = d
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


if __name__ == '__main__':
	if len(sys.argv) == 1:
		loadTime = time.time()
		index = interact_files.loadIndexFromFile('main')
		imgIndex = interact_files.loadIndexFromFile('img')

		ANALYTICS['load'] = time.time() - loadTime

	elif sys.argv[1] in {'-r', 'reload'}:
		""" Index isn't necessarily needed until we need to merge...Maybe better to keep it
		out of memory, but either way is okay"""
		index = defaultdict(Counter) # {token : {docID: priority} }
		imgIndex = defaultdict(list) # {(title, imgAlt): [(srcurl, priority)]}
		interact_files.resetIndexFiles()
	else:
		raise Warning("Invalid command line input")

	main(index, imgIndex)