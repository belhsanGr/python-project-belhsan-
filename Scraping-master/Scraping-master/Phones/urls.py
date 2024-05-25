from django.urls import path
from . import views
urlpatterns = [
    path('', views.scrape_and_filter, name='scrape_and_filtersearch'),
]