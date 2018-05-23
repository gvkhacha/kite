import sqlite3
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer() #Not sure, but probably better to init once.



def resultGenerator(query: str, c, stop=10):
	""" Generator that will fetch another row on a given query.
	Query should already be stripped/lowercase/lemmatized/etc
	* currently only works with one-word queries"""
	q = tuple(query.split())
	c.execute('SELECT * FROM occurances WHERE token=? ORDER BY weight DESC', q)
	for _ in range(stop, 0, -1):
		yield c.fetchone()

def getQueryInput() -> str:
	""" Gets string input from user to use as query - makes all
	changes as needed to get ready for searching """
	q = input("Input Query: ").strip().lower()
	return lmtzr.lemmatize(q)

def search(c):
	q = getQueryInput()
	while q != '':
		for i in resultGenerator(q, c):
			print(i)
		q = getQueryInput()



def main():
	conn = sqlite3.connect('index.sqlite')
	c = conn.cursor()

	search(c)

	conn.close()

if __name__ == '__main__':
	main()