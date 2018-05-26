from django.db import connection
from bs4 import BeautifulSoup, Comment
import urllib.parse
import re
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer() #Not sure, but probably better to init once.

def _getResultFromIndex(query: str) -> list:
	""" Return raw result sqlite database """
	q = (query, )
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM occurances WHERE token=%s ORDER BY weight DESC', q)
		return cursor.fetchmany(10)

def _formatResults(raw: list, query: str) -> list:
	""" Taking raw results from database, format the data
	into usable format for printing 
	raw: [('token', 'ID:URL', WEIGHT)]
	result: [(ID, URL, TITLE)]"""
	results = []
	for doc, idf in raw:
		index = doc.find(':')
		docid = doc[:index]
		url = doc[index+1:]
		if not url.startswith('http'):
			url = 'http://' + url
		results.append( {'id':docid, 'url':url, 'weight': idf, 'meta':_getPageMetaData(docid, url, query)} )
	return results

def _tagVisible(element):
	""" Helper function to filter all non-visible text from soup document """
	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def _findSurroundingWords(soup, query: str) -> [str]:
	""" 
	Uses regex to find words around the given query to use as website description if other description was not found...
	Uses soup and extracts all not-visible text first. Considers first 3 unique results found, returns as list of string
	"""
	texts = soup.findAll(text=True)
	visibleTexts = ''.join([t for t in filter(_tagVisible, soup.body.findAll(text=True))])
	sub = '(\w*)\W*(\w*)\W*({})\W*(\w*)\W*(\w*)'.format(query)
	results = set()
	for i in re.findall(sub, visibleTexts, re.IGNORECASE):
		results.add(" ".join([x for x in i if x != '']))
		if len(results) > 3:
			break
	return results

def _getPageMetaData(docid: str, url: str, query: str) -> dict:
	""" Uses doc id to find document and find meta data
	(parsing through html head if necessary)"""
	result = dict()
	with open('../WEBPAGES_RAW/{}'.format(docid), 'r') as file:
		soup = BeautifulSoup(file, 'lxml')
		foundDesc = False
		for meta in soup.find_all('meta'):
			if meta.get('name', '') == 'description':
				result['desc'] = meta['content']
				foundDesc = True
				break
		if not foundDesc:
			result['desc'] = "...".join(_findSurroundingWords(soup, query))
		try:
			result['title'] = soup.title.string
		except:
			parsed = urllib.parse.urlparse(url)
			split = parsed.path.split('/')
			result['title'] = parsed.netloc + ' ' + split[0] + ' ' + split[-1]
	return result

def _isint(s: str) -> bool:
	try:
		int(s)
		return True
	except ValueError:
		return False

def _modifyQuery(query: str) -> [str]:
	""" Takes the full string query given by user input and modifies it 
	to separate queries that can be used for immediate SQL search.
	Also lemmatizes and adds that to list as well."""
	fields = [re.sub(r'\W+', '', q) for q in query.split()]
	results = []
	for i in range(len(fields)):
		if _isint(fields[i]):
			# add query with strings before and after number
			# don't need to lemmatize b/c it doesn't during building index
			if i != 0:
				prev = "{} {}".format(fields[i-1], fields[i]).lower()
				results.append(prev)
			if i != len(fields)-1:
				after = "{} {}".format(fields[i], fields[i+1]).lower()
				results.append(after)
		else:
			q = fields[i].lower().strip()
			results.append(q)
			results.append(lmtzr.lemmatize(q))
	return results

def _combineReuslts(raw: list) -> list:
	""" Gets a list of (query, docid, weight) pairs and returns a list of
	(docid, weight) pairs that have no unique docIDS. """
	results = []
	foundDocs = set()
	for tok, doc, weight in raw:
		if doc in foundDocs:
			for i in range(len(results)):
				if results[i][0] == doc:
					results[i] = (doc, results[i][1] + weight)
		else:
			foundDocs.add(doc)
			results.append( (doc, weight) )
	return results


def searchIndex(query: str) -> list:
	""" Takes string query (generally from input)
	makes operations on them to be able to index sqlite
	"""
	allResults = []
	for q in _modifyQuery(query):
		allResults.extend(_getResultFromIndex(q))
	combined = _combineReuslts(allResults)
	final = _formatResults(combined, query)
	#combineResults(allResults)?



	# print(_modifyQuery(query))
	# query = re.sub(r' \W+', '', query)
	# query = lmtzr.lemmatize(query.lower().strip())
	# raw = _getResultFromIndex(query)
	# results = _formatResults(allResults, query)
	#Reversed because they get appended into a list in descending order
	return sorted(final, key=lambda x: x['weight'], reverse=True)
