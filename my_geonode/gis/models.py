from django.db import models
from django.contrib.gis.db import models as gismodels
from geonode.people.models import Profile

class Office(gismodels.Model):
    """
    Model for WFP Office.
    """
    wfpid = gismodels.IntegerField(null=True, blank=True)
    place = gismodels.CharField(max_length=254)
    facility = gismodels.CharField(max_length=254, null=True, blank=True)
    status = gismodels.CharField(max_length=254, null=True, blank=True)
    iso3 = gismodels.CharField(max_length=254, null=True, blank=True)
    iso3_op = gismodels.CharField(max_length=254, null=True, blank=True)
    country = gismodels.CharField(max_length=254, null=True, blank=True)
    locprecisi = gismodels.CharField(max_length=254, null=True, blank=True)
    latitude = gismodels.FloatField(null=True, blank=True)
    longitude = gismodels.FloatField(null=True, blank=True)
    wfpregion = gismodels.CharField(max_length=254, null=True, blank=True)
    nat_staff = gismodels.IntegerField(null=True, blank=True)
    int_staff = gismodels.IntegerField(null=True, blank=True)
    lastcheckd = gismodels.DateField(null=True, blank=True)
    remarks = gismodels.CharField(max_length=254, null=True, blank=True)
    source = gismodels.CharField(max_length=254, null=True, blank=True)
    createdate = gismodels.DateField(null=True, blank=True)
    updatedate = gismodels.DateField(null=True, blank=True)
    objectidol = gismodels.FloatField(null=True, blank=True)
    precisiono = gismodels.CharField(max_length=254, null=True, blank=True)
    verifiedol = gismodels.CharField(max_length=254, null=True, blank=True)
    geom = gismodels.PointField()
    objects = gismodels.GeoManager()
    
    def __unicode__(self):
        return '%s' % (self.place)
        
    class Meta:
        ordering = ['place']

class Employee(models.Model):
    """
    Model for WFP Profile.
    """
    
    GIS_LEVEL_CHOICES = (
        (0, 'Basic'),
        (1, 'Intermediate'),
        (2, 'Advanced'),
    )
    
    DUTIES_CHOICES = (
        (0, 'GIS'),
        (1, 'Not GIS')
    )
    
    gis_level = models.IntegerField(null=True, blank=True, choices=GIS_LEVEL_CHOICES)
    duties_type = models.IntegerField(blank = True, null=True, choices=DUTIES_CHOICES)
    profile = models.OneToOneField(Profile, primary_key=True)
    office = models.ForeignKey(Office, null=True, blank=True)
        
    @property
    def geom(self):
        return self.office.geom
        
    @property
    def place(self):
        return self.office.place
        
    @property
    def country(self):
        return self.office.country
        
    @property
    def wfpregion(self):
        return self.office.wfpregion
        
    @property
    def facility(self):
        return self.office.facility
        
    @property
    def name(self):
        return self.profile.name
        
    @property
    def position(self):
        return self.profile.position

    
    def __unicode__(self):
        return '%s in %s' % (self.profile.name, self.office.place)
