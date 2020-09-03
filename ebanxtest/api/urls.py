
from api.views import Event, Reset, Balance
from django.urls import path

urlpatterns = [

	path('event', Event.as_view(), name='event'),
	path('balance', Balance.as_view(), name='balance'),
	path('reset', Reset.as_view(), name='reset'),
]