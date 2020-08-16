from django.urls import path

from . import views

# not following REST here, need all url to GET so scripts can triggered from browser iteself
urlpatterns = [
    path('chatrooms', views.Chatrooms.as_view()),
    path('search', views.UserSearch.as_view()),
    path('request', views.Request.as_view()),
    path('accept', views.RequestAccept.as_view()),
    path('decline', views.RequestDecline.as_view()),
    path('pending', views.PendingRequests.as_view())
]
