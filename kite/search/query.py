from django.db import connection

def searchIndex(query: str) -> list:
	""" Takes string query (generally from input)
	makes operations on them to be able to index sqlite
	"""

	q = tuple(query.strip().split())
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM occurances WHERE token=%s ORDER BY weight DESC', q)
		return cursor.fetchmany(10)
	return []