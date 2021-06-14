from django.urls import path

from .views import APIGetResult, APIPoll, APIVote

urlpatterns = [
    path('v1/createPoll/', APIPoll.as_view()),
    path('v1/poll/', APIVote.as_view()),
    path('v1/getResult/', APIGetResult.as_view()),
]
