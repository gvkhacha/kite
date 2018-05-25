from django.db import connection
from bs4 import BeautifulSoup, Comment
import urllib.parse
import re

def _getResultFromIndex(query: str) -> list:
	""" Return raw result sqlite database """
	q = tuple(query.strip().split())
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM occurances WHERE token=%s ORDER BY weight DESC', q)
		return cursor.fetchmany(10)

def _formatResults(raw: list, query: str) -> list:
	""" Taking raw results from database, format the data
	into usable format for printing 
	raw: [('token', 'ID:URL', WEIGHT)]
	result: [(ID, URL, TITLE)]"""
	results = []
	for tok, doc, idf in raw:
		docid, url = doc.split(':')
		if not url.startswith('http'):
			url = 'http://' + url
		results.append( {'id':docid,'url':url, 'meta':_getPageMetaData(docid, url, query)} )
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


def searchIndex(query: str) -> list:
	""" Takes string query (generally from input)
	makes operations on them to be able to index sqlite
	"""
	query = query.lower().strip()
	raw = _getResultFromIndex(query)
	results = _formatResults(raw, query)
	#Reversed because they get appended into a list in descending order
	return reversed(results)
