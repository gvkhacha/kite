from django.db import connection


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
		results.append( (docid, url) )
	return results



def searchIndex(query: str) -> list:
	""" Takes string query (generally from input)
	makes operations on them to be able to index sqlite
	"""
	return _formatResults(_getResultFromIndex(query))