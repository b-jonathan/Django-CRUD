from socket import fromshare
from django import forms  
from .models import Complain, ComplainDetails, IcProblemanalysis, IcCapa  
class ComplainForm(forms.ModelForm):  
    class Meta:  
        model = Complain
        fields = "__all__"  

class DetailForm(forms.ModelForm):  
    class Meta:  
        model = ComplainDetails
        fields = "__all__"  
        
class PAForm(forms.ModelForm):  
    class Meta:  
        model = IcProblemanalysis
        fields = "__all__"  
        
class CapaForm(forms.ModelForm):  
    class Meta:  
        model = IcCapa
        fields = "__all__"  