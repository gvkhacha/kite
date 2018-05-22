from database import interact_files
from collections import defaultdict, Counter
from structures import DocID

import math, sqlite3


def insertIntoDb(c, data: list) -> None:
	""" Takes data and inserts into 'occurances' table of
	database (SQL) """
	# c.execute("INSERT INTO occurances (token, doc, weight) VALUES ('{}', '{}', {:.4f})".format(token, doc, weight))
	c.executemany("INSERT INTO occurances VALUES (?, ?, ?)", data)

def insertIntoImgTable(c, data: list) -> None:
	c.executemany("INSERT INTO images VALUES (?, ?, ?, ?)", data)
	

def calculateWeight(token: str, values: dict, numDocs: int)-> list:
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

def extractDataFromImages(token:str, values: dict, numDocs:int) -> list:
	""" Looking at a single token, extract all the data from the 
	ImgID object and normalize weight.
	Formula (weight) = (1 + log(tf)) * (log(N/df))
		N = # of total documents
		df = # of documents token appears in """
	data = []

	docFreq = len(values)
	for img, tf in values.items():
		weight = 1 + math.log(tf, 10)
		weight *= math.log(numDocs/docFreq, 10)

		x, y = img.getID()
		docToString = "{}/{}:{}".format(x, y, img.getURL())


		data.append( (token, docToString, img.getImgURL(), weight) )

	return data



def mainToDatabase(c):
	index = interact_files.loadIndexFromFile('main')
	numDocs = index['& LAST DOC &']

	for k, v in index.items():
		if isinstance(v, dict):
			data = calculateWeight(k, v, numDocs)
			insertIntoDb(c, data)

def imageToDatabase(c):
	imgIndex = interact_files.loadIndexFromFile('img')
	numDocs = 37455 # Didn't save this, just going to write as is

	for k, v in imgIndex.items():
		if isinstance(v, dict):
			data = extractDataFromImages(k, v, numDocs)
			insertIntoImgTable(c, data)

def main():
	conn = sqlite3.connect('index.sqlite')
	c = conn.cursor()

	# mainToDatabase(c)
	imageToDatabase(c)

	conn.commit()
	conn.close()

if __name__ == '__main__':
	main()