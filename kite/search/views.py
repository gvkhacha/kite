from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from search import query


def index(request):
    return render_to_response('index.html')

@csrf_exempt
def search(request):
	if request.POST:
		if request.POST['term'] == '':
			return render_to_response('index.html')
		if 'main' in request.POST:
			return render_to_response('search.html', {'query': request.POST['term'], 'result': query.searchIndex(request.POST['term'])})
		elif 'images' in request.POST:
			return render_to_response('index.html')
	else:
		return render_to_response('index.html')
