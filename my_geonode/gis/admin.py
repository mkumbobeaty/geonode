from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from models import Office, Employee
from geonode.people.models import Profile
from geonode.people.admin import ProfileAdmin

class EmployeeInline(admin.StackedInline):
    model = Employee
    
class OfficeAdmin(GeoModelAdmin):
    model = Office
    
class ExtendedProfileAdmin(ProfileAdmin):
    inlines = [ EmployeeInline, ]
    
admin.site.register(Office, OfficeAdmin)
admin.site.unregister(Profile)
admin.site.register(Profile, ExtendedProfileAdmin)
