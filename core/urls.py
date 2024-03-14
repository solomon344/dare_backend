from django.urls import path
from . import views


urlpatterns = [
    path('users/all',views.profileViewSet.as_view()),
    path('rooms/all',views.roomViewSet.as_view()),
    path('messages/all',views.messageViewSet.as_view()),
    path('login',views.Login_User.as_view(),name='login'),
    path('get',views.get_csrfToken.as_view())
]