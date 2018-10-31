from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point, GEOSGeometry
from geonode.people.models import Profile
from models import Office, Employee
    
def import_offices():
    Office.objects.all().delete()
    ds = DataSource('wfp/gis/data/wld_poi_facilities_wfp.shp')
    print(ds)
    lyr = ds[0]
    print lyr.fields
    # 'wfpid', u'place', u'facility', u'status', u'iso3', u'iso3_op', u'country'
    # u'locprecisi', u'latitude', u'longitude', u'wfpregion', u'nat_staff', 
    # u'int_staff', u'lastcheckd', u'remarks', u'source', u'createdate', 
    # u'updatedate', u'objectidol', u'precisiono', u'verifiedol'
    for feat in lyr:
        geom = feat.geom
        pnt = GEOSGeometry(geom.ewkt)
        wfpid = feat.get('wfpid')
        place = feat.get('place')
        facility = feat.get('facility')
        status = feat.get('status')
        country = feat.get('country')
        wfpregion = feat.get('wfpregion')
        lastcheckd = feat.get('lastcheckd')
        createdate = feat.get('createdate')
        updatedate = feat.get('updatedate')
        source = feat.get('source')
        office = Office(geom=pnt, wfpid=wfpid, place=place, facility=facility,
            wfpregion=wfpregion, lastcheckd=lastcheckd, source=source,
            status=status, country=country, createdate=createdate,
            updatedate=updatedate)
        office.save()
        
def create_employees():
    Employee.objects.all().delete()
    o = Office.objects.all()[0]
    for p in Profile.objects.all():
        e = Employee(profile=p, office=o)
        e.save()
