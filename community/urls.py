from django.urls import path
from django.conf.urls import include
from . import views


    
urlpatterns = [
    path('', views.index, name='index'),
    path('sendCommunityForm/', views.communityForm, name='index'),
    path('sendDatatypePage/', views.DatatypePage, name='index'),
    path('sendPostPage/', views.PostPage, name='index'),
	path('login/', views.login_view, name='login'),
	path('register/', views.register_view, name = "register"),
	path('logout/', views.logout_view, name = "logout"),
	path('profile/', views.profilePage, name = "profile"),
	path('searchTag/', views.searchTag_view, name = "searchTag"),
	path('CreateCommunity/', views.CreateCommunity_view, name = "CreateCommunity"),
	path('sendDatatypeForm/', views.datatypeForm, name = "Call datatype form"),
	path('CreateDatatype/', views.CreateDatatype_view, name = "CreateDatatype"),
]
