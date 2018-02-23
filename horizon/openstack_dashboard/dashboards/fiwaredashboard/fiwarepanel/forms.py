# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget
import json

class newServiceForm(forms.Form):
    #attrs = { 'required': True}
    attrs =  {'class':'form-control', 'required': True}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
