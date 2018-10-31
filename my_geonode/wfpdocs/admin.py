from django.contrib import admin
from wfp.wfpdocs.models import WFPDocument, Category
from account.models import EmailAddress

# we keep here it for now
class EmailAddressAdmin(admin.ModelAdmin):
    model = EmailAddress
    list_display = ('user', 'email', 'verified')
    list_filter = ('verified',)
    #search_fields = ('name', 'workspace',)

class WFPDocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'get_date', 'get_date_type', 'get_regions', 
        'source', 'get_categories', 'orientation', 'page_format', )
    list_display_links = ('document',)
    list_filter  = ('orientation', 'page_format', 'categories' )
    search_fields = ('document__title',)
    #date_hierarchy = 'date'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
        
admin.site.register(WFPDocument, WFPDocumentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
