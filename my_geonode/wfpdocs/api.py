from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from geonode.documents.models import Document
from geonode.base.models import Region

from models import WFPDocument, Category

class CategoryResource(ModelResource):
    
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        excludes = ['id',]
        include_resource_uri = False
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        filtering = {
            'name': ALL_WITH_RELATIONS,
        }
        
class RegionResource(ModelResource):
    
    class Meta:
        queryset = Region.objects.all()
        resource_name = 'region'
        excludes = ['id',]
        include_resource_uri = False
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        cache = SimpleCache(timeout=10)
        
class DocumentResource(ModelResource):

    regions = fields.ToManyField(RegionResource, 'regions', full=True)
    geonode_page = fields.CharField(attribute='get_absolute_url', readonly=True)
    geonode_file = fields.FileField(attribute='doc_file')
    
    class Meta:
        queryset = Document.objects.all()
        resource_name = 'document'
        fields = ['title', 'date',]
        include_resource_uri = False
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        cache = SimpleCache(timeout=10)
        filtering = {
            'title': ALL,
            'date': ALL_WITH_RELATIONS,
        }
        
class WFPDocumentResource(ModelResource):

    document = fields.ToOneField(DocumentResource, 'document', full=True)
    categories = fields.ToManyField(CategoryResource, 'categories', full=True)
    
    class Meta:
        queryset = WFPDocument.objects.all()
        resource_name = 'wfp-document'
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        cache = SimpleCache(timeout=10)
        filtering = {
            'document': ALL_WITH_RELATIONS,
            'categories': ALL_WITH_RELATIONS,
        }
        
    def dehydrate_page_format(self, bundle):
        return WFPDocument.FORMAT_CHOICES[bundle.data['page_format']][1]
        
    def dehydrate_orientation(self, bundle):
        return WFPDocument.ORIENTATION_CHOICES[bundle.data['orientation']][1]
        
    def build_schema(self):
        base_schema = super(WFPDocumentResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })
        return base_schema
        

