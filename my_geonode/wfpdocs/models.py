from django.db import models
from geonode.documents.models import Document

class Category(models.Model):
    """
    A WFM Map Document category
    """
    
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
        
class WFPDocument(models.Model):
    """
    A WFP document
    """
    
    ORIENTATION_CHOICES = (
        (0, 'Landscape'),
        (1, 'Portrait'),
    )
    
    FORMAT_CHOICES = (
        (0, 'A0'),
        (1, 'A1'),
        (0, 'A2'),
        (1, 'A3'),
        (0, 'A4'),
    )

    source = models.CharField(max_length=255)
    orientation = models.IntegerField('Orientation', choices=ORIENTATION_CHOICES)
    page_format = models.IntegerField('Format', choices=FORMAT_CHOICES)
    document = models.OneToOneField(Document)
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True)
    last_version = models.BooleanField(default=False)

    def __str__(self):  
          return "%s" % self.source
          
    def get_regions(self):
        regions = []
        for region in self.document.regions.all():
            regions.append(region.name)
        return ", ".join(regions )
    get_regions.short_description = 'Regions'
    
    def get_date(self):
        return self.document.date.isoformat()
    get_date.short_description = 'Date'
    
    def get_categories(self):
        categories = []
        for category in self.categories.all():
            categories.append(category.name)
        return ", ".join(categories)
    get_categories.short_description = 'Categories'
    
    def get_date_type(self):
        return self.document.date_type
    get_date_type.short_description = 'Date Type'
