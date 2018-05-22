from database import interact_files
from collections import defaultdict, Counter
from structures import DocID

import math, sqlite3


def insertIntoDb(c, data: list) -> None:
	""" Takes data and inserts into 'occurances' table of
	database (SQL) """
	# c.execute("INSERT INTO occurances (token, doc, weight) VALUES ('{}', '{}', {:.4f})".format(token, doc, weight))
	c.executemany("INSERT INTO occurances VALUES (?, ?, ?)", data)

	

def calculateWeight(token: str, values: dict, numDocs: int, c) -> None:
	""" Looking at a single token, and values already have
	term frequencies: calculates weight of each document 
	based on normalized term frequency and inverse document
	frequency
	Formula (weight) = (1 + log(tf)) * (log(N/df))
		N = # of total documents
		df = # of documents token appears in """
	data = []

	docFreq = len(values)
	for doc, tf in values.items():
		weight = 1 + math.log(tf, 10)
		weight *= math.log(numDocs/docFreq, 10)
		x, y = doc.getID()
		docToString = "{}/{}:{}".format(x, y, doc.getURL())
		# insertIntoDb(c, token, docToString, weight)
		data.append( (token, docToString, weight) )
	return data


def main():
	conn = sqlite3.connect('index.sqlite')
	c = conn.cursor()


	index = interact_files.loadIndexFromFile('main')
	numDocs = index['& LAST DOC &']

	for k, v in index.items():
		if isinstance(v, dict):
			data = calculateWeight(k, v, numDocs, c)
			insertIntoDb(c, data)
	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()