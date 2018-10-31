from django.template import RequestContext
from django.shortcuts import render_to_response
import json
from django.http import HttpResponse

from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document
from geonode.people.models import Profile
from geonode.search.views import search_api
from geonode.search.search import _filter_security

def index(request):
    post = request.POST.copy()
    post.update({'type': 'layer'})
    request.POST = post
    return search_page(request, template='site_index.html')

def search_page(request, template='search/search.html', **kw): 
    results, facets, query = search_api(request, format='html', **kw)

    facets = {      
        'maps' : Map.objects.count(),
        'layers' : Layer.objects.count(),
        'documents': Document.objects.count(),
        'users' : Profile.objects.count()
    }
    
    featured_maps = Map.objects.filter(keywords__name__in=['featured'])
    featured_maps = _filter_security(featured_maps, request.user, Map, 'view_map').order_by('data_quality_statement')[:4]
    
    return render_to_response(template, RequestContext(request, {'object_list': results, 
        'facets': facets, 'total': facets['layers'], 'featured_maps': featured_maps }))
    
def contacts(request):
    profiles = Profile.objects.filter(user__groups__name='OMEP GIS Team').order_by('name')
    return render_to_response('contacts.html', 
        {   
            'profiles': profiles,
        },
        context_instance=RequestContext(request))
        
def owslogin(request):
    
    # it will work only for requests from localhost!
    #ip = request.META.get('REMOTE_ADDR')
    #if ip != ('127.0.0.1'):
    #        return HttpResponse(
    #                "Operation not allowed.",
    #                status=403,
    #                content_type="text/plain"
    #                )
    
    # authentication
    username = ''
    password = ''
    if 'username' in request.GET:
        username = request.GET.get('username', '')
    if 'password' in request.GET:
        password = request.GET.get('password', '')
    from django.contrib.auth import authenticate, login
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
    else:
        return HttpResponse(
            "Operation not allowed.",
            status=403,
            content_type="text/plain"
        )

    response_data = {}
    response_data['result'] = 'ok'
    response_data['message'] = 'Authenticated with GeoNode for OWS requests.'
    return HttpResponse(json.dumps(response_data), 
        content_type="application/json")

