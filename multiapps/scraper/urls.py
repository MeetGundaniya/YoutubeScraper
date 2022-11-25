"""
ScraperApp URL Configuration
"""

# DJANGO LIBRARY
from django.urls import path

# FIRSTPARTY LIBRARY
# # FIRSTPARTY LIBRARY
from scraper import views as scraper_views



urlpatterns = [
  path("", scraper_views.HomeTemplateView.as_view(), name="home"),
  path("results", scraper_views.SearchTemplateView.as_view(), name="search-query"),
  path("watch", scraper_views.WatchTemplateView.as_view(), name="watch-video"),
  path("channel/<str:c_id>", scraper_views.VideoTemplateView.as_view(), name="channel"),
]
