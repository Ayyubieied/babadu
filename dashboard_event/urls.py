from django.urls import path
from dashboard_event.views import *

app_name = 'dashboard_event'

urlpatterns = [
    path('enrolled_event', enrolled_event_table, name='enrolled_event_table'),
    path('', enrolled_partai, name='enrolled_partai'),
    path('create_sponsor', create_sponsor, name='create_sponsor'),
    path('read_sponsor', read_sponsor, name='read_sponsor'),
    path('sponsor_card', sponsor_card, name='sponsor_card'),
    path('logout/', logout, name='logout'),
]