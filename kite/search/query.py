
def searchIndex(query: str) -> list:
	""" Takes string query (generally from input)
	makes operations on them to be able to index sqlite
	"""
	results = []
	results.append(query)
	return results #temporarily, just put query into results.