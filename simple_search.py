import interact_files
from structures import DocID
import json

def query(index: dict, q: str):
	return index[q].most_common()[:5]

def getDocIDs() -> dict:
	with open('bookkeeping.json', 'r') as file:
		return json.loads(file.read())


def main():
	index = interact_files.loadIndexFromFile('main')
	docs = getDocIDs()


	q = input("Give me a search query: ")
	results = query(index, q)
	for r in results:
		print(r)
		print(docs['/'.join(r[0])])


if __name__ == '__main__':
	main()