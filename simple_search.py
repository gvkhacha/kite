from database import interact_files
from structures import DocID

import json
from collections import Counter


def searchIndex(index: dict, query: str, amount=10) -> [{'docid': int}]:
	""" TEMP: only searches index by exact matches on query. Does not canonicalize
	or use operators.
	Returns first `amount` results"""
	q = query.lower()
	if ' ' in q:
		combined = []
		for i in q.split():
			combined.extend(searchIndex(index, i))
		# Add all results, then get the best of the results
		results = Counter()
		for k, v in sorted(combined):
			results[k] += v


		try:
			return results.most_common()[:amount]
		except IndexError:
			return results.most_common()
	else:
		try:
			return index[q].most_common()[:amount]	
		except IndexError:
			# Results are less than amount, just give all. 
			return index[q].most_common()

def getDocIDs() -> dict:
	with open('bookkeeping.json', 'r') as file:
		return json.loads(file.read())


def main():
	index = interact_files.loadIndexFromFile('main')


	q = input("Give me a search query: ")
	while q != '':
		results = searchIndex(index, q)
		for r in results:
			doc = r[0]
			print(doc.getID())
			print(doc.getURL())
		print('--------------')
		q = input("Give me a search query: ")


if __name__ == '__main__':
	main()