from django.urls import path

from . import views

# not following REST here, need all url to GET so scripts can triggered from browser iteself
urlpatterns = [
    path('chatrooms', views.Chatrooms.as_view()),
]
