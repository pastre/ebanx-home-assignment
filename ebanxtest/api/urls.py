
from api.views import Event, Reset
from django.urls import path

urlpatterns = [

	path('event', Event.as_view(), name='event'),
	path('reset', Reset.as_view(), name='reset'),
]