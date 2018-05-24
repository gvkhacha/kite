from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def search(request):
	if request.POST:
		print(request.POST['term'])
		return HttpResponseRedirect("/")
	else:
		return render_to_response('search.html')
