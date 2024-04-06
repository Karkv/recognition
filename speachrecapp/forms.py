from django import  forms
from . models import videoupload

class uploadfile(forms.Form):

    class Meta:
        fields=['video']