from django.shortcuts import render

from community.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts

def index(request):
    CommunityList = Communities.objects.all()
    Datatypes = Communities.Datatypes
    context = {
        'Communities1': CommunityList[0],
		'Communities2': CommunityList[1]
    }
	
    return render(request, 'index.html', context=context)

