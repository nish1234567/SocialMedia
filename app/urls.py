from django.urls import path
from app.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from socialmedia.settings import REST_FRAMEWORK

urlpatterns = [
    path('register',Register.as_view()),
    path('profile',Profile.as_view()),
    path('Login',Login.as_view()),
    path('like',Like.as_view()),
    path('comment',Comment.as_view()),
    path('postComment/<int:pk>',PostComments.as_view()),
    path('postComment',PostComments.as_view()),
    path('sendRequest',SendRequest.as_view()),
    path('AcceptRequest',AcceptRequest.as_view()),
    path('postView',PostView.as_view()),
    path('gettoken/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refreshtoken/',TokenRefreshView.as_view(),name='token_refresh'),
    path('verifytoken/',TokenVerifyView.as_view(),name='token_verify')
]
