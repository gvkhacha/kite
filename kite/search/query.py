from django.db import connection
from bs4 import BeautifulSoup
import urllib.parse

def _getResultFromIndex(query: str) -> list:
	""" Return raw result sqlite database """
	q = tuple(query.strip().split())
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM occurances WHERE token=%s ORDER BY weight DESC', q)
		return cursor.fetchmany(10)

def _formatResults(raw: list) -> list:
	""" Taking raw results from database, format the data
	into usable format for printing 
	raw: [('token', 'ID:URL', WEIGHT)]
	result: [(ID, URL, TITLE)]"""
	results = []
	for tok, doc, idf in raw:
		docid, url = doc.split(':')
		if not url.startswith('http'):
			url = 'http://' + url
		results.append( {'id':docid,'url':url, 'meta':_getPageMetaData(docid, url)} )
	return results

def _getPageMetaData(docid: str, url: str) -> dict:
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
			result['desc'] = "No Meta Description found for this website."
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
	#Reversed because they get appended into a list in descending order
	return reversed(_formatResults(_getResultFromIndex(query)))