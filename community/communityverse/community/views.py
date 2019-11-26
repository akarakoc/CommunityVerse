from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import connection
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UsersLoginForm, UsersRegisterForm
from .forms import UsersRegisterForm
from .forms import AddCommunity
from .forms import AddDatatype
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string, get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import json
import requests
import uuid
import hashlib
from datetime import datetime
from community.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts

def LoginPage(request):
    return render(request, 'login.html', {'community_resp': 'test'}) 

def index(request):
    if request.user.is_authenticated:
        Community_List = Communities.objects.all()
        paginator = Paginator(Community_List, 3)
        page = request.GET.get('page')
        community_resp = paginator.get_page(page)
        return render(request, 'index.html', {'community_resp': community_resp})
    else:
        return HttpResponseRedirect("/community/login")
	
def communityForm(request):
    form = AddCommunity()
    return render(request, 'modal.html', {'form': form})
	
def datatypeForm(request):
    form = AddDatatype()
    return render(request, 'modal.html', {'form': form})

def searchTag_view(request):
    txtSRC = request.GET.get('search_text')
    SEARCHPAGE = txtSRC	
    PARAMS = {
		"action": "query",
		"format": "json",
		"list": "search",
		"srsearch": SEARCHPAGE
    }
    Srch = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    Res = Srch.get(url=URL, params=PARAMS)
    DATA = Res.json()['query']['search']
    titles=""
    for tt in DATA:
        titles+="#"+tt['title']
    return render_to_response('tagSearch.html', {'form' : titles})


def handle_uploaded_file(f):
    filepath = 'community/static/uploads/communities/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"

def CreateCommunity_view(request):
    form = AddCommunity(request.POST, request.FILES)
    c_image=request.FILES.get("Community_Image")
    image_path=handle_uploaded_file(c_image)
    comm = Communities()
    comm.name = request.POST.get("Community_Name")
    comm.description = request.POST.get("Community_Description")
    salt = uuid.uuid4().hex
    comm.communityHash = hashlib.sha256(salt.encode() + comm.name.encode()).hexdigest() + ':' + salt
    if request.POST.get("Private_Community"):
        comm.communityPrv = True
    else:
        comm.communityPrv = False
    comm.communityPhoto = image_path
    comm.communityPopularity = 0
    comm.communityTags = request.POST.get("Community_Tags")
    comm.communityCreationDate = datetime.now()
    comm.communityCreator = communityUsers.objects.get(nickName=request.user)
    comm.save()
    comm.communityMembers.add(communityUsers.objects.get(nickName=request.user))
    comm.save()
    return render_to_response('tagSearch.html', {'form' : "Community is created Successfully!"})
		 
def DatatypePage(request):
    if request.user.is_authenticated:
        CommunityHash = request.GET.get('showDataTypes')
        Community_List = Communities.objects.filter(communityHash=CommunityHash)
        dt = Community_List[0].datatypes_set.all()
        paginator = Paginator(dt, 5)
        page = request.GET.get('page')
        dt_resp = paginator.get_page(page)
        return render(request, 'datatypes.html', {'dt_resp': dt_resp, 'community_hash':CommunityHash, 'community':Community_List[0]})
    else:
        return HttpResponseRedirect("/community/login")


def handle_uploaded_datatypefile(f):
    filepath = 'community/static/uploads/datatypes/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"
	
def CreateDatatype_view(request):
    form = AddDatatype(request.POST, request.FILES)
    d_image=request.FILES.get("Datatype_Image")
    image_path=handle_uploaded_datatypefile(d_image)
    dt = Datatypes()
    comm.name = request.POST.get("Community_Name")
    comm.description = request.POST.get("Community_Description")
    salt = uuid.uuid4().hex
    comm.communityHash = hashlib.sha256(salt.encode() + comm.name.encode()).hexdigest() + ':' + salt
    if request.POST.get("Private_Community"):
        comm.communityPrv = True
    else:
        comm.communityPrv = False
    comm.communityPhoto = image_path
    comm.communityPopularity = 0
    comm.communityTags = request.POST.get("Community_Tags")
    comm.communityCreationDate = datetime.now()
    comm.communityCreator = communityUsers.objects.get(nickName=request.user)
    comm.save()
    comm.communityMembers.add(communityUsers.objects.get(nickName=request.user))
    comm.save()
    return render_to_response('tagSearch.html', {'form' : "Community is created Successfully!"})
	
def PostPage(request):
    if request.user.is_authenticated:
        DatatypeId = request.GET.get('showPosts')
        Datatype_Primitive = Datatypes.objects.filter(id=int(DatatypeId))
        Primitive_List = Datatype_Primitive[0].datatypefields_set.all()
        c = connection.cursor()
        execution_string = 'select "entryHash",json_object_agg("propertyName","propertyValue") from (select "entryHash","propertyName","propertyValue" from community_posts where "relatedDatatypes_id"='+DatatypeId+') S GROUP BY "entryHash"'
        c.execute(execution_string)
        posts=c.fetchall()
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page)
        return render(request, 'posts.html', {'post_resp': post_resp,'table_fields':Primitive_List,'Datatype_Id':DatatypeId, 'Datatype_name':Datatype_Primitive})
    else:
        return HttpResponseRedirect("/community/login")

def login_view(request):
    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect("/community")
    return render(request, "login.html", {
		"form" : form,
		"title" : "Login",})


def register_view(request):
    form = UsersRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        comUsers = communityUsers()
        comUsers.userMail = user.email
        comUsers.nickName = user.username
        comUsers.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect("/community/login")
    return render(request, "login.html", {
	    "title" : "Register",
	    "form" : form,
    })
 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/community/login")
	
def profilePage(request):
    if request.user.is_authenticated:
        userinfo=request.user
        return render(request, "profile.html", {
	"user" : userinfo,
	"title" : "Login",
	})
    else:
        return HttpResponseRedirect("/community/login")
