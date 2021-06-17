from django.urls import path

from .views import APIGetResult, APIPoll, APIVote

urlpatterns = [
    path('v1/createPoll/', APIPoll.as_view(), name='create-poll'),
    path('v1/poll/', APIVote.as_view(), name='poll'),
    path('v1/getResult/', APIGetResult.as_view(), name='get-result-poll'),
]
