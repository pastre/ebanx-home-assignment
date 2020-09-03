
from api.views import Event
from django.urls import path

urlpatterns = [

	path('event', Event.as_view(), name='event'),
]