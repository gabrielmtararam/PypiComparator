from extractor import models as mod
from django import forms


class PypiSimpleIndexLinksForm(forms.ModelForm):
    """StationCodeType model admin form."""

    class Meta(object):  # NOQA
        model = mod.PypiSimpleIndexLinks
        fields = '__all__'


class PypiProcessedLinkForm(forms.ModelForm):
    """StationCodeType model admin form."""

    class Meta(object):  # NOQA
        model = mod.PypiProcessedLink
        fields = '__all__'



class GlobalProcessorParametersForm(forms.ModelForm):
    """StationCodeType model admin form."""

    class Meta(object):  # NOQA
        model = mod.GlobalProcessorParameters
        fields = '__all__'


