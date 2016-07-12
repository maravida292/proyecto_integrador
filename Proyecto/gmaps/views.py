from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def verMapa (request):
	return render_to_response ("verMapa.html", context_instance = RequestContext(request))