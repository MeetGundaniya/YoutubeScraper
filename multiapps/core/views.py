"""
This module handle request within CoreApp
"""

# DJANGO LIBRARY
from django.shortcuts import render

# FIRSTPARTY LIBRARY
from backend.settings import env



def response_not_found(request, *args, **kwargs):
  return render(request, '404.html')

def response_server_error(request, *args, **kwargs):
  return render(request, '500.html', {'github_link': env.str('GITHUB_LINK', '#')})
