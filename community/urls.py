from django.urls import path
from . import views

    
urlpatterns = [
    path('', views.index, name='index'),
    path('sendCommunityForm/', views.communityForm, name='index'),
    path('sendDatatypePage/', views.DatatypePage, name='index'),
    path('sendPostPage/', views.PostPage, name='index'),
	path('login/', views.LoginPage, name='index'),	
]
