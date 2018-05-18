import interact_files
from structures import DocID
import json


def query(index: dict, query: str, amount=10) -> [{'docid': int}]:
	""" TEMP: only searches index by exact matches on query. Does not canonicalize
	or use operators.
	Returns first `amount` results"""
	try:
		q = query.lower()
		return index[q].most_common()[:amount]	
	except IndexError:
		# Results are less than amount, just give all. 
		return index[q].most_common()

def getDocIDs() -> dict:
	with open('bookkeeping.json', 'r') as file:
		return json.loads(file.read())


def main():
	index = interact_files.loadIndexFromFile('main')
	docs = getDocIDs()


	q = input("Give me a search query: ")
	while q != '':
		results = query(index, q)
		for r in results:
			print(r)
			print(docs['/'.join(r[0])])
		print('--------------')
		q = input("Give me a search query: ")


if __name__ == '__main__':
	main()