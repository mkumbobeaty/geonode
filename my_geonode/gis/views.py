from django.shortcuts import render_to_response

from models import Employee

from djgeojson.views import GeoJSONLayerView

class EmployeeLayer(GeoJSONLayerView):
    
    def get_queryset(self):
        context = Employee.objects.all().filter(duties_type=0)
        return context

def ___employees_geojson(request):
    object_list = Employee.objects.all()
    properties=['place', 'country', 'wfpregion', 'facility',
                 'name', 'position']
    return render_to_response(
        'gis/employees.geojson',
        {
            'object_list': object_list,
            'properties': properties,
        }, )
