from django import forms
from models import WFPDocument, Category
from geonode.base.models import Region
from geonode.documents.forms import DocumentForm
import datetime

class WFPDocumentForm(forms.ModelForm):
    publication_date = forms.DateField(initial=datetime.date.today)
    source = forms.CharField()
    orientation = forms.ChoiceField(WFPDocument.ORIENTATION_CHOICES)
    page_format = forms.ChoiceField(WFPDocument.FORMAT_CHOICES)
    categories = forms.ModelMultipleChoiceField(Category.objects.all())
    regions = forms.ModelMultipleChoiceField(Region.objects.all(), required=False)
    last_version = forms.BooleanField(initial=True, required=False)
    
    class Meta:
        model = WFPDocument
        exclude = ('document',)
        
    def __init__(self, *args, **kwargs):
        super(WFPDocumentForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance'):
            if hasattr(self.instance, 'document'):
                self.fields['publication_date'].initial = self.instance.document.date
