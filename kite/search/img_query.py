from django.db import connection

import re

def _getResultFromIndex(query: str) -> list:
	""" Return raw result sqlite database """
	q = tuple(query.strip().split())
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM images WHERE token=%s ORDER BY weight DESC', q)
		return cursor.fetchall()

def _formatResults(raw: list, query: str) -> list:
	""" Taking raw results from database, format the data
	into usable format for printing 
	raw: [('token', 'ID:URL', WEIGHT)]
	result: [(ID, URL, TITLE)]"""
	results = []
	for tok, doc, img, idf in raw:
		index = doc.find(':')
		docid = doc[:index]
		url = doc[index+1:]
		if not url.startswith('http'):
			url = 'http://' + url
		if img.startswith('/'):
			imgurl = url + img
		elif img.startswith('http'):
			imgurl = img
		else:
			imgurl = 'http://' + img
		results.append( {'id':docid,'url':url, 'img': imgurl} )
	return results

def searchIndex(query: str) -> list:
	""" Takes string query (generally from input)
	makes operations on them to be able to index sqlite
	"""
	query = re.sub(r' \W+', '', query)
	query = query.lower().strip()
	raw = _getResultFromIndex(query)
	results = _formatResults(raw, query)
	#Reversed because they get appended into a list in descending order
	return reversed(results)
