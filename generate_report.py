"""
This module will create a report on runtime with the current database found with index.pickle.

 - It will observe the number of documents indexed (As found with a special analytics key placed in the index file)
 - It will provide other basic analytics for the actual index
 - It will use the search module and make some searches based on exact matches.
 	* There is no canonicalization in the search module
"""

import simple_search as search
from database import interact_files

import os #To get size of index

def generateStats(index: dict):
	print("Size of Index: {:.2f} KB".format(os.stat('index.pickle').st_size/1024))
	print("# of Docs: {}".format(index['& LAST DOC &']))
	print("# of Tokens: {}".format(len(index.keys())-1)) # 1 is stats ^^


def searchIndex(index: dict, docs: dict, queries: [str]) -> None:
	for q in queries:
		print("="*36)
		print("{:^36}".format("Search for " + q))
		print("="*36)
		counter = 1
		results = search.searchIndex(index, q)
		for r in results:
			print("{}. DocID: {}, Score: {}".format(counter, r[0], r[1]))
			counter += 1
			print("\t{}".format(docs['/'.join(r[0])]), end="\n\n")


def main():
	index = interact_files.loadIndexFromFile('main')
	docs = search.getDocIDs()
	queries = ['Informatics', 'Mondego', 'Irvine', 'artificial intelligence', 'computer science']

	generateStats(index)
	searchIndex(index, docs, queries)


if __name__ == '__main__':
	main()
