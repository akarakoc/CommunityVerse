from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import connection

from community.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts

def LoginPage(request):
    return render(request, 'login.html', {'community_resp': 'test'}) 

def index(request):
    Community_List = Communities.objects.all()
    paginator = Paginator(Community_List, 3)
    page = request.GET.get('page')
    community_resp = paginator.get_page(page)   
    return render(request, 'index.html', {'community_resp': community_resp}) 
	
def communityForm(request):
    form="""
	<form>
		<div class="form-entry">
			<label for="validationServer01">Community Name</label>
			<input type="text" class="form-control is-valid" id="validationServer01" placeholder="" value="" required>
			<div class="valid-feedback">
				Looks good!
			</div>
		</div>
		<div class="form-entry">
			<label for="validationServer02">Community Description</label>
			<input type="text" class="form-control is-valid" id="validationServer02" placeholder="" value="" required>
			<div class="valid-feedback">
				Looks good!
			</div>
		</div>
		<div class="form-group">
			<label for="exampleFormControlFile1">Community Image</label>
			<input type="file" class="form-control-file" id="exampleFormControlFile1">
		</div>
		<div class="form-check">
			<input class="form-check-input position-static" type="checkbox" id="blankCheckbox" value="" aria-label="">
			<label for="blankCheckbox">Private Community</label>
		</div>
	</form>
	
	"""
    return HttpResponse(form)
	
def DatatypePage(request):
    CommunityName = request.GET.get('showDataTypes')
    Community_List = Communities.objects.filter(name=CommunityName)
    dt = Community_List[0].datatypes_set.all()
    paginator = Paginator(dt, 5)
    page = request.GET.get('page')
    dt_resp = paginator.get_page(page)   
    return render(request, 'datatypes.html', {'dt_resp': dt_resp})
	
def PostPage(request):
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
