import json, os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from geonode.documents.models import Document
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from models import WFPDocument, Category
from forms import WFPDocumentForm
from geonode.documents.forms import DocumentForm
from geonode.people.forms import ProfileForm
from geonode.maps.views import _perms_info
from geonode.documents.views import DOCUMENT_LEV_NAMES, IMGTYPES

ALLOWED_DOC_TYPES = settings.ALLOWED_DOCUMENT_TYPES

def document_browse(request, template='wfpdocs/document_list.html'):
    from geonode.search.views import search_page
    post = request.POST.copy()
    post.update({'type': 'document'})
    request.POST = post
    return search_page(request, template=template)

def document_detail(request, docid):
    """
    The view that show details of each document
    """
    document = get_object_or_404(Document, pk=docid)
    if not request.user.has_perm('documents.view_document', obj=document):
        return HttpResponse(loader.render_to_string('401.html',
            RequestContext(request, {'error_message':
                _("You are not allowed to view this document.")})), status=403)
    try:
        related = document.content_type.get_object_for_this_type(id=document.object_id)
    except:
        related = ''

    document.popular_count += 1
    document.save()

    return render_to_response("wfpdocs/document_detail.html", RequestContext(request, {
        'permissions_json': json.dumps(_perms_info(document, DOCUMENT_LEV_NAMES)),
        'document': document,
        'imgtypes': IMGTYPES,
        'related': related
    }))
    
@login_required
def document_update(request, id=None, template_name='wfpdocs/document_form.html'):
    
    wfpdoc = None
    if id:
        wfpdoc = get_object_or_404(WFPDocument, pk=id)

    if request.method == 'POST':
        try:
            content_type = ContentType.objects.get(name=request.POST['type'])
            object_id = request.POST['q']
        except:
            content_type = None
            object_id = None
        title = request.POST['title']
        doc_file = None
        if 'file' in request.FILES:
            doc_file = request.FILES['file']
        
            if len(request.POST['title'])==0:
                return HttpResponse(_('You need to provide a document title.'))
            if not os.path.splitext(doc_file.name)[1].lower()[1:] in ALLOWED_DOC_TYPES:
                return HttpResponse(_('This file type is not allowed.'))
            if not doc_file.size < settings.MAX_DOCUMENT_SIZE * 1024 * 1024:
                return HttpResponse(_('This file is too big.'))
        # map document
        form = WFPDocumentForm(request.POST)
        if form.is_valid():
            source = form.cleaned_data.get('source')
            publication_date = form.cleaned_data.get('publication_date')
            orientation = form.cleaned_data.get('orientation')
            page_format = form.cleaned_data.get('page_format')
            categories = form.cleaned_data.get('categories')
            regions = form.cleaned_data.get('regions')
            last_version = form.cleaned_data.get('last_version')
        if wfpdoc is None:
            wfpdoc = WFPDocument()
        wfpdoc.source = source
        wfpdoc.orientation = orientation
        wfpdoc.page_format = page_format
        wfpdoc.last_version = last_version
        # if we are creating the static map, we need to create the document as well
        if not id:
            document = Document(content_type=content_type, object_id=object_id, 
                title=title, doc_file=doc_file)
            document.owner = request.user
            document.save()
            wfpdoc.document = document
        else:
            document = wfpdoc.document
        # title=title, doc_file=doc_file, date=publication_date, regions=regions
        document.owner = request.user
        document.title = title
        if doc_file:
            document.doc_file = doc_file
        document.date = publication_date
        document.regions = regions
        document.save()
        document.update_thumbnail()
        #wfpdoc = WFPDocument(source = source, orientation=orientation,
        #    page_format=page_format, document=document)
        wfpdoc.save()
        wfpdoc.categories = categories
        return HttpResponseRedirect(reverse('wfpdocs-browse'))
    else:
        if wfpdoc:
            form = WFPDocumentForm(instance=wfpdoc, 
                initial={'regions': wfpdoc.document.regions.all()})
        else:
            form = WFPDocumentForm()
        # some field in the form must be manually populated
        return render_to_response(
            'wfpdocs/document_form.html',
            { 'form': form,
            },
            RequestContext(request)
        )
        

